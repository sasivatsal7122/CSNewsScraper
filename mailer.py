import smtplib
from email.message import EmailMessage
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from time import sleep
import os
from string import Template


def read_info():
    sheet_url = "https://docs.google.com/spreadsheets/d/1ny-ehlpHMOqmjZsKDJqvUhIOGJyX78V_w9XptU32qOg/edit?resourcekey#gid=1638289615"
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
    df = pd.read_csv(url_1)
    
    print(df)
    names = df['Student Name'].to_list()
    emails = df['Email'].to_list()
    
    print(names)
    print(emails)
    
    return emails, names


def send_mail(email_receiver,names):
    load_dotenv()

    email_sender = 'owaspviit@gmail.com'
    email_password = os.getenv("OWASP-VIIT-PASSWORD")
    print(email_sender, email_password)
    #email_receiver = ['sasivatsal7122@gmail.com','likhithbavisetti@gmail.com','mallaharsha66@gmail.com','lokeshwarlakhi@gmail.com']
    email_receiver = tqdm(email_receiver)
    #names = ['Satya Sasi Vatsal','Likhith',"Mallesh","Lokesh"]
    
    for email,name in zip(email_receiver,names):
        Reciever_Email = email

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        smtp.login(email_sender, email_password)

        newMessage = EmailMessage()
             
        with open('master_body.html','r+',encoding='utf-8') as f:
            html_body = f.readlines()
                
        subject = 'Hey {Name}. checkout our newsletter'
        subject = subject.format(Name=name)
        
        html_body = ' '.join([str(char) for char in html_body])
    
        newMessage['Subject'] = subject
        newMessage['From'] = email_sender
        newMessage['To'] = Reciever_Email
        newMessage.set_content(html_body,subtype='html')

        smtp.sendmail(from_addr=email_sender, to_addrs=Reciever_Email, msg=newMessage.as_string())
        sleep(.01)

    smtp.quit()


if __name__ == '__main__':  
   emails, names = read_info()
   send_mail(emails,names)