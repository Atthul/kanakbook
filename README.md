KanakBook
KanakBook is a responsive, mobile-friendly web application that helps you track your income, expenses, and balances (both Cash and UPI) securely.
Built with Django, it provides insightful summaries and helps you stay in control of your money.

✨ Features
Track income and expenses with detailed records

Separate balance tracking for Cash and UPI

Responsive design — works seamlessly on desktop and mobile

Clean, intuitive user interface

Built with Django’s robust and secure framework

🛠️ Tech Stack
Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap

Database: SQLite (default)

🚀 Getting Started
📥 Clone the repository
bash
Copy
Edit
git clone https://github.com/Atthul/kanakbook.git
cd kanakbook
📦 Install dependencies
It’s recommended to use a virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Linux/Mac

pip install -r requirements.txt
If requirements.txt is missing, just install Django:

bash
Copy
Edit
pip install django
🛠️ Apply migrations
bash
Copy
Edit
python manage.py migrate
🧪 Run the development server
bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

📂 Project Structure
csharp
Copy
Edit
expense_tracker/
├── expense_tracker/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── …
├── kanakbook/             # Main app
│   ├── models.py
│   ├── views.py
│   └── …
├── templates/             # HTML templates
├── static/                # CSS/JS/static assets
├── db.sqlite3             # Database file
├── manage.py
└── README.md
🧾 License
This project is licensed under the MIT License.
