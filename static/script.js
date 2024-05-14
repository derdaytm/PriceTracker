function getPrice() {
    var productLink = document.getElementById('productLink').value;
    var website = detectWebsite(productLink);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_price', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var productPrice = response['Fiyat'];
            var currentDate = response['Tarih'];
            updatePriceContainer(productPrice, currentDate);
        } else {
            console.log('Bir hata oluştu. Durum kodu: ' + xhr.status);
        }
    };
    xhr.send(JSON.stringify({url: productLink, wsite: website}));
}
function detectWebsite(url) {
    if (url.includes("amazon.com")) {
        return "amazon";  }
    if (url.includes("trendyol.com")) {
        return "trendyol"; }
    if (url.includes("hepsiburada.com")) {
        return "hepsiburada"; }   }

function updatePriceContainer(price, date) {
    var priceContainer = document.getElementById('priceContainer');
    var newPriceEntry = document.createElement('div');
    newPriceEntry.innerHTML = 'Ürün Fiyatı: ' + price + '<br>' + 'Güncelleme Tarihi: ' + date + '<br>' + '-------------------------------------------------------';
    priceContainer.appendChild(newPriceEntry);
}

setInterval(getPrice, 14400000);
