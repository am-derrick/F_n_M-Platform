import requests
from django.shortcuts import render

def home(request):
    """Displays charts showing the first three macroeconomic
    datapoints on GDP and population on the hoome page.
    More information about the World Bank API can be found here
    https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
    """

    context = {
        'gdp_data': [],
        'pop_data': [],
        'per_capita_data': [],
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

    return render(request, 'home.html', context)