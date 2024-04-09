import requests
import pandas as pd
from openpyxl import Workbook

def fetch_top_coins(limit=250):
    # CoinGecko API endpoint for fetching the top coins
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Extract relevant information from the API response
        top_coins = []
        for coin in data:
            coin_info = {
                'Rank': coin['market_cap_rank'],
                'Name': coin['name'],
                'Symbol': coin['symbol'],
                'Price (USD)': coin['current_price'],
                'Market Cap (USD)': coin['market_cap'],
                '24h Change (%)': coin['price_change_percentage_24h']
            }
            top_coins.append(coin_info)

        return top_coins

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_excel(data, filename='250_ranks.xlsx', sheet_name='Top250'):
    try:
        # Create a new workbook
        workbook = Workbook()
        workbook.save(filename)

        # Save the DataFrame to Excel using Pandas to_excel
        df = pd.DataFrame(data)
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data saved to {filename} sheet '{sheet_name}'.")

    except Exception as e:
        print(f"Error saving data to Excel: {e}")

def main():
    # Fetch the top 250 coins
    top_coins = fetch_top_coins()

    if top_coins:
        # Display the fetched data
        print("Top 250 Cryptocurrencies:")
        print("{:<5} {:<15} {:<8} {:<15} {:<20} {:<15}".format(
            'Rank', 'Name', 'Symbol', 'Price (USD)', 'Market Cap (USD)', '24h Change (%)'
        ))
        for coin in top_coins:
            print("{:<5} {:<15} {:<8} {:<15} {:<20} {:<15}".format(
                coin['Rank'], coin['Name'], coin['Symbol'], coin['Price (USD)'], coin['Market Cap (USD)'], coin['24h Change (%)']
            ))

        # Save data to Excel file
        save_to_excel(top_coins)

if __name__ == "__main__":
    main()
