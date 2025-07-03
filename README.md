# 🔐 Movie List — Make a Movie List, Signup, Password Reset

A beginner-friendly Flask web application that allows users to:

- ✅ Register (Sign Up)
- ✅ Make their own list of movies (add and remdeleteove)
- ✅ Reset their password securely via email


---

## ✨ Features

- 📝 User Registration (Signup)
- 🎬 Maintain a movie list
- 🗝️ API usage to search movies `TMDB`
- 💾 CRUD operations in database `SQLAlchemy` 
- 📧 Forgot Password via Email
- 🔑 Secure, time-limited reset tokens using `itsdangerous`
- 📬 Email integration using Gmail SMTP and Flask-Mail
- 💡 Simple, modular structure and templates for easy editing


---

## 🧰 Tech Stack

- Python
- Flask
- SQLAlchemy
- HTML (Jinja templates)
- Bootstrap
- CSS
- Flask-Mail
- itsdangerous


---

## 📁 Folder Structure

movie-list/
│
├── app.py # Main Flask application file
├── requirements.txt # Python dependencies
└── templates/ # HTML templates (Jinja2)
├── footer.html
├── forgot.html
├── header.html
├── home.html
├── login.html
├── message.html
├── moviecheck.html
├── reset-password.html
├── signup.html
├── success.html
├── watched.html
└── watchlist.html
└── instance/ # Database (SQLAlchemy)
├── data.db
---

## 🚀 Getting Started

### 🔁 1. Clone the Repository

```bash
git clone https://github.com/sutanudutta15/movie-list.git
cd movie-list
```
🐍 2. Create Virtual Environment (optional)
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```
📦 3. Install Dependencies
```
pip install -r requirements.txt
```

📧 Email Configuration
```bash
This app uses Gmail SMTP to send password reset links.


🔐 Step 1: Generate Gmail App Password
Go to https://myaccount.google.com/apppasswords

Enable 2-Step Verification if not already enabled.

Generate an App Password for "Mail".

Use that password in your Flask app configuration.

✍️ Step 2: Set Email Config in app.py
Edit the following lines in app.py:

app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
```

🔌API configuration
```bash
✅ Step-by-Step Guide:
1. Go to the TMDB Website
    Open your browser and visit:
    👉 https://www.themoviedb.org

2. Sign Up / Log In

    If you do not have an account, click "Join TMDB" to create one.
    
    If you already have an account, simply log in.

3. Access Your Profile Settings

    Once logged in, click your profile avatar in the top-right corner.
    
    Select "Settings" from the dropdown menu.

4. Navigate to the API Section

    In the left sidebar, click on "API".

5. Apply for an API Key

    Scroll down to the API Key Request section.
    
    Click the "Create" or "Request an API Key" button.

6. Fill Out the Application Form

    You will be asked some basic questions like:
    
    App name and purpose
    
    Intended usage (education, development, etc.)
    
    Fill them honestly and submit.

7. Choose the Right Key Type

    For most personal or development uses, a "Developer" or "Personal" key will be sufficient.

8. Wait for Approval (If Required)

    In most cases, the API key is generated immediately.
    
    If manual review is needed, it might take some time.

9. Copy Your API Key

    Once generated, you will see your API key listed.
    
    Copy this key and store it securely.


Edit the following line in app.py:


API_KEY = "your_api_key"
```


▶️ Run the App
```bash
python app.py

Visit http://localhost:5000 in your browser.
```

## Tutorial
```bash
https://drive.google.com/file/d/1v6MqR6pSHhO134zWIGYltt0W6yJiShDZ/view
```