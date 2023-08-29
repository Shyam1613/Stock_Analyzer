# pip install streamlit prophet yfinance plotly

import streamlit as st
from datetime import date
from flask import Flask
import yfinance as yf
import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from bs4 import BeautifulSoup
from lxml import etree
import requests
import subprocess
# import mysql.connector,time
# from mysql.connector import errorcode
from flask import Flask,render_template,request,redirect,url_for,session

# try:
#   cnx = mysql.connector.connect(user='root',host="localhost",password="12345",database='farm')
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
    
# cur=cnx.cursor()
app = Flask(__name__)

options = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA',
'DIVISLAB', 'DRREDDY', 'EICHERMOT', 'GRASIM', 'HCLTECH',
'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR',
'HDFC', 'ICICIBANK', 'ITC', 'IOC', 'INDUSINDBK', 'INFY',
'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC',
'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE',
'SHREECEM', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS',
'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']




def fetchNifty():
    URL = "https://ticker.finology.in/"

    HEADERS = ({'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
    'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    sensex =float (dom.xpath('//*[@id="frmTicker"]/div[3]/div/div[1]/h6/a/span[1]')[0].text)
    sensexChange =float(dom.xpath('//*[@id="frmTicker"]/div[3]/div/div[1]/h6/a/span[2]/span[1]')[0].text) 
    print(sensex,sensexChange)
    nifty = float(dom.xpath('//*[@id="frmTicker"]/div[3]/div/div[2]/h6/a/span[1]')[0].text)
    niftyChange =float(dom.xpath('//*[@id="frmTicker"]/div[3]/div/div[2]/h6/a/span[2]/span[1]')[0].text) 
    print(nifty,niftyChange)
    global list
    list=(sensex,sensexChange,round((sensexChange/sensex)*100,3),nifty,niftyChange,round((niftyChange/nifty)*100,3))


@app.route('/',methods=['GET','POST'])
def main():
    fetchNifty()    
    return (render_template('index.html',list=list,options=options))  



@app.route('/search',methods=['GET','POST'])
def search():   
    if request.method == 'POST':
        stock = str(request.form['search'])
        global stk
        stk=stock
        fetchdata(stock)
        classify_stock()
    return(render_template('stocks.html',stock=stock,list1=list1))




# def display(stock):
#     return (render_template('stocks.html',stock=stock,list1=list1))


# @app.route('/login',methods=['GET','POST'])
# def admin():
#     if request.method=='POST':
#       email=(request.form['email'])
#       passwd=(request.form['pswd'])
#       cur.execute("select * from user")
#       login=cur.fetchone()
#       if user==login[0] and passwd==login[1]:
#         return redirect(url_for('loggedin'))
#       else:
#         return (render_template('loginfail.html'))     
#     return (render_template('login.html'))

# fetch data
def launch_streamlit_app():
    

    subprocess.run(['streamlit', 'run', 'prediction.py',stk])
	
    # subprocess.call(['python', 'prediction.py',stk])
    print(stk)
   	


@app.route('/prediction')
def prediction():
    launch_streamlit_app()

@app.route('/tutorial')
def tutorial():
    return(render_template('tutorial.html'))

def fetchdata(company_name):
        global pe_ratio, pb_ratio, roe, roce, debt_to_equity_ratio
        
        URL = "https://ticker.finology.in/company/"+company_name+""

        
        HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})

        
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        #pe_ratio, pb_ratio, last_price, dividends_per_share, roe, roce, debt_to_equity_ratio
        pe_ratio = float(dom.xpath('//*[@id="mainContent_updAddRatios"]/div[4]/p')[0].text.strip())
        pb_ratio = float(dom.xpath('//*[@id="mainContent_updAddRatios"]/div[5]/p')[0].text.strip())
        roe = float(dom.xpath('//*[@id="mainContent_updAddRatios"]/div[14]/p/span')[0].text.strip())
        try:
            debt_to_equity_ratio = float(dom.xpath('//*[@id="mainContent_divDebtEquity"]/div/span/span')[0].text.strip())
        except:
             debt_to_equity_ratio=0 
        roce = float(dom.xpath('//*[@id="mainContent_updAddRatios"]/div[15]/p/span')[0].text.strip())
        global list1
        list1=[pe_ratio, pb_ratio, roe, roce, debt_to_equity_ratio]

def classify_stock():
    # Define the threshold values
    pe_ratio_threshold = 20
    pb_ratio_threshold = 3
    roe_threshold = 10
    roce_threshold = 10
    debt_to_equity_ratio_threshold = 1

    # Check each parameter against its threshold value and classify the stock as undervalued or overvalued
    if pe_ratio < pe_ratio_threshold and pb_ratio < pb_ratio_threshold and (roe > roe_threshold or roce > roce_threshold) and debt_to_equity_ratio < debt_to_equity_ratio_threshold:
        list1.append('Undervalued') 
    else:
        list1.append('Overvalued')
# fetchTopFive()

if __name__ == '__main__':
	app.run(debug=True)
 