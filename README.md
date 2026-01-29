# 🏋️ IronLife Gym Manager

**IronLife Gym Manager** is a robust, full-stack web application engineered to modernize fitness center administration. By transitioning from manual paper-based records to a centralized digital platform, it reduces administrative overhead by approximately 60% and eliminates risks associated with manual data entry.

## 👨‍💻 Project Information
* **Developer:** Yaseen Ahmad
* **Institution:** Software Engineering Student at CECOS University
* **Instructor:** Muhammad Ejaz
* **Date:** January 29, 2026

---

## ✨ System Features

### 🖥️ Presentation Layer (Frontend)
* **Modern Dark UI:** A high-performance interface utilizing glass-morphism effects and energetic red accents (`#ef4444`) for a premium user experience.
* **Responsive Architecture:** Built with a "Mobile-First" approach; the sidebar collapses into a hamburger menu on screens smaller than 768px.
* **Real-time Dashboard:** Instant insights into total members, active counts, and monthly revenue tracking.
* **Member Management:** Full CRUD (Create, Read, Update, Delete) capabilities with real-time search and filtering.
* **Offline Capability:** Leverages browser localStorage to cache data, ensuring accessibility even during network interruptions.

### ⚙️ Application & Data Layer (Backend)
* **RESTful API:** Clean separation of concerns using Python Flask to process logic and serve JSON endpoints.
* **Secure Gateway:** Authentication gateway to ensure only authorized personnel can access sensitive data.
* **Relational Storage:** Persistent management using SQLite with SQLAlchemy ORM to ensure data integrity.
* **Automated Logic:** Intelligent calculation of membership validity dates and fee structures.



---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | HTML5, CSS3 |
| **Frontend Logic** | JavaScript (ES6+) |
| **Backend Framework** | Python 3.8+, Flask 3.0 |
| **ORM / Database** | SQLAlchemy 2.0 / SQLite |
| **Icons & Fonts** | Font Awesome 6.4, Teko, Roboto |

---

## 📂 Repository Structure
```plaintext
├── app.py                # Flask Backend, API Endpoints & Database Models
├── gym-manager.html      # Main Application User Interface
├── index.html            # Landing / Start Page
├── style.css             # Custom CSS with Dark Theme & Glass-morphism
├── script.js             # Frontend Logic, API Interaction & State Management
├── requirements.txt      # Python Package Dependencies
└── gym_manager.db        # SQLite Database (Automatically generated on run)


📊 Database Schema
The system manages three primary entities:

User: Stores administrator credentials and roles.

Member: Manages client details, membership plans (Basic, Pro, Elite), and registration dates.

Payment: Tracks financial transactions linked to members.

🚀 Installation & Execution
1. Prerequisites
Python 3.8+ installed.

pip (Python package manager).

A modern web browser.

2. Deployment Steps
Step 1: Clone the repository

Bash

git clone https://github.com/MrYaseen0/IronLife-Gym-Manager-by-Yaseen-Ahmad.git
cd ironlife-gym-manager

Step 2: Install dependencies

Bash

pip install -r requirements.txt

Step 3: Start the Backend server

Bash
python app.py
The backend will initialize the database and run at http://localhost:5000.

Step 4: Launch the Interface
Open index.html or gym-manager.html directly in your browser.

🔐 Demo Credentials
Username: admin

Password: 123456

🛠️ Troubleshooting
Port Conflict: If the backend fails to start, verify that port 5000 is not being used by another application.

Database Reset: To clear all records, delete gym_manager.db and restart app.py.

API Connectivity: Ensure the Flask backend is running to allow the frontend to fetch and save data.

📜 License
This project was developed for educational purposes at CECOS University.
