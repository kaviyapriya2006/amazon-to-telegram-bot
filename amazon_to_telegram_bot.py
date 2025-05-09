import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot

# === CONFIGURATION ===
AMAZON_URL = 'https://www.amazon.in/boAt-Nirvana-Crystl-Quantum-Black/dp/B0DGTVRH97/ref=sr_1_1?nsdOptOutParam=true&s=electronics&sr=1-1'  
AFFILIATE_LINK = 'https://amzn.to/438ok8x' 
TELEGRAM_TOKEN = '8155146341:AAEiwJ6IjiTOqMXjIhDm-D11y7WYff6GiIA'  
TELEGRAM_CHAT_ID = '@LootersZone123' 

# === SCRAPE AMAZON PRODUCT DATA ===
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br'
}

# Send the request to Amazon and parse the page
res = requests.get(AMAZON_URL, headers=headers)
soup = BeautifulSoup(res.content, 'html.parser')

# Find the title and image
title = soup.find(id='productTitle')
image = soup.find('img', {'id': 'landingImage'})

# Extract the product title and image URL
product_title = title.get_text(strip=True) if title else 'No Title Found'

# Ensure image URL is complete (handle relative URLs)
image_url = image['src'] if image else None
if image_url and not image_url.startswith('http'):
    image_url = 'https://www.amazon.in' + image_url  # Prepend the base URL if relative

# === SEND TO TELEGRAM ===
async def send_to_telegram():
    if image_url:
        bot = Bot(token=TELEGRAM_TOKEN)
        caption = f"🛒 *{product_title}*\n🔗 [Buy Now]({AFFILIATE_LINK})"
        await bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'
        )
        print("Posted to Telegram successfully!")
    else:
        print("Failed to get image. Product may not exist or scraping blocked.")

# Run the async function
asyncio.run(send_to_telegram())
