import pandas as pd
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# 2024 12-month inflation data: see static/csv_files/Inflation_Rates.csv
inflation_data = [
    {'month': 'July', 'value': 4.31, 'date': '2024-07-01'},
    {'month': 'June', 'value': 6.22, 'date': '2024-06-01'},
    {'month': 'May', 'value': 5.10, 'date': '2024-05-01'},
    {'month': 'April', 'value': 5.00, 'date': '2024-04-01'},
    {'month': 'March', 'value': 5.70, 'date': '2024-03-01'},
    {'month': 'February', 'value': 6.31, 'date': '2024-02-01'},
    {'month': 'January', 'value': 6.85, 'date': '2024-01-01'},
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

    # Function to filter data based on period (5Y, 10Y, Full)
    def filter_data(data, period):
        if period == '5Y':
            return data[:6]  # Last 5 years of data
        elif period == '10Y':
            return data[:11]  # Last 10 years of data
        else:
            return data  # Full dataset

    # Fetch GDP data from 2010
    gdp_period = request.GET.get('gdp_period', 'full')
    gdp_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/NY.GDP.MKTP.CD?date=2010:2024&format=json'
    gdp_response = requests.get(gdp_url)
    if gdp_response.status_code == 200:
        gdp_data = gdp_response.json()[1] # the first index contains page details
        context['gdp_data'] = filter_data(gdp_data, gdp_period)

    # Fetch Population data from 2010
    pop_period = request.GET.get('pop_period', 'full')
    pop_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/SP.POP.TOTL?date=2010:2024&format=json'
    pop_response = requests.get(pop_url)
    if pop_response.status_code == 200:
        pop_data = pop_response.json()[1]
        context['pop_data'] = filter_data(pop_data, pop_period)

    # Fetch GDP per capita from 2010
    per_capita_period = request.GET.get('per_capita_period', 'full')
    per_capita_url = 'https://api.worldbank.org/v2/en/country/KE/indicator/NY.GDP.PCAP.CD?date=2010:2024&format=json'
    per_capita_response = requests.get(per_capita_url)
    if per_capita_response.status_code == 200:
        per_capita_data = per_capita_response.json()[1]
        context['per_capita_data'] = filter_data(per_capita_data, per_capita_period)

    # Fetch USD/KES exchange from 2019 to date
    exchange_period = request.GET.get('exchange_period', 'full')
    exchange_rates_file = 'static/csv_files/CBK_Indicative_Exchange_Rates.csv'
    exchange_rates_df = pd.read_csv(exchange_rates_file)

    usd_exchange_rates = exchange_rates_df[exchange_rates_df['Currency'] == 'US DOLLAR']
    usd_exchange_rates['Date'] = pd.to_datetime(usd_exchange_rates['Date'], format='%d/%m/%Y')
    usd_exchange_rates['Date'] = usd_exchange_rates['Date'].dt.strftime('%Y-%m-%d')

    usd_exchange_rates = usd_exchange_rates[['Date', 'Mean']].rename(columns={'Mean': 'Rate'})
    usd_exchange_rates = usd_exchange_rates.sort_values(by='Date')

    # Filtering Exchange Rates
    if exchange_period == '5Y':
        usd_exchange_rates = usd_exchange_rates
    elif exchange_period == '2Y':
        usd_exchange_rates = usd_exchange_rates.tail(496)
    elif exchange_period == 'YTD':
        usd_exchange_rates = usd_exchange_rates[usd_exchange_rates['Date'] >= f'{datetime.now().year}-01-01']
    elif exchange_period == '3M':
        usd_exchange_rates = usd_exchange_rates.tail(42)
    elif exchange_period == '1M':
        usd_exchange_rates = usd_exchange_rates.tail(2)

    context['exchange_rates'] = usd_exchange_rates.to_dict('records')

    # Inflation data for dashboard 3
    context['current_inflation'] = inflation_data[0]['value']
    context['previous_inflation'] = inflation_data[1]['value']

    return render(request, 'accounts/home.html', context)

def upgrade(request):
    """page users are prompted to become full members"""
    if request.user.is_authenticated and request.user.is_full_member:
        return redirect('macroeconomics:home')

    return render(request, 'macroeconomics/upgrade.html')

@login_required
def inflation_trend(request):
    """Displays dashboard for historical monthly inflation from January 2024 to date"""
    if not request.user.is_full_member:
        return redirect('macroeconomics:upgrade')
    
    # Get the filter period from the request, default is YTD
    period = request.GET.get('period', 'YTD')

    inflation_df = pd.DataFrame(inflation_data)
    inflation_df['date'] = pd.to_datetime(inflation_df['date'])

    # Determine the last available date which is in July
    last_date = inflation_df['date'].max()

    if period == '3M':
        start_date = last_date - pd.DateOffset(months=3)
        filtered_inflation_data = inflation_df[inflation_df['date'] >= start_date]
    elif period == '1M':
        start_date = last_date - pd.DateOffset(months=1)
        filtered_inflation_data = inflation_df[inflation_df['date'] >= start_date]
    else:  # YTD
        start_of_year = pd.to_datetime(f'{last_date.year}-01-01')
        filtered_inflation_data = inflation_df[inflation_df['date'] >= start_of_year]

    filtered_inflation_data['date'] = filtered_inflation_data['date'].dt.strftime('%Y-%m-%d')

    context = {
        'inflation_data': filtered_inflation_data.to_dict('records'),
        'selected_period': period
    }
    return render(request, 'macroeconomics/inflation_trend.html', context)

@login_required
def membership_upgrade(request):
    """redirects to Stripe checkout for full membership upgrade"""
    if request.user.is_full_member:
        messages.info(request, 'You are already a full member.')
        return redirect('macroeconomics:home')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if payment_method == 'stripe':
            return redirect('payments:stripe_checkout')
        elif payment_method == 'mpesa':
            return redirect('payments:mpesa_checkout')
        else:
            messages.error(request, 'Invalid payment method selected.')
            return redirect('macroeconomics:upgrade')
    
    return render(request, 'macroeconomics/membership_upgrade.html')