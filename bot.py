import requests
from bs4 import BeautifulSoup
import schedule
import time
import telegram

# Telegram bilgileri
BOT_TOKEN = "8581645631:AAFkKcUAqB-1jdyzGUiJ4VdruJ6A4GNxOxs"
CHAT_ID = "5250165372"

bot = telegram.Bot(token=BOT_TOKEN)

# Kontrol edilecek siteler (örnek: Amazon ve Hepsiburada)
sites = [
    {
        "name": "Amazon",
        "url": "https://www.amazon.com.tr/s?k=televizyon",
        "parser": "html.parser",
        "price_selector": "span.a-price-whole"
    },
    {
        "name": "Hepsiburada",
        "url": "https://www.hepsiburada.com/laptop-x-c-98",
        "parser": "html.parser",
        "price_selector": "div.price"
    }
]

def check_discounts():
    for site in sites:
        try:
            r = requests.get(site["url"], headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, site["parser"])
            price_tags = soup.select(site["price_selector"])
            
            if price_tags:
                price_text = price_tags[0].get_text().replace(".", "").replace(",", ".")
                price = float(price_text)
                if price < 10000:
                    message = f"{site['name']} sitesinde fırsat! Şu an fiyat: {price} TL\n{site['url']}"
                    bot.send_message(chat_id=CHAT_ID, text=message)
        except Exception as e:
            print(f"Hata {site['name']} kontrolünde: {e}")

# Her 30 dakikada bir çalışacak
schedule.every(30).minutes.do(check_discounts)

print("Bot başlatıldı...")
bot.send_message(chat_id=CHAT_ID, text="Fırsat botu başlatıldı!")

while True:
    schedule.run_pending()
    time.sleep(10)
