import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")
    SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL")
    GENERATOR_MODEL =  os.getenv("GENERATOR_MODEL","google/flan-t5-small")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER","uploads")
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")