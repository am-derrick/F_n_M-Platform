from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd

file_path = 'static/csv_files/SCOMHistoricalPrices[June_to_Aug].csv'
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# Page 1 from July 2024 to Date
page1_data = df[df['Date'] >= '2024-07-01']

# Page 2 from June 2024 to Date
page2_data = df[df['Date'] >= '2024-06-01']

def financial_analysis_1(request):
    """view for page 1 of the financial analysis tab showing SCOM data
    from July 1 2024 to date"""
    context = {
        'SCOM_data': page1_data.to_dict('records')
    }
    return render(request, 'financials/page1.html', context)

@login_required
def financial_analysis_2(request):
    """view for page 1 of the financial analysis tab showing SCOM data
    from June 1 2024 to date"""
    if not request.user.is_full_member:
        return redirect('macroeconomics:upgrade')
    context = {
        'SCOM_data': page2_data.to_dict('records')
    }
    return render(request, 'financials/page2.html', context)