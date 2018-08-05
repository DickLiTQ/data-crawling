#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:40:12 2018

@author: DickLi

Website: https://www.aqistudy.cn/historydata/

"""

import re
from selenium import webdriver
import pandas as pd
import time
import numpy as np

def remove_label(text):
    html_label = re.compile("<[^>]+>")
    return re.sub(html_label, "", text)

chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
df = pd.DataFrame(columns=['city','date','AQI','AQI_range','level','PM2.5','PM10','SO2','CO','NO2','O3'])
end = len(citylist)
now = 0
driver = webdriver.Chrome(chromedriver)
xpath = "/html/body/div[1]/div/div[2]/form/div/input"
url = "https://www.aqistudy.cn/historydata/monthdata.php?city="
html = driver.get(url)
citylist = ["北京","上海","广州","深圳"]


for city in citylist:
    now = now+1
    driver.find_element_by_xpath(xpath).clear()
    driver.find_element_by_xpath(xpath).send_keys(city)
    driver.find_element_by_xpath(xpath).submit()
    print("Now:(%d/%d) - %s"%(now,end,city))
    waittime1 = 4+ np.abs(np.random.normal(0,2))
    print("Waiting1: "+str(waittime1))
    time.sleep(waittime1)
    text = driver.page_source
    pattern1 = re.compile("<tr.+?</tr>")
    text1 = re.findall(pattern1, text)
    print(str(len(text1)))
    for item in text1:
        text2 = remove_label(item)
        pattern2 = re.compile("        ")
        text3 = re.split(pattern2, text2)
        mydict = {'city': city,
                  'date': text3[1],
                  'AQI': text3[2],
                  'AQI_range': text3[3],
                  'level':text3[4],
                  'PM2.5':text3[5],
                  'PM10':text3[6],
                  'SO2':text3[7],
                  'CO':text3[8],
                  'NO2':text3[9],
                  'O3':text3[10]}
        print(mydict)
        df = df.append(mydict, ignore_index=True)