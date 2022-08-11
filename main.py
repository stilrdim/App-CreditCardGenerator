# https://cardguru.io/

import json
from pyperclip import copy
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime as dt
from time import sleep

print("Generating a VISA credit card...")

s = HTMLSession()
response = s.get('https://cardguru.io/credit-card-generator/visa')
response.html.render(sleep=3)

cardguru = BeautifulSoup(response.html.html, 'html.parser')

json_response = cardguru.find_all('span', {'class': 'hljs-string'})
json_attr = cardguru.find_all('span', {'class': 'hljs-attr'})
cvv = cardguru.find('span', {'class': 'hljs-number'}).text.replace('"', '')
card_number = json_response[1]

a = []
b = []
json_dict = {
    "cvv": cvv
}

for st in json_response:
    strings = st.text.replace('"', '')
    a.append(strings)

for st in json_attr:
    strings = st.text.replace('"', '')
    b.append(strings)

# Turn the two lists into a dictionary
for key in b:
    if key == 'cvv':
        continue
    for value in a:
        json_dict[key] = value
        a.remove(value)
        break

# Get today's date
time_now = dt.now()
date = str(time_now).split('.')[0]


with open('credentials.txt', 'a+') as f:
    json_object = json.dumps(json_dict, indent=0)
    f.write(f'-------------------\n{date}')
    f.write(json_object.replace('{', '').replace('}', '').replace('"', '').replace(',', ''))

# Put main details in clipboard
copy_string = f"{json_dict['cardNumber']} {json_dict['exp']} {json_dict['cvv']}"
copy(copy_string)

print(f"Credentials saved in clipboard.\nFile 'credentials.txt' created.\n{copy_string}")
sleep(5)
