## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/izielin/students_app.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

```bash
python manage.py createsuperuser
```

The project will be available at **127.0.0.1:8000**.

