import requests
from bs4 import BeautifulSoup
import csv
import re
def extract_picture_url(html_content):
    """Extracts the picture URL from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    div_tag = soup.find('div', class_='ProductDesktopImage__ImageWrapperDesktop-sc-8sgxcr-0')
    if div_tag:
        source_tag = div_tag.find('source')
        if source_tag and 'srcset' in source_tag.attrs:
            return source_tag['srcset']
    return "URL not found."

def extract_product_name(html_content):
    """Extracts the product name from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    span_tag = soup.find('span', class_='Text__StyledText-oo0kvp-0 gpVzIL', attrs={'color': 'greyT2', 'font-size': '18px', 'font-weight': 'demi'})
    if span_tag:
        return span_tag.get_text(strip=True)
    return "Product name not found"

def extract_price(html_content):
    """Extracts the product price from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    h4_tag = soup.find('h4', class_='Text__StyledText-oo0kvp-0 fka-Dwo')
    if h4_tag:
        return h4_tag.get_text(strip=True)
    return "Price not found."

def extract_rating(html_content):
    """Extracts the product rating from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    span_tag = soup.find('span', class_="Text__StyledText-oo0kvp-0 UKsFl", attrs={'color': '#ffffff', 'font-size': '16px', 'font-weight': 'demi'})
    if span_tag:
        return span_tag.get_text(strip=True)
    return "Product rating not found"

def extract_trusted_supplier(html_content):
    """Checks if the seller is trusted based on HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    p_tag = soup.find('p', class_="Text__StyledText-oo0kvp-0 hYxNyq", attrs={'color': 'greyT2', 'font-size': '16px', 'font-weight': 'book'})
    if p_tag and 'from trusted suppliers' in p_tag.text.lower():
        return 1
    return 0

def extract_name_of_the_seller(html_content):
    """Extracts the name of the seller from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    span_tag = soup.find('span', class_="Text__StyledText-oo0kvp-0 fFihtW ShopCardstyled__ShopName-du9pku-6 gdULmH ShopCardstyled__ShopName-du9pku-6 gdULmH", attrs={'color': 'greyBase', 'font-size': '18px', 'font-weight': 'demi'})
    if span_tag:
        return span_tag.get_text(strip=True)
    return "Seller Not Found"

def extract_product_details(html_content):
    """Extracts the product details from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    product_details = {}
    details_div = soup.find('div', class_='ProductDescription__DetailsCardStyled-sc-1tmqkzf-0')
    if details_div:
        for p_tag in details_div.find_all('p'):
            text = p_tag.get_text(strip=True)
            match = re.match(r'^(.+?)\s*:\s*(.+)$', text)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                product_details[key] = value
    return product_details

def extract_data(html_content):
    """Extracts all relevant data from HTML content."""
    picture_url = extract_picture_url(html_content)
    product_name = extract_product_name(html_content)
    price = extract_price(html_content)
    product_rating = extract_rating(html_content)
    trusted = extract_trusted_supplier(html_content)
    seller = extract_name_of_the_seller(html_content)
    product_details = extract_product_details(html_content)
    return {
        'Listing Name': product_name,
        'Listing Price': price,
        'Listing Picture URL': picture_url,
        'Product Details': product_details,
        'Name of the Seller': seller,
        'Trusted Supplier': trusted,
        'Product Ratings - Star': product_rating
    }

def main():
    """Main function to scrape data from URLs and write to CSV."""
    urls = [
        'http://127.0.0.1:5500/Aakarsha%20Petite%20Kurtis.html',
        'http://127.0.0.1:5500/Akiko%20PLUS%20SIZE%20Cotton%20Slub%20Bandhej%20Print%20Anarkali%20Kurta.html',
        'http://127.0.0.1:5500/Charvi%20Drishya%20Kurtis.html'
    ]

    output_file = 'product_data.csv'
    column_names = [
        'Line Number',
        'Listing Name',
        'Listing Price',
        'Listing Picture URL',
        'Product Details',
        'Name of the Seller',
        'Trusted Supplier',
        'Product Ratings - Star'
    ]

    data_rows = []
    line_number = 1  # Initialize line number counter

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            extracted_data = extract_data(response.content)
            # Include line number in the data dictionary
            extracted_data['Line Number'] = line_number
            data_rows.append(extracted_data)
            line_number += 1  # Increment line number for the next row
        else:
            print(f"Failed to fetch data from URL: {url}")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"Data successfully written to {output_file}")

if __name__ == "__main__":
    main()
