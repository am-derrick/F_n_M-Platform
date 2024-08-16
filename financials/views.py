from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import JsonResponse

file_path = 'static/csv_files/SCOMHistoricalPrices[June_to_Aug].csv'
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# Page 1 from July 2024 to Date
page1_data = df[df['Date'] >= '2024-07-01']

# Strip whitespace from column names
page1_data.columns = page1_data.columns.str.strip()

# Convert the 'Date' column to strings in 'YYYY-MM-DD' format
page1_data['Date'] = page1_data['Date'].dt.strftime('%Y-%m-%d')

# Page 2 from June 2024 to Date
page2_data = df[df['Date'] >= '2024-06-01']
page2_data.columns = page1_data.columns.str.strip()
page2_data['Date'] = page2_data['Date'].dt.strftime('%Y-%m-%d')

def financial_analysis_1(request):
    """view for page 1 of the financial analysis tab showing SCOM data
    from July 1 2024 to date"""
    # Get the filter period from the request, default is 2M
    period = request.GET.get('period', '2M')

    # Convert 'Date' back to datetime for filtering
    page1_data['Date'] = pd.to_datetime(page1_data['Date'])

    # Filter the data based on the selected period
    if period == '2M':
        filtered1_data = page1_data[page1_data['Date'] >= (pd.to_datetime('today') - pd.DateOffset(months=2))]
    elif period == '5D':
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.DateOffset(days=9)  # Offset to handle weekends and public holidays
        filtered1_data = page1_data[(page1_data['Date'] >= start_date) & (page1_data['Date'] <= end_date)]
    else:
        filtered1_data = page1_data

    # Convert 'Date' back to string for JSON serialization
    filtered1_data['Date'] = filtered1_data['Date'].dt.strftime('%Y-%m-%d')

    context = {
        'safaricom_data': filtered1_data.to_dict('records'),
        'selected_period': period
    }
    return render(request, 'financials/page1.html', context)

@login_required
def financial_analysis_2(request):
    """view for page 1 of the financial analysis tab showing SCOM data
    from June 1 2024 to date"""
    if not request.user.is_full_member:
        return redirect('macroeconomics:upgrade')
    
    # Get the filter period from the request, default is 3M
    period = request.GET.get('period', '3M')

    page2_data['Date'] = pd.to_datetime(page2_data['Date'])

    if period == '3M':
        filtered2_data = page2_data[page2_data['Date'] >= (pd.to_datetime('today') - pd.DateOffset(months=3))]
    elif period == '1M':
        filtered2_data = page2_data[page2_data['Date'] >= (pd.to_datetime('today') - pd.DateOffset(months=1))]
    elif period == '5D':
        end_date = pd.to_datetime('today')
        start_date = end_date - pd.DateOffset(days=9)
        filtered2_data = page2_data[(page2_data['Date'] >= start_date) & (page2_data['Date'] <= end_date)]
    else:
        filtered2_data = page2_data

    filtered2_data['Date'] = filtered2_data['Date'].dt.strftime('%Y-%m-%d')

    context = {
        'safaricom_data': filtered2_data.to_dict('records'),
        'selected_period': period
    }
    return render(request, 'financials/page2.html', context)