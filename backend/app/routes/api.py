from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import db
from app.database.models import User, Conversation, Message
from app.data_processing.pdf_processor import PDFProcessor
from app.models.retriever import Retriever
from app.config import Config
import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)


def handle_error(message, status_code):
    logger.error(f"Error: {message}")
    return jsonify({"error": message}), status_code


@api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return handle_error("Username and password are required", 400)

        if User.query.filter_by(username=username).first():
            return handle_error("Username already exists", 400)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return handle_error(str(e), 500)


@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return handle_error("Username and password are required", 400)

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return handle_error("Invalid username or password", 401)

        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return handle_error(str(e), 500)


@api.route('/upload', methods=['POST'])
@jwt_required()
def upload_pdf():
    try:
        if 'file' not in request.files:
            return handle_error("No file uploaded", 400)

        file = request.files['file']
        if file.filename == '':
            return handle_error("Empty filename", 400)

        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        upload_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        file.save(upload_path)

        processor = PDFProcessor(upload_path)
        text_chunks = processor.extract_text()
        tables = processor.extract_tables()
        images = processor.process_images()

        retriever = Retriever()
        retriever.add_documents(text_chunks)

        return jsonify({
            "message": "PDF processed successfully",
            "tables": list(tables.keys()),
            "images": list(images.keys())
        }), 200
    except Exception as e:
        return handle_error(str(e), 500)


@api.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message')
        if not user_input:
            return handle_error("No message provided", 400)

        retriever = Retriever()
        text_indices = retriever.retrieve(user_input)

        if not text_indices:
            return handle_error("No relevant documents found", 404)

        relevant_texts = [retriever.documents[i] for i in text_indices]
        
        from app.models.generator import Generator
        generator = Generator()
        context = "\n".join(relevant_texts)
        response = generator.generate(user_input, context)

        user = User.query.filter_by(username=get_jwt_identity()).first()
        if not user:
            return handle_error("User not found", 404)

        conv = Conversation(user_id=user.id)
        db.session.add(conv)

        user_msg = Message(content=user_input, conversation=conv)
        bot_msg = Message(content=response, conversation=conv, is_bot=True)
        db.session.add_all([user_msg, bot_msg])
        db.session.commit()

        return jsonify({
            "response": response,
            "conversation_id": conv.id
        }), 200
    except Exception as e:
        return handle_error(str(e), 500)
