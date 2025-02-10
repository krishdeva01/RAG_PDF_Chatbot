# app/models/generator.py

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Dict, List, Union
import pandas as pd
import logging

class Generator:
    def __init__(self, model_name: str = None, device: str = "cpu"):

        from app.config import Config
        
        self.config = Config
        self.model_name = model_name or self.config.GENERATOR_MODEL
        self.device = device
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.model.to(self.device)
        
        self.pipeline = pipeline(
            "text2text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=device
        )
        
        self.logger = logging.getLogger(__name__)

    def _format_table_context(self, tables: Dict[str, pd.DataFrame]) -> str:

        table_context = []
        for name, df in tables.items():
            table_str = f"Table {name}:\n"
            table_str += df.to_markdown(index=False)
            table_context.append(table_str)
        return "\n\n".join(table_context)

    def _format_image_context(self, images: Dict[str, Dict]) -> str:

        image_context = []
        for img_name, metadata in images.items():
            context_entry = f"Image {img_name}:\n"
            context_entry += f"Caption: {metadata['caption']}\n"
            context_entry += f"OCR Text: {metadata['text']}"
            image_context.append(context_entry)
        return "\n\n".join(image_context)

    def generate(
        self,
        query: str,
        text_context: List[str],
        tables: Dict[str, pd.DataFrame] = None,
        images: Dict[str, Dict] = None,
        max_length: int = 512,
        **kwargs
    ) -> str:

        try:
            context_parts = []
            cleaned_text = "".join(chunk.replace("•", "-").strip() for chunk in text_context)
            context_parts.append("Text Context:\n" + cleaned_text)

            
            if tables:
                context_parts.append("Table Context:\n" + self._format_table_context(tables))
                
            if images:
                context_parts.append("Image Context:\n" + self._format_image_context(images))
            full_context = "\n\n".join(context_parts)
            
            prompt = f"""You are an expert in nutrition and vitamins.
             Answer the question based on the following context about the history and definitions of vitamins.
            Context:
            {full_context}

            Question: {query}

            Provide a detailed and accurate answer, focusing on the history and definitions of vitamins. 
            If the context does not contain enough information, state that explicitly.
            Answer: """
            print("Prompt:", prompt)
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048  
            ).to(self.device)
            print("Tokenizer Inputs:", inputs)
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=150, 
                do_sample=True,
                temperature=0.9,    
                top_k=50,           
                top_p=0.95,         
                num_beams=4,
                no_repeat_ngram_size=2,
                early_stopping=False
            )
            print("Model Outputs:", outputs)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            return self.pipeline(
                prompt,
                max_length=max_length,
                **kwargs
            )[0]['generated_text']

    def format_answer_with_sources(
        self,
        answer: str,
        sources: Dict[str, Union[List[str], List[int]]]
    ) -> Dict:

        return {
            "answer": answer,
            "sources": {
                "text": sources.get("text_chunks", []),
                "tables": sources.get("tables", []),
                "images": sources.get("images", [])
            }
        }

