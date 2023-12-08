# import module
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as soup
from dataclasses import dataclass
import re
from IPython.display import display


class govDataset:
    hdr = {'User-Agent':'Mozilla/5.0', 'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    def __init__(self, dataURL:str):
        self.dataURL = dataURL
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
        if (self._connected):
            self._htmlTagToKeep = ['a']
            self._allTitle = self.html_soup.findAll(self._htmlTagToKeep, class_='dataset-details__list-item-download')
            self._allaTags = self.html_soup.findAll(self._htmlTagToKeep, class_='dataset-details__list-item-download')
            
            for i, title in enumerate(self._allTitle):
                self.url[i] = title

            self.df['Title'] = self.url
            # PROGRESS
            

            self.save(lang)

    def save(self):
        if self.mode=='dataframe':
            display(self.df);
        if self.mode=='print':
            for tag in self._allaTags:
                print(tag.get('href'))

        if self.mode=='txt':
            self.f = open('csvList.txt', 'w')
            for tag in self._allaTags:
                self.f.write(tag.get('href')+'\n')
            self.f.close()

        if self.mode == 'csv':
            for tag in self._allaTags:
                local_filename, headers = urllib.request.urlretrieve('tag')
                urllib.request.urlretrieve(re.findall(r'ss[0-9]{4}.*',local_filename, f'{local_filename}.csv'))
            self.f.close()