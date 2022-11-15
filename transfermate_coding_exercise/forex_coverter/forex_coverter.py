import os
import sys
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

def forex_conversion(folder):
    '''
    Read all files in the given folder and perform foreign exchange coversion
    '''

    # Initialize id to have unique ids in result
    id = 0
    # Initialize dataframe to store final result
    df_result = pd.DataFrame(columns = ['ID', 'SourceCurrency', 'DestinationCurrency', 'SourceAmount', 'DestinationAmount', 'Rate'])

    #Iterate through files in the folder
    for f in sorted(os.listdir(folder)): 
        
        os.chdir(folder)
        print(os.path.abspath(f))
        # Need to handle multiple file formats mentioned in the challenge
        rewrite_file = False
        with open(rf'{f}', 'r') as fileh:
            data = fileh.read()
            if '|' in data:
                data = data.replace('|', ',')
                rewrite_file = True
        if rewrite_file:
            with open(rf'{f}', 'w') as fileh:
                fileh.write(data)

        df = pd.read_csv(f'{f}', skipinitialspace = True)
        # Have uniform column names in all input files
        column_names = {
            'Currency1': 'SourceCurrency',
            'Currency2': 'DestinationCurrency',
            'SrcAmount': 'SourceAmount',
            'TrxId': 'ID',
            'CurrencyFrom': 'SourceCurrency',
            'CurrencyTo': 'DestinationCurrency',
            'AmountFrom': 'SourceAmount'
        }
        df.rename(columns=column_names, inplace=True)
        # print(df)
        print(list(df.columns.values))
        # Initial a dict to store forex rates values for each country in dataframe
        rates_dict = {}
        for index, row in df.iterrows():
            base_curr = row["SourceCurrency"]
            if base_curr not in rates_dict:
                # Get forex rates for base currency
                rates_dict = get_forex_rates(base_curr, rates_dict)

            rate = rates_dict[base_curr][row["DestinationCurrency"]]
            dest_amt = row["SourceAmount"] * rate
            # Add new record to with destination currency and rate
            df_new_row = pd.DataFrame({
                "ID": id,
                "SourceCurrency": [row['SourceCurrency']],
                "DestinationCurrency": [row['DestinationCurrency']],
                "SourceAmount": [row['SourceAmount']],
                "DestinationAmount": [dest_amt],
                "Rate": [rate]
            })
            # Update df_result with the new record
            df_result = pd.concat([df_result, df_new_row], ignore_index=True)
            id += 1
    
    print(df_result)
    df_result.to_csv('result.csv')

def get_forex_rates(base_curr, rates_dict):
    '''
    Call fixer endpoint get forex rates using requests library
    '''
    base_url = 'https://api.apilayer.com/fixer/latest'
    headers = {'apikey': os.getenv('API_KEY')}
    if base_curr in rates_dict:
        return rates_dict
    url = f'{base_url}?base={base_curr}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError('Error from fixer endpoint')

    forex_response = response.json()

    # Check if we are getting success response
    if forex_response and forex_response['success'] == True:
        # Update the rates for the base currency
        rates_dict[forex_response['base']] = forex_response['rates']
        return rates_dict
    raise RuntimeError('Error from fixer endpoint')
    
    
try:
    folder = sys.argv[1]
except IndexError:
    raise ValueError('Folder path is required in the command')

forex_conversion(folder)



