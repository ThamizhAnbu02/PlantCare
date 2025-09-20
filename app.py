import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import torch
import re
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import model  # Import the ResNet34 model
from transformers import pipeline
from optimum.onnxruntime import ORTModelForQuestionAnswering

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://plantcare_user:1234@localhost/organic_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_Account_SID"
TWILIO_AUTH_TOKEN = "your twilio authentication code"
TWILIO_PHONE_NUMBER = "your phone no"
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    organic_solution = db.Column(db.Text)
    guidance = db.Column(db.Text)
    possible_steps = db.Column(db.Text)

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))
    confidence = db.Column(db.Float)
    image_path = db.Column(db.String(255))
    diagnosis_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='diagnoses')
    disease = db.relationship('Disease', backref='diagnoses')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize AI Chatbot (Quantized DistilBERT)
try:
    qa_pipeline = pipeline(
        "question-answering",
        model=ORTModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-finetuned-squad", export=True),
        tokenizer="distilbert-base-uncased-finetuned-squad",
        use_safetensors=True
    )
except Exception as e:
    print(f"Error loading chatbot model: {str(e)}")
    qa_pipeline = None

# Agriculture-specific FAQs
AGRI_FAQS = {
    "how to improve soil health": "To improve soil health, use organic compost, rotate crops, and avoid chemical fertilizers. Cover crops like clover can enhance soil fertility.",
    "best organic pest control": "Use neem oil, diatomaceous earth, or introduce beneficial insects like ladybugs. Companion planting with marigolds can deter pests.",
    "how to prevent fungal diseases": "Ensure proper plant spacing, avoid overhead watering, and apply organic fungicides like copper-based solutions."
}

def predict_disease(image_path):
    try:
        # Use the predict_image function from model.py
        prediction = model.predict_image(image_path)
        # Get the index of the predicted class
        class_index = model.num_classes.index(prediction)
        # Calculate confidence
        image = Image.open(image_path)
        tensor = model.transform(image)
        xb = tensor.unsqueeze(0)
        with torch.no_grad():
            yb = model.model(xb)
            probabilities = torch.softmax(yb, dim=1)
            confidence = float(probabilities[0][class_index]) * 100
        return class_index, confidence
    except Exception as e:
        flash(f"Error processing image: {str(e)}", "danger")
        return None, None

def send_sms(to_number, disease_name, solution, guidance):
    try:
        message_body = (
            f"PlantCare Diagnosis:\n"
            f"Disease: {disease_name}\n"
            f"Organic Solution: {solution}\n"
            f"Guidance: {guidance}"
        )[:1600]
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return True, message.sid
    except TwilioRestException as e:
        return False, str(e)

def get_agri_response(question):
    question = question.lower().strip()
    
    # Check FAQs first
    for faq, answer in AGRI_FAQS.items():
        if faq in question:
            return answer
    
    # Query Disease table for disease-specific information
    diseases = Disease.query.all()
    for disease in diseases:
        if disease.disease_name.lower() in question:
            context = (
                f"{disease.description} Organic Solution: {disease.organic_solution} "
                f"Guidance: {disease.guidance} Possible Steps: {disease.possible_steps}"
            )
            if qa_pipeline:
                result = qa_pipeline(question=question, context=context)
                return result['answer']
            else:
                return (
                    f"{disease.disease_name}:\n"
                    f"Description: {disease.description}\n"
                    f"Organic Solution: {disease.organic_solution}\n"
                    f"Possible Steps: {disease.possible_steps}\n"
                    f"Guidance: {disease.guidance}"
                )
    
    # Fallback for general agriculture questions
    if qa_pipeline:
        general_context = (
            "Organic farming focuses on sustainable practices, avoiding synthetic chemicals, and promoting biodiversity. "
            "Common practices include crop rotation, composting, and using natural pest control methods like neem oil."
        )
        result = qa_pipeline(question=question, context=general_context)
        if result['score'] > 0.5:  # Confidence threshold
            return result['answer']
    
    return "Sorry, I couldn't find specific information. Try asking about a plant disease, organic farming, or crop care tips."

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('upload'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form.get('phone', '')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        elif phone and not re.match(r'^\+\d{10,15}$', phone):
            flash('Invalid phone number format. Use E.164 (e.g., +1234567890)', 'danger')
        else:
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password_hash=password_hash, phone_number=phone)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@app.route('/predict')
@login_required
def predict():
    return render_template('predict.html')

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    if 'image' not in request.files:
        flash('No image uploaded', 'danger')
        return redirect(url_for('predict'))
    image = request.files['image']
    if image.filename == '':
        flash('No image selected', 'danger')
        return redirect(url_for('predict'))
    if image and image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename = f"{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(file_path)
        index, confidence = predict_disease(file_path)
        if index is not None:
            # Map index to disease_id (assuming Disease table IDs start at 1 and match num_classes order)
            disease = Disease.query.get(int(index + 1))
            if disease:
                phone = request.form.get('phone')
                if phone and re.match(r'^\+\d{10,15}$', phone):
                    current_user.phone_number = phone
                    db.session.commit()
                diagnosis = Diagnosis(
                    user_id=current_user.id,
                    disease_id=disease.id,
                    confidence=confidence,
                    image_path=file_path
                )
                db.session.add(diagnosis)
                db.session.commit()
                if current_user.phone_number:
                    success, result = send_sms(
                        current_user.phone_number,
                        disease.disease_name,
                        disease.organic_solution,
                        disease.guidance
                    )
                    if success:
                        flash('Diagnosis successful! SMS sent.', 'success')
                    else:
                        flash(f'SMS failed: {result}', 'warning')
                return render_template('result.html',
                                      image_url=file_path,
                                      disease=disease.disease_name,
                                      description=disease.description,
                                      solution=disease.organic_solution,
                                      guidance=disease.guidance,
                                      possible_steps=disease.possible_steps,
                                      source="PlantCare Database",
                                      confidence=confidence)
        flash('Unable to identify disease', 'danger')
    else:
        flash('Invalid file format. Please upload a PNG, JPG, or JPEG image.', 'danger')
    return redirect(url_for('predict'))

@app.route('/history')
@login_required
def history():
    diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).order_by(Diagnosis.diagnosis_date.desc()).all()
    history_data = [
        (
            d.disease.disease_name,
            d.confidence,
            d.image_path,
            d.diagnosis_date,
            d.disease.organic_solution,
            d.disease.guidance,
            d.id
        )
        for d in diagnoses
    ]
    return render_template('history.html', history=history_data)

@app.route('/delete_diagnosis/<int:id>', methods=['POST'])
@login_required
def delete_diagnosis(id):
    diagnosis = Diagnosis.query.get_or_404(id)
    if diagnosis.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('history'))
    try:
        os.remove(diagnosis.image_path)  # Delete image file
    except OSError:
        pass  # Ignore if file doesn't exist
    db.session.delete(diagnosis)
    db.session.commit()
    flash('Diagnosis deleted successfully', 'success')
    return redirect(url_for('history'))

@app.route('/delete_all_diagnoses', methods=['POST'])
@login_required
def delete_all_diagnoses():
    diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).all()
    for diagnosis in diagnoses:
        try:
            os.remove(diagnosis.image_path)  # Delete image file
        except OSError:
            pass
        db.session.delete(diagnosis)
    db.session.commit()
    flash('All diagnoses deleted successfully', 'success')
    return redirect(url_for('history'))

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if request.method == 'POST':
        message = request.form['message']
        response = get_agri_response(message)
        return render_template('chatbot.html', message=message, response=response)
    return render_template('chatbot.html')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
