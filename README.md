
🌱 PlantCare AI – Organic Plant Disease Diagnosis & Guidance

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/flask-2.2-green)](https://flask.palletsprojects.com/)  
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📝 Project Overview

**PlantCare AI** is a web-based application that helps users **diagnose plant diseases using AI** and provides **organic solutions and guidance**.  
It also features a chatbot for agriculture-related questions.  

This project is perfect for **farmers, gardeners, and agriculture enthusiasts** aiming to maintain healthy plants using **sustainable and organic methods**.  

---

## 🌟 Key Features

- **👤 User Authentication**
  - Register, login, and logout.
  - Optional phone number storage for SMS alerts.

- **🖼️ Disease Diagnosis**
  - Upload plant images for AI-based disease detection.
  - Powered by **ResNet34** for accurate classification.
  - Store historical diagnoses for users.

- **📹 Live Camera Prediction**
  - Real-time detection using camera or base64 images.
  - Instant results with optional SMS notifications.

- **🌿 Organic Guidance**
  - Disease-specific solutions, guidance, and actionable steps.
  - Optional SMS notifications via Twilio.

- **💬 Agriculture Chatbot**
  - Powered by **DistilBERT** (Quantized ONNX model).
  - Handles FAQs about soil health, pest control, and crop care.
  - Provides disease-specific context-aware answers.

- **📜 History Management**
  - View, delete, or clear all past diagnoses.
  - Uploaded images and results stored securely.

---

## 🛠️ Tech Stack

| Component                  | Technology/Library                                |
|-----------------------------|--------------------------------------------------|
| Backend                     | Python, Flask, SQLAlchemy, Flask-Login          |
| AI Model                    | PyTorch, ResNet34, PIL                          |
| Chatbot                     | HuggingFace Transformers, ONNX Runtime          |
| SMS Notifications           | Twilio REST API                                 |
| Database                    | MySQL (default), fallback SQLite for local dev |
| Frontend                    | HTML, CSS, Bootstrap (Jinja2 Templates)        |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+  
- MySQL (or SQLite for testing)  
- Git  

### Clone Repository
```bash
git clone https://github.com/your-username/plantcare-ai.git
cd plantcare-ai
````

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_flask_secret_key
DATABASE_URL=mysql+mysqlconnector://username:password@localhost/organic_db
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

> ⚠️ **Never commit your `.env` file** to GitHub.

### Database Initialization

```python
from app import db, app
with app.app_context():
    db.create_all()
```

---

## 🚀 Running the Application

```bash
python app.py
```

* Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Usage Guide

1. **👤 Register/Login**

   * Create an account or log in to access disease diagnosis.

2. **🖼️ Upload Plant Image**

   * Navigate to **Upload → Choose Image → Submit**.
   * The system predicts the disease and displays organic treatment steps.

3. **📲 Receive SMS Notification (Optional)**

   * Enter your phone number in E.164 format (`+1234567890`).
   * SMS with disease info and solutions will be sent via Twilio.

4. **💬 Chatbot Assistance**

   * Navigate to **Chatbot** and ask agriculture questions.
   * Example questions:

     * "How to improve soil health?"
     * "How to prevent fungal diseases?"

5. **📜 View History**

   * Check all past diagnoses.
   * Delete specific or all entries as needed.

---

## 🗂️ Folder Structure

```
plantcare-ai/
│
├── app.py                   # Main Flask app
├── model.py                 # AI model & preprocessing
├── templates/               # HTML templates (Jinja2)
├── static/
│   └── uploads/             # Uploaded images
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚠️ Important Notes

* AI model weights are **not included**; train or download separately.
* SMS feature requires **Twilio credentials**.
* For local testing, SQLite can be used instead of MySQL.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit (`git commit -m "Description of changes"`)
5. Push (`git push origin feature-name`)
6. Open a Pull Request

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

* [Flask](https://flask.palletsprojects.com/) – Web framework
* [PyTorch](https://pytorch.org/) – Deep learning
* [HuggingFace Transformers](https://huggingface.co/transformers/) – NLP chatbot
* [Twilio](https://www.twilio.com/) – SMS integration


