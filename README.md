# data-crawling
Containing my trial for data mining in several websites.

## Overture
I use **requests** and **webdriver** for data mining. If you don't have these tools, you are supposed to obtain them at first.

Use **pip** to install **requests** and **selenium**.
```{console}
pip install requests
pip install selenium
```
To mine a dynamic website, we need **PhantomJS** or **Chromedriver**. Here are some notes for download them.
- http://phantomjs.org
- http://phantomjs.org/download.html
- http://chromedriver.chromium.org
- http://chromedriver.storage.googleapis.com/index.html

It is easy for you to install them by google or baidu it.

## Crawling on different websites
All Python3 scripts are provided.

#### (a) History air quality data of Chinese cities from aqistudy
Environment is crucial for everything on Earth. To better protect our Earth, we may need history data in order to analyze. Here we choose the website [aqistudy](https://www.aqistudy.cn/historydata/) as our source of data.

This website is friendly and has about 300+ Chinese cities, providing data from 2014 to nowadays. We use **webdriver** to simulate searching actions and **pandas** to modify our data. 

```python
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
citylist = ["北京", "上海", "深圳", "广州"] # Here you can replace it with whatever you want can be found on that website.

for city in citylist:
    now = now+1 # Timer
    # Use driver to simulate people
    driver.find_element_by_xpath(xpath).clear()
    driver.find_element_by_xpath(xpath).send_keys(city)
    driver.find_element_by_xpath(xpath).submit()
    # Wait for an interval to diminish the stress of Server :)
    print("Now:(%d/%d) - %s"%(now,end,city))
    waittime1 = 4+ np.abs(np.random.normal(0,2))
    print("Please wait for a random time: "+str(waittime1))
    time.sleep(waittime1)
    # Obtain data on pages
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
```


