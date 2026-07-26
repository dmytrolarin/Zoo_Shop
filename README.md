# Zoo Feed

Zoo Feed is a Django-based e-commerce application for a pet store. It features a product catalog, category and brand navigation, advanced product filtering, shopping cart functionality, and a customized Django admin interface.

---

## Features

- Product catalog
- Category and brand navigation
- Brand segmentation
- Advanced product filtering
- Product detail pages
- Session-based shopping cart
- Customized Django admin interface

---

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Pillow

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Zoo_Feed
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows CMD**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

For local development the project uses SQLite by default.

If you want to use production settings, create a `.env` file inside the `zoo_feed/` directory:

```env
ENV=development

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

DB_PASSWORD=your_database_password
```

- `ENV=development` uses SQLite.
- Any other value uses the production MySQL configuration.

---

## Run the Project

```bash
cd zoo_feed
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Demo Data

The repository includes a preconfigured SQLite database with demo data and the required media files, allowing the project to run immediately after setup.

---

## Development Note

This repository is a portfolio version of the original project, which was initially developed in a separate private repository.

Before publication, the project was cleaned up and reorganized for public presentation. AI tools were used only for documentation, comment translation, and code formatting. The application logic and core functionality were implemented independently.