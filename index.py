import pandas
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from smtplib import SMTPException

url = 'https://www.vinted.pl/ubrania?search_text=lego+star+wars'

browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
browser.get('https://www.vinted.pl/ubrania?search_text=lego+star+wars')
data = browser.page_source
browser.close()
soup = BeautifulSoup(data,'html.parser')


grids = soup.find_all('div',{'class':'feed-grid__item'})[:9]
grids.pop(6)
items_list = []
for item in grids:
    list_item = {}
    list_item['anchor'] = item.find('a',{'class':'ItemBox_overlay__1kNfX'}).get('href')
    list_item['img'] = item.find('div',{'class':'ItemBox_image__3BPYe'}).find('img',{'class':'Image_content__lvAec'}).get('src')
    items_list.append(list_item)

web_data = pandas.DataFrame(items_list)
existing_data = ''
if os.path.isfile('Output.csv'):
    existing_data = pandas.read_csv('Output.csv')
else:
    web_data.to_csv('Output.csv')

if len(existing_data) > 0:
    filtered_data = existing_data.drop('Unnamed: 0',axis=1).reset_index().drop('index',axis=1)
    if not filtered_data.equals(web_data):
        web_data.to_csv('Output.csv')
        sender = '<from>@<domain>.com'
        receivers = ['<to>@<domain>.com']
        message = """From: Automation Monitor
        Hi,\nPlease check website because there is change occured.
        """
        smtpObj = smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(email,password)
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")

    


    
