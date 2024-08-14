import pandas as pd
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib import messages

# 2024 12-month inflation data: see static/csv_files/Inflation_Rates.csv
inflation_data = [
    {'month': 'July', 'value': 4.31},
    {'month': 'June', 'value': 6.22},
    {'month': 'May', 'value': 5.10},
    {'month': 'April', 'value': 5.00},
    {'month': 'March', 'value': 5.70},
    {'month': 'February', 'value': 6.31},
    {'month': 'January', 'value': 6.85},
]

def home(request):
    """Displays charts showing the macroeconomic
    datapoints on GDP, population, GDP per capita, USD/KES exchange rate and inflation rates on the home page.
    More information about the World Bank API can be found here
    https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
    """

    context = {
        'gdp_data': [],
        'pop_data': [],
        'per_capita_data': [],
        'exchange_rates': [],
        'current_inflation': [],
        'previous_inflation': [],
    }

    # Fetch GDP data from 2010
    gdp_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/NY.GDP.MKTP.CD?date=2010:2024&format=json'
    gdp_response = requests.get(gdp_url)
    if gdp_response.status_code == 200:
        gdp_data = gdp_response.json()[1] # the first index contains page details
        context['gdp_data'] = gdp_data

    # Fetch Population data from 2010
    pop_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/SP.POP.TOTL?date=2010:2024&format=json'
    pop_response = requests.get(pop_url)
    if pop_response.status_code == 200:
        pop_data = pop_response.json()[1]
        context['pop_data'] = pop_data

    # Fetch GDP per capita from 2010
    per_capita_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/NY.GDP.PCAP.CD?date=2010:2024&format=json'
    per_capita_response = requests.get(per_capita_url)
    if per_capita_response.status_code == 200:
        per_capita_data = per_capita_response.json()[1]
        context['per_capita_data'] = per_capita_data

    # Fetch USD/KES exchange from 2019 to date
    exchange_rates_file = 'static/csv_files/CBK_Indicative_Exchange_Rates.csv'
    exchange_rates_df = pd.read_csv(exchange_rates_file)

    usd_exchange_rates = exchange_rates_df[exchange_rates_df['Currency'] == 'US DOLLAR']
    usd_exchange_rates['Date'] = pd.to_datetime(usd_exchange_rates['Date'], format='%d/%m/%Y')
    usd_exchange_rates['Date'] = usd_exchange_rates['Date'].dt.strftime('%Y-%m-%d')

    usd_exchange_rates = usd_exchange_rates[['Date', 'Mean']].rename(columns={'Mean': 'Rate'})
    usd_exchange_rates = usd_exchange_rates.sort_values(by='Date') # sort date

    exchange_rates_list = usd_exchange_rates.to_dict('records')
    context['exchange_rates'] = exchange_rates_list

    context['current_inflation'] = inflation_data[0]['value']
    context['previous_inflation'] = inflation_data[1]['value']

    return render(request, 'accounts/home.html', context)

@login_required
def inflation_trend(request):
    """Displays dashboard for historical monthly inflation from January 2024 to date"""
    if not request.user.is_full_member:
        return redirect('upgrade')
    
    context = {
        'inflation_data': inflation_data,
    }

    return render(request, 'macroeconomics/inflation_trend.html', context)

def upgrade(request):
    """page users are prompted to become full members"""
    return render(request, 'macroeconomics/upgrade.html')

@login_required
def membership_upgrade(request):
    """processes upgrading users to full membership"""
    user = request.user
    if user.is_full_member:
        messages.info(request, 'You are already a full member.')
        return redirect('macroeconomics:home')
    
    if request.method == 'POST':
        user.is_full_member = True
        user.save()

        messages.success(request, 'Congrats! You are now a full member.')
        return redirect('macroeconomics:home')
    
    return render(request, 'macroeconomics/membership_upgrade.html')