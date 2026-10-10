"""
Dollar Exchange page scrapper
"""
import os
import requests
import argparse
from bs4 import BeautifulSoup

def scrap_web_page(url:str) -> str:
    """Scrap the content of a web page and return the text."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as exc:
        raise Exception(f"Failed to retrieve the web page. Status code: {exc.response.status_code}") from exc
    except requests.RequestException as exc:
        raise Exception(f"Failed to retrieve the web page: {exc}") from exc

def get_dollar_exchange_rate(content:str):
    """Extract the dollar exchange rate from the web page content."""
    soup = BeautifulSoup(content, 'html.parser')
    main_table = soup.find('table', id='dllsTable')
    if main_table:
        rows = main_table.find_all('tr')
        price_list = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 4:
                sell_price = cols[3].text.strip()
                buy_price = cols[3].text.strip()
                bank_name = cols[2].text.strip()
            if len(cols) == 5:
                sell_price = cols[3].text.strip()
                buy_price = cols[4].text.strip()
                bank_name = cols[2].text.strip()
            price_list.append((bank_name, sell_price, buy_price))
        return price_list

def main(args):
    """Main function to scrap a web page and save its content to a file."""
    url = args.url
    output_file = args.output_file
    try:
        content = scrap_web_page(url)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Web page content saved to {output_file}")
        price_list = get_dollar_exchange_rate(content)
        if price_list:
            print("Dollar Exchange Rates:")
            for bank, sell, buy in price_list:
                print(f"Bank: {bank}, Sell: {sell}, Buy: {buy}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap a web page and save its content to a file.")
    parser.add_argument("url", type=str, help="The URL of the web page to scrap.")
    parser.add_argument("output_file", type=str, help="The output file to save the content.")
    args = parser.parse_args()
    main(args)