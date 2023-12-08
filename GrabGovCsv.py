# import module
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as soup
from dataclasses import dataclass
import re
from IPython.display import display
import os

class govDataset:
    hdr = {'User-Agent':'Mozilla/5.0', 'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    def __init__(self, dataURL:str):
        self.dataURL = dataURL
        self.title = {}
        self.url = {}

        self._connected = 0
        self.html_soup = soup
        self.df = pd.DataFrame()
        self.connect()

    def connect(self):
        # Connect to data.gov.hk
        try:
            self.req = urllib.request.Request(self.dataURL, headers=self.hdr)
            self.html_page = urllib.request.urlopen(self.req, timeout=60)
            self.html_soup = soup(self.html_page, "html.parser")
            self._connected = 1
            print('Connected')
        except:
            print(f'Failed connecting to {self.dataURL}')

    def grab(self, mode:str, lang:str='all'):
        """ 
        mode='print' or
        mode='csv' or
        mode='txt'

        lang='all' or
        lang='zh' or
        lang='en'
        """
        self.mode = mode
        self.lang = lang
        if (self._connected):
            self._htmlTagToKeep = ['a', 'div']
            self._allTitle = self.html_soup.findAll(self._htmlTagToKeep, class_='dataset-details__list-item-name')
            self._allaTags = self.html_soup.findAll(self._htmlTagToKeep, class_='dataset-details__list-item-download')
            
            for i, TITLE in enumerate(self._allTitle):
                self.title[i] = TITLE.text
            for i, URL in enumerate(self._allaTags):
                self.url[i] = URL.get('href')

            self.df['Title'] = self.title
            self.df['URL'] = self.url
            self.save()
            # PROGRESS
            

    def save(self):
        self.df['isZH']={}
        for i, tt in enumerate(self.df['Title']):
            self.df['Title'].loc[i] = re.sub(r'/', '-', re.sub(r'\n', '', re.sub(r' ', '', tt)) )
            self.df['isZH'].loc[i] = (re.findall('繁', tt))

        if (self.lang == 'zh'):
            self.df= self.df[self.df['isZH'].str.len()!=0]
        else:
            self.df= self.df[self.df['isZH'].str.len()==0]
        
        if self.mode=='dataframe':
            display(self.df);
        if self.mode=='print':
            print(self.df['URL'])

        if self.mode=='txt':
            f = open('csvList.txt', 'w')
            for i in self.df['URL']:
                f.write(f"{i}+'\n'")
            f.close()

        for i in f'/csv/{tt[i]}.csv':
            if not os.path.isdir(i):
                os.makedirs(i)

        if self.mode == 'csv':
            tt, url = self.df['Title'], self.df['URL']
            for i in self.df.reset_index(drop=True).index:
                self.fildir = f'/csv/{tt[i]}.csv'
                urllib.request.urlretrieve(url[i], self.fildir)

