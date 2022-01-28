import csv
import os
import yaml
import smtplib
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Initialise email parameters
def fetch_config():
    configfile = os.path.dirname(os.path.abspath('config.yaml')) + '/config.yaml'
    with open(configfile) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

text = """
Hello, please find below ...
{table}
Cheers.
"""

html = """
<html>
<head>
<style>
        table {{ border-collapse: collapse; border: 1px solid black; padding: 5px; }}
        th, td {{ padding : 5px; border: 2px solid black; }}
</style>
</head>
<body>
<p>Hello, </p>
<p> Please find below report on performance of KPIs </p>
{table}
<p>Thank you</p>
</body>
</html>
"""

with open(os.path.dirname(os.path.abspath('reportFile.csv')) + '/reportFile.csv') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])

message['Subject'] = "Hits Count Daily Report"
message['From'] = fetch_config()['sender_email']
message['To'] = fetch_config()['recipient_email']
server = smtplib.SMTP(fetch_config()['server'])
server.ehlo()
server.starttls()
server.login(fetch_config()['sender_username'], fetch_config()['sender_password'])
server.sendmail(fetch_config()['sender_email'], fetch_config()['recipient_email'], message.as_string())
server.quit()

# remove file after email is sent
os.remove(os.path.dirname(os.path.abspath('config.yaml')) + '/config.yaml')
