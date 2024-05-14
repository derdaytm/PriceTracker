from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

app = Flask(__name__)

def get_amazon_product_page(url):
    response = requests.get(url)
    while True :
        if response.status_code == 200:
            return response.text
        else:
            print("Üzgünüz, istek başarısız oldu. Durum Kodu:", response.status_code)
            print("Tekrar Deneniyor...")
            time.sleep(300)
            return get_amazon_product_page(url)

def extract_product_info(page_content, website):
    soup = BeautifulSoup(page_content, 'html.parser')
    if website == "amazon": 
        price_element = soup.find('span', class_='a-offscreen')
        if price_element:
            price = price_element.text.strip()
            return price
        else:
            return "Ürün fiyatı bulunamadı." 
    if website == "trendyol" :
        price_element = soup.find('span', class_='prc-dsc')
        if price_element:
            price = price_element.text.strip()
            return price
        else:
            return "Ürün fiyatı bulunamadı." 
    if website == "hepsiburada": 
        price_element = soup.find('span', attrs={'data-bind': "markupText:'currentPriceBeforePoint'"})
        if price_element:
            price = price_element.text.strip()
            return price
        else:
            return "Ürün fiyatı bulunamadı."    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_price', methods=['POST'])
def get_price():
    data = request.get_json()
    product_url = data['url']
    website = data['wsite'] 
    page_content = get_amazon_product_page(product_url)
    if page_content:
        product_price = extract_product_info(page_content, website)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({'Fiyat': product_price, 'Tarih': current_time})
    else:
        return jsonify({'error': 'Sayfa içeriği alınamadı.'})

if __name__ == "__main__":
    app.run(debug=True)
