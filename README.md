# FindYourGuide

## Setting Up and Running the Project

### Prerequisites

1. **Python:**
   - Ensure Python is installed on your machine. If not, download and install it from [Python Official Website](https://www.python.org/).

2. **Virtual Environment:**
   - It's recommended to use a virtual environment to isolate project dependencies.
     ```bash
     # Create a virtual environment
     python -m venv venv

     # Activate the virtual environment
     source venv/bin/activate  # On Unix-based systems
     .\venv\Scripts\activate  # On Windows
     ```

3. **Install Dependencies:**
   - Install Django using pip within your virtual environment.
     ```bash
     pip install django
     pip install pillow
     pip install stripe
     ```

4. **Configure:**
     ```bash
     python manage.py migrate
     # To access admin site
     python manage.py createsuperuser
     ```

5. **Run Server:**
     ```bash
    python manage.py runserver
     ```
