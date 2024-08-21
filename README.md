# Financial & Macroeconomics Analysis Platform
[![Python Version](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.1-brightgreen.svg)](https://www.djangoproject.com/download/)
[![Bootsrap Version](https://img.shields.io/badge/bootstrap-5.3-purple.svg)](https://getbootstrap.com/docs/5.3/)

![The_Analysis_Platform](https://github.com/am-derrick/F_n_M-Platform/blob/main/static/img/The_Analysis_Platform.png)

This Project is named `analysis_platform` and has for the start 4 apps:
1. `accounts`: containing relevant signup, login and account views and a custom user model.
2. `macroeconomics`: containing the views and relevant urls for the macroeconomic charts on GDP ,population, GDP per capita and inflation.
3. `financials`: containing the views and relevant urls for the financial analysis charts on SCOM data.
4. `payments`: containing the business logic for payment integration with [Stripe](https://stripe.com) and mobile money (currently supporting only [MPESA](https://developer.safaricom.co.ke/)).

## Demo

You can view the demo [here](https://youtu.be/2arRWqn2GeM).

View the deployed site on Digital Ocean [here](https://analysis-platform-5pdz9.ondigitalocean.app/accounts/login/).

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
The example involved assumes your environmental variables are saved in the ```.env.example``` file. Transfer them to a file named ```.env```. You'll need 5 keys;
- `STRIPE_PUBLIC_KEY` - can be found on your Stripe Dashboard.
- `STRIPE_SECRET_KEY`- can be found on your Stripe Dashboard.
- `SECRET_KEY` - Djanago's production secret key.
- `MPESA_SECRET_KEY` - can be found on your Safricom Developer Dashbaord when you create a new app.
- `MPESA_CONSUMER_KEY` - can be found on your Safricom Developer Dashbaord.

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
