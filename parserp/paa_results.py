from bs4 import BeautifulSoup
import pandas as pd
import re, os, time, shutil
from datetime import datetime
from datetime import timedelta
import __main__
from parserp import soup_from_file

output_files = 'output_data'
file_paa_results = 'paa_results.csv'


def get_paa_results(soup):
    position = 1
    div_obj = {}
    div_obj['Keyword'] = []
    div_obj['Position'] = []
    div_obj['Question'] = []

    try:
        html_paa_results = soup.find("div", {"class": "ifM9O"})
        #print(html_paa_results)
        #html_paa_results = soup.find_all('div', {'class': 'related-question-pair'})

        #if soup.find_all('div', {'class': 'related-question-pair'}):
        #   print('Tag Found')
        #   print(soup.find_all('div', {'class': 'related-question-pair'}).text)
        #   questions = soup.find('div',class_='cbphWd').text
        #   print(questions)

        paa_results = html_paa_results.find_all('div',class_='cbphWd')
        #print(paa_results)
        for paa_result in paa_results:
            #if paa_result.find('div') is not None:

            keyword = soup.find('title').text.strip().split('-')[0]
            #print(keyword)
            div_obj['Keyword'].append(keyword)

            div_obj['Position'].append(position)
            #print(position)
            position +=1

            question = paa_result.text.strip()
            #print(question)

            div_obj['Question'].append(question)


        #print(div_obj)
        div_obj_df = pd.DataFrame(div_obj, index=None)
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d-%H")
        #print(dt_string)
        div_obj_df.to_csv(f'{output_files}/{dt_string}-{file_paa_results}', mode='a', header=False, index=False, encoding='UTF-8', sep='\t')
        print('---- paa_results')

    except:
        pass
