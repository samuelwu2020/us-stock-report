import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import datetime

def get_stock_data():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=^GSPC,^DJI,^IXIC"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查HTTP状态码
        data = response.json()
        if 'quoteResponse' in data and 'result' in data['quoteResponse']:
            return data['quoteResponse']['result']
        else:
            print("Error: Invalid API response format.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return []
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return []

def generate_report():
    stocks = get_stock_data()
    report = f"Market Summary - {datetime.date.today()}\n\n"
    for stock in stocks:
        name = stock.get('shortName', 'Unknown')
        price = stock.get('regularMarketPrice', 'N/A')
        change = stock.get('regularMarketChangePercent', 'N/A')
        report += f"{name}: {price} USD ({change:.2f}%)\n"
    return report

def send_email(report, recipient_email):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Daily US Stock Market Report"
    msg.attach(MIMEText(report, 'plain'))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    try:
        report = generate_report()
        print("Report generated successfully.")
        send_email(report, "thatsamuelwu@gmail.com")
    except Exception as e:
        print(f"Unexpected error: {e}")
