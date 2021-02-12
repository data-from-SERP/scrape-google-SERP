from bs4 import BeautifulSoup
import pandas as pd
import re, os, time, shutil
from datetime import datetime
from datetime import timedelta
import __main__
from parserp import soup_from_file

output_files = 'output_data'
file_organic_results = 'organic_results.csv'


def get_organic_results(soup):
    position = 1
    div_obj = {}
    div_obj['Keyword'] = []
    div_obj['Position'] = []
    div_obj['Titles'] = []
    div_obj['Links'] = []
    #div_obj['Displayed Links'] = []
    #div_obj['Snippets'] = []
    #div_obj['Cached Page Links'] = []
    #div_obj['Inline Links'] = []
    #soup = soup_from_file(f'{html_file}/{file}'.format(file=file,html_file=html_file))
    html_organic_results = soup.find("div", {"id": "rso"})
    #print(html_organic_results)
    organic_results = html_organic_results.find_all('div',class_='g')
    #print(organic_results)

    for organic_result in organic_results:
        keyword = soup.find('title').text.strip().split('-')[0]
        #print(keyword)
        div_obj['Keyword'].append(keyword)
        #posizione + 1
        div_obj['Position'].append(position)
        #print(position)
        position +=1
        title = organic_result.find('h3').text.strip()
        #print(title)
        div_obj['Titles'].append(title)
        link = organic_result.find('a').attrs['href']
        #print(link)
        div_obj['Links'].append(link)
    #print(div_obj)
    div_obj_df = pd.DataFrame(div_obj, index=None)
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d-%H")
    print(dt_string)
    div_obj_df.to_csv(f'{output_files}/{dt_string}-{file_organic_results}', mode='a', header=False, index=False, encoding='UTF-8', sep=';')
    print('---- organic_results')
