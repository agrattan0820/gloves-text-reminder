import os
import json
import requests
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


def getWeatherData():
    params = {
        "access_key":  os.environ["WEATHERSTACK_API_KEY"],
        "query": os.environ["WEATHERSTACK_QUERY"],
        "units": "f"
    }

    api_result = requests.get('http://api.weatherstack.com/current', params)

    api_response = api_result.json()

    print(json.dumps(api_response, indent=2))

    print('Current temperature in %s is %d' %
          (api_response['location']['name'], api_response['current']['temperature']))

    return api_response


def sendGlovesText(weather_data):
    # Email Server Setup
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    sms_gateway = os.environ["SMS_GATEWAY"]

    smtp = os.environ["SMTP_SERVER"]
    port = 587

    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(email, password)

   # Create message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    msg['Subject'] = "It's cold: %s" % (
        weather_data['current']['temperature'])
    body = "Put on your gloves!\n"
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(email, sms_gateway, sms)


if __name__ == '__main__':
    weather_data = getWeatherData()
    if int(weather_data['current']['temperature']) <= 50:
        sendGlovesText(weather_data)
