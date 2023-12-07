# import module
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as soup
from dataclasses import dataclass

class govDataset:
    hdr = {'User-Agent':'Mozilla/5.0', 'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    def __init__(self, dataURL:str):
        self.dataURL = dataURL
        self.url = {}

        self._connected = 0
        self.html_soup = soup
        self._allTags = soup.ResultSet
        self.connect()

    def connect(self):
        # Connect to data.gov.hk
        try:
            self.req = urllib.request.Request(self.dataURL, headers=self.hdr)
            self.html_page = urllib.request.urlopen(self.req, timeout=60)
            self.html_soup = soup(self.html_page, "html.parser")
            self._connected = 1
        except:
            print(f'Failed connecting to {self.dataURL}')

    class grab:
        def __init__(self, mode:str='print'):
            self.mode = mode

        def grabCsvList(self):
            if (self._connected):
                self.htmlTagToKeep = ['a']
                self._allTags = self.html_soup.findAll(self.htmlTagToKeep, class_='dataset-details__list-item-download')

        def save(self):
            if self.mode=='print':
                for i, tag in enumerate(self._allTags):
                    print(tag.get('href'))
                    self.url[i] = tag

            if self.mode=='save':
                self.f = open('csvList.txt', 'w')
                for i, tag in enumerate(self._allTags):
                    self.url[i] = tag
                    self.f.write(tag.get('href')+'\n')
                self.f.close()