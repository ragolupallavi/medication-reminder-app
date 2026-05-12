# 💊 Medication Reminder App

A **Streamlit-based Medication Reminder System** that helps users manage their daily medicines with:

- User Authentication (Login / Signup)
- Add and manage medications
- Email reminders using Gmail SMTP
- Mark medicines as taken
- Delete medications
- Dashboard with medication statistics
- Secure deployment using Streamlit Secrets

---

## 🚀 Features

### 🔐 Authentication
- User Registration
- Secure Login System
- Session Management
- Logout functionality

### 💊 Medication Management
- Add medication name
- Add dosage
- Set reminder time
- View all medications
- Delete medication
- Mark medicine as taken

### 📧 Email Notifications
- Sends automatic reminder emails
- Uses Gmail App Password
- Secure credential storage with Streamlit Secrets

### 📊 Dashboard Metrics
- Total medications
- Taken medications
- Pending medications

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**
- **SMTP (Email Service)**

---

## 📂 Project Structure

```plaintext
medication-reminder/
│
├── app.py
├── database.py
├── auth.py
├── medication.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/medication-reminder.git
cd medication-reminder
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run app:

```bash
streamlit run app.py
```

---

## 🔑 Streamlit Secrets Setup

Create:

```plaintext
.streamlit/secrets.toml
```

Add:

```toml
EMAIL = "yourgmail@gmail.com"
PASSWORD = "your_16_digit_gmail_app_password"
```

---

## 📌 Gmail App Password Setup

1. Enable **2-Step Verification**
2. Visit Google App Passwords
3. Generate App Password
4. Add it to `secrets.toml`

---

## 🌐 Deployment

Deploy easily using Streamlit Community Cloud:

1. Push project to GitHub
2. Connect GitHub repo to Streamlit Cloud
3. Add Secrets
4. Deploy

---

## 📷 Screenshots

<img width="1597" height="917" alt="image" src="https://github.com/user-attachments/assets/ff0895a7-9702-4279-af3b-4faf263f3ef3" />


---

## 👩‍💻 Author

**Pallavi**

---
