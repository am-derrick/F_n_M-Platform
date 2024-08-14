# Financial & Macroeconomics Analysis Platform
[![Python Version](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.1-brightgreen.svg)](https://www.djangoproject.com/download/)

![The_Analysis_Platform](https://github.com/am-derrick/F_n_M-Platform/blob/main/static/img/The_Analysis_Platform.png)

## Demo



## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone git@github.com:am-derrick/F_n_M-Platform.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Setup the local configurations:
The example involved assumes your environmental variables are saved in the ```.env.example``` file. Transfer them to a file named ```.env```. You'll need 3 keys;
- `STRIPE_PUBLIC_KEY` - can be found on your Stripe Dashboard
- `STRIPE_SECRET_KEY`- can be found on your Stripe Dashboard
- `SECRET_KEY` - Djanago's production secret key

```bash
cp .env.example .env
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.
