import requests
import ddddocr
from bs4 import BeautifulSoup
import time
from datetime import time as datetime_time

from datetime import datetime
import time as tm
import re
def login(account,password):
    ocr = ddddocr.DdddOcr()
    s=requests.Session()
    url='https://www.cjcf.com.tw/CG02.aspx'
    resp=s.get(url)
    time.sleep(1)
    url='https://www.cjcf.com.tw/ShowInfo.aspx?action=LoginCheck'
    resp=s.get(url)
    time.sleep(1)
    url='https://www.cjcf.com.tw/CG02.aspx?module=login_page&files=login'
    resp=s.get(url)
    time.sleep(1)
    url='https://www.cjcf.com.tw/CG02.aspx?Module=ind&files=ind'
    resp=s.get(url)
    time.sleep(1)
    url='https://www.cjcf.com.tw/NewCaptcha.aspx?img=0.9968041272657759'
    resp=s.get(url)
    time.sleep(1)

    data = resp.content 
    res = ocr.classification(resp.content)

    with open('image.gif', 'wb') as file:
        file.write(data)
    url='https://www.cjcf.com.tw/CG02.aspx?Module=login_page&files=login'

    data = {
        'loginid': f'{account}',
        'loginpw': f'{password}',
        'Captcha_text': f'{res}'
    }

    resp=s.post(url,data)
    if '您好' in resp.text:
        print('登入成功')
        return s
    else:
        print('請確認帳號密碼')
def wait_until_midnight():
    while True:
        # Get the current time
        now = datetime.now()
        current_time = now.time()
        
        # Check if the current time is past 23:59:59
        if current_time >= datetime_time(23, 59, 58):
            print("It's past 23:59:59, starting while loop...")
            break
        else:
            print("It's not time yet, waiting...")
            # Wait for a second before checking the time again to avoid overloading the CPU
            tm.sleep(0.5)
def booking(s,date,booking_time,lot):        
   
    #wait_until_midnight()
    url=f'https://www.cjcf.com.tw/CG02.aspx?module=net_booking&files=booking_place&StepFlag=25&QPid={lot}&QTime={booking_time}&PT=1&D={date}'
    resp=s.get(url)
    while not (check(s,resp)):
        time.sleep(0.6)
        url=f'https://www.cjcf.com.tw/CG02.aspx?module=net_booking&files=booking_place&StepFlag=25&QPid={lot}&QTime={booking_time}&PT=1&D={date}'
        resp=s.get(url)
    
    
def check(s,resp):
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Find the script tag containing the URL
    script_tag = soup.find('script', text=re.compile(r"window.location.href='(.*?)'"))
    if script_tag:
        # Extract the URL segment from the script tag using a regular expression
        match = re.search(r"window.location.href='(.*?)'", script_tag.string)
        url_segment = match.group(1) if match else None
        url=f'https://www.cjcf.com.tw/{url_segment[9:]}'
        resp=s.get(url)
        if  '預約失敗' in resp.text:
            print('失敗')
            return False
        else:
            print('預定成功')
            return True
# A107661084
# 123456789

def start_booking():
    account = username_entry.get()
    password = password_entry.get()
    date='2023/12/01'
    booking_time='20'
    dict={
        "羽3":1114,	
        "羽4":1115,
        "羽5":1116,
        "羽8":1150,
        "羽9":1151,	
        "羽10":1152,		
        "羽11":1151,	
        "羽12":1155,	
    }
    lot=dict['羽5']
    s=login(account,password)
    url='https://www.cjcf.com.tw/CG02.aspx?Module=net_booking&files=booking_before&PT=1'
    resp=s.get(url)
    time.sleep(1)
    url='https://www.cjcf.com.tw/CG02.aspx?module=net_booking&files=booking_place&PT=1'
    resp=s.get(url)
    time.sleep(1)
    url=f'https://www.cjcf.com.tw/CG02.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={date}&D2=1'
    resp=s.get(url)
    time.sleep(1)
    url=f'https://www.cjcf.com.tw/CG02.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={date}&D2=3'
    resp=s.get(url)
    time.sleep(1)
    booking(s,date,booking_time,lot)
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Login Interface")
root.geometry("800x600")

# Create labels for username and password
username_label = tk.Label(root, text="帳號:")
username_label.place(x=200, y=150)
password_label = tk.Label(root, text="密碼:")
password_label.place(x=200, y=190)

# Create entry widgets for username and password
username_entry = tk.Entry(root)
username_entry.place(x=400, y=150)
password_entry = tk.Entry(root, show="*")
password_entry.place(x=400, y=190)

# Create three selection boxes (dropdown menus)
options = ["選項1", "選項2", "選項3"]
option1 = tk.StringVar(root)
option1.set(options[0])
option_menu1 = tk.OptionMenu(root, option1, *options)
option_menu1.place(x=200, y=230)

option2 = tk.StringVar(root)
option2.set(options[0])
option_menu2 = tk.OptionMenu(root, option2, *options)
option_menu2.place(x=350, y=230)

option3 = tk.StringVar(root)
option3.set(options[0])
option_menu3 = tk.OptionMenu(root, option3, *options)
option_menu3.place(x=500, y=230)

# Create a text display box
text_display = tk.Text(root, height=5, width=50)
text_display.place(x=200, y=270)

# Create three buttons
login_button = tk.Button(root, text="登入")
login_button.place(x=200, y=400)

start_button = tk.Button(root, text="開始",command=start_booking)
start_button.place(x=350, y=400)

stop_button = tk.Button(root, text="中斷")
stop_button.place(x=500, y=400)

# Run the application
root.mainloop()
