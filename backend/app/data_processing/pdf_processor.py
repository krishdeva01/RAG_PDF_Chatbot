import pdfplumber
import camelot
import pytesseract
from PIL import Image
import cv2
import os
from transformers import BlipProcessor, BlipForConditionalGeneration

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_chunks = []
        self.tables = {}
        self.image_data = {}

        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def extract_text(self, chunk_size=512):
        with pdfplumber.open(self.file_path) as pdf:
            full_text = "\n".join([page.extract_text() for page in pdf.pages])
            
        self.text_chunks = [full_text[i:i+chunk_size] 
                           for i in range(0, len(full_text), chunk_size)]
        return self.text_chunks

    def extract_tables(self):
        tables = camelot.read_pdf(self.file_path, flavor="stream")
        self.tables = {f"table_{i}": table.df.to_dict() 
                      for i, table in enumerate(tables)}
        return self.tables

    def process_images(self):
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                images = page.images
                for img_num, img in enumerate(images):
                    img_obj = page.to_image(resolution=300)
                    img_path = f"images/page_{page_num}_img_{img_num}.png"
                    img_obj.save(img_path)
                    
                    image = cv2.imread(img_path)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    text = pytesseract.image_to_string(gray)
                    self.image_data[img_path] = {
                        "text": text,
                        "caption": self._generate_image_caption(image)
                    }
        return self.image_data

    def _generate_image_caption(self, image):
        inputs = self.blip_processor(image, return_tensors="pt")
        outputs = self.blip_model.generate(**inputs, max_new_tokens=100)
        return self.blip_processor.decode(outputs[0], skip_special_tokens=True)