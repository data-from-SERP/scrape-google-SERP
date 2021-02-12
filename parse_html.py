import pandas as pd
import re, os, time, shutil
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from parserp import soup_from_file
from parserp import organic_results
from parserp import related_searches
from parserp import inline_shopping

#variabili
html_file = 'output_html'
html_file_error = 'output_html_error'
output_files = 'output_data'

#creazione cartelle
if not os.path.exists(output_files):
    os.makedirs(output_files)
if not os.path.exists(html_file_error):
    os.makedirs(html_file_error)

files = [file for file in os.listdir(html_file) if '.html' in file]
for file in files:
    print(file)
    #filename = file
    soup = soup_from_file.get_soup_from_file(file)
    organic_results.get_organic_results(soup)
    related_searches.get_related_searches(soup)
    #inline_shopping.get_inline_shopping(soup)
    print('finito file')
