```python
import requests
import json
import logging
import time
import smtplib
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(filename='price_alert_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_sol_price():
    """Fetches the current SOL price from CoinGecko API"""
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': 'solana', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['solana']['usd']
    else:
        logging.error(f'Failed to fetch SOL price: {response.status_code}')
        return None

def send_alert(price, threshold, direction):
    """Sends an alert when the price crosses a specified threshold"""
    config = load_config()
    sender_email = config['sender_email']
    sender_password = config['sender_password']
    recipient_email = config['recipient_email']
    subject = f'SOL Price Alert: {direction} {threshold}'
    body = f'The current SOL price is {price} USD.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    logging.info(f'Sent alert: {subject}')

def load_config():
    """Loads the configuration from the config.json file"""
    with open('config.json', 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    threshold_high = config['threshold_high']
    threshold_low = config['threshold_low']
    last_price = None
    while True:
        current_price = get_sol_price()
        if current_price is not None:
            logging.info(f'Current SOL price: {current_price} USD')
            if last_price is not None:
                if current_price > threshold_high and last_price <= threshold_high:
                    send_alert(current_price, threshold_high, 'above')
                elif current_price < threshold_low and last_price >= threshold_low:
                    send_alert(current_price, threshold_low, 'below')
            last_price = current_price
        time.sleep(60)  # Check price every 1 minute

if __name__ == '__main__':
    main()
```