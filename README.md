# Zoo Feed

Zoo Feed is a Django pet shop project with a product catalog, brand segmentation, product pages, filters, cart, and seeded demo data.

## Features

- Home page with slider and category navigation
- Categories: `dog_food`, `cat_food`, `wet_food`, `care_and_hygiene`
- Brand segmentation: economy, premium, super premium
- Product list with filters and price range
- Product detail pages with packing options
- Session-based shopping cart
- Admin panel
- Catalog seed commands

## Stack

- Python
- Django
- SQLite for local development
- HTML, CSS, JavaScript
- Pillow
- python-dotenv

## Requirements

The project uses the root [requirements.txt](/abs/c:/Users/DimaW/Desktop/Zoo_Feed/requirements.txt).

Current dependencies:

```text
asgiref==3.11.1
Django==6.0.4
dotenv==0.9.9
pillow==12.2.0
python-dotenv==1.2.2
sqlparse==0.5.5
tzdata==2026.1
```

## Project Structure

```text
Zoo_Feed/
|-- README.md
|-- requirements.txt
|-- zoo_feed/
|   |-- manage.py
|   |-- db.sqlite3
|   |-- media/
|   |-- zoo_feed/
|   |   |-- settings.py
|   |   |-- urls.py
|   |   `-- ...
|   `-- shop_app/
|       |-- models.py
|       |-- views.py
|       |-- templates/
|       |-- static/
|       `-- management/commands/
```

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd Zoo_Feed
```

2. Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

3. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Environment Variables

For local development the project can run without a custom `.env`, but email sending and production DB settings use environment variables.

Create a `.env` file inside `zoo_feed/` if needed:

```env
ENV=development
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DB_PASSWORD=your_production_db_password
```

Behavior:

- `ENV=development` uses SQLite
- any other `ENV` value switches settings to the MySQL production config from [settings.py](/abs/c:/Users/DimaW/Desktop/Zoo_Feed/zoo_feed/zoo_feed/settings.py)

## Run the Project

From the Django project folder:

```bash
cd zoo_feed
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Seed the Catalog

The project includes management commands for catalog filling.

Seed with real brands and products:

```bash
python manage.py seed_real_catalog
```

Seed demo catalog:

```bash
python manage.py seed_demo_catalog
```

## Admin Panel

The admin URL is customized in [urls.py](/abs/c:/Users/DimaW/Desktop/Zoo_Feed/zoo_feed/zoo_feed/urls.py).

Admin route:

```text
/5QH8GD4F4aBKkTacuWZc8dL54cSVzAtl/
```

Create a superuser:

```bash
python manage.py createsuperuser
```

## Useful Commands

Apply migrations:

```bash
python manage.py migrate
```

Create new migrations:

```bash
python manage.py makemigrations
```

Run local server:

```bash
python manage.py runserver
```

## Data Storage

- SQLite database: `zoo_feed/db.sqlite3`
- media files: `zoo_feed/media/`
- static files: `zoo_feed/shop_app/static/`

## Notes

- The repository already contains a local SQLite database
- Media files are served automatically in development when `DEBUG=True`
- The cart works through Django session storage
- After seeding, product images and brand logos are stored in `media/`
