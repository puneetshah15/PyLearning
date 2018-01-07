# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import dateutil
import sqlite3

urls= [
       "http://www.moneycontrol.com/mutual-funds/nav/l-t-liquid-fund-direct-plan/MCC283",
       "http://www.moneycontrol.com/mutual-funds/nav/reliance-regular-savings-fund-balanced-option-direct-plan/MRC1011",
       "http://www.moneycontrol.com/mutual-funds/nav/l-t-emerging-businesses-fund-dp/MCC492",
       "http://www.moneycontrol.com/mutual-funds/nav/reliance-regular-savings-fund-balanced-option/MRC100"
      ]

create_table_sql="""CREATE TABLE MutualFunds
(
asofdate date,
name varchar(255),
nav int,
primary key(name,asofdate)
);"""


db_file="E:\\Work_Related\\Learning Python\\MF.db"
data=[]

def process_urls():
    for url in urls:
        r=requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        name = soup.find_all('div', class_='header')
        name = name[0].find('h1').string
        nav_date = soup.find_all('div', class_='MT10')
        nav = nav_date[1].span.string
        asofdate = dateutil.parser.parse(" ".join(nav_date[1].p.string.split()[3:]))
        mytup = (asofdate,name,nav)
        data.append(mytup)
        print(mytup)

        with sqlite3.connect(db_file) as conn:
            cur=conn.cursor()
            cur.executemany("insert into MutualFunds values(?,?,?)", data)
            print(cur.lastrowid)

def fetchDatafromSqlite():
    with sqlite3.connect(db_file) as conn:
        cur=conn.cursor()
        cur.execute("select * from MutualFunds")
        rows = cur.fetchall()
        print(rows)
        
if __name__=="__main__":
    process_urls()
    fetchDatafromSqlite()