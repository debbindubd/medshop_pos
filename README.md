# Medical Shop POS System

A Point of Sale system for medical shops built with Django, SQLite, Tailwind CSS, Bootstrap, and JavaScript.

## Features

- User authentication and role-based access
- Dashboard with sales statistics and quick actions
- Inventory management (add medicines, manage stock)
- POS interface for quick sales processing
- Sales history and detailed sale records
- Stock tracking with expiry date monitoring
- Low stock and expired medicine alerts

## Tech Stack

- **Backend:** Django 
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **CSS Frameworks:** Bootstrap, Tailwind CSS 
- **Icons:** Font Awesome

## Project Structure

- `medshop_pos/` - Main project directory
  - `medshop_pos/` - Django project settings
  - `pos/` - Django app for POS functionality
  - `static/` - Static files (CSS, JS)
  - `templates/` - HTML templates
  - `manage.py` - Django management script

## Models

- **Category** - Medicine categories
- **Medicine** - Medicine information and pricing
- **Stock** - Inventory tracking with batches and expiry dates
- **Sale** - Sales transaction records
- **SaleItem** - Individual items in a sales transaction

## Setup Instructions

1. Install dependencies:
   ```
   pip install django
   ```

2. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   For demonstration purposes, you can use:
   ```
   python simulate_migrations.py
   ```

3. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
   
   For demonstration purposes, you can use:
   ```
   python create_superuser.py
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```
   
   For demonstration purposes, you can use:
   ```
   python simulate_server.py
   ```

5. Access the admin interface at `/admin` to add initial categories and medicines.
   
   For demonstration purposes, you can use:
   ```
   python add_sample_data.py
   ```

## Usage

1. Log in with your user credentials
2. Use the dashboard to navigate to different sections
3. Add medicines and stock through the inventory management
4. Process sales through the POS interface
5. View sales history and details

## Screenshots

(Screenshots will be added here)

## License

This project is licensed under the MIT License.# medshop_pos
