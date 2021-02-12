#i campi https://www.scaleserp.com/docs/search-api/results/overview
from bs4 import BeautifulSoup
import pandas as pd
import re, os, time, shutil
from datetime import datetime
from datetime import timedelta

#variabili
html_file = 'output_html'
html_file_error = 'output_html_error'
output_files = 'output_data'

file_related_searches = 'related_searches.csv'
file_organic_results = 'organic_results.csv'
file_inline_shopping = 'inline_shopping.csv'
file_ads = 'ads.csv'

count_file = 1
if not os.path.exists(output_files):
    os.makedirs(output_files)
if not os.path.exists(html_file_error):
    os.makedirs(html_file_error)

#apertura file html
#filename = 'output_html/20210208-213721-millefiori+milano+diffusore.html'
#file_html = open(filename,encoding='utf-8')
#soup = BeautifulSoup(file_html,'html.parser')
#print(soup)

def soup_from_file(filename):
    file = open(filename,encoding='utf-8')
    soup = BeautifulSoup(file,'html.parser')
    return soup


def get_organic_results():
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
    try: 
        soup = soup_from_file(f'{html_file}/{file}'.format(file=file,html_file=html_file))
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
    except:
        if os.path.isfile(f'{html_file_error}/{file}'):
            print('---- related_searches FILE GIà SPOSTATO')
        else:
            shutil.move(f'{html_file}/{file}',f'{html_file_error}')
            print('---- related_searches FILE SPOSTATO')


def get_related_searches():
    div_obj = {}
    div_obj['Keyword'] = []
    div_obj['Query'] = []
    div_obj['Link'] = []
    try: 
        soup = soup_from_file(f'{html_file}/{file}'.format(file=file,html_file=html_file))
        html_related_searches = soup.find("div", {"class": "card-section"})
        #print(html_relate)
        related_queries = html_related_searches.find_all('a')
        #print(related_queries)
        for related_query in related_queries:
            keyword = soup.find('title').text.strip().split('-')[0]
            #print(keyword)
            div_obj['Keyword'].append(keyword)
            query = re.sub(' +',' ',related_query.text.strip().replace('\n',''))
            #print(query)
            div_obj['Query'].append(query)
            link = related_query.attrs['href']
            #print(link)
            div_obj['Link'].append(link)
        #print(div_obj)
        div_obj_df = pd.DataFrame(div_obj, index=None)
        #print(div_obj_df)
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d-%H")
        div_obj_df.to_csv(f'{output_files}/{dt_string}-{file_related_searches}', mode='a', header=False, index=False, encoding='UTF-8', sep=';')
        print('---- related_searches')
    except:
        if os.path.isfile(f'{html_file_error}/{file}'):
            print('---- related_searches FILE GIà SPOSTATO')
        else:
            shutil.move(f'{html_file}/{file}',f'{html_file_error}')
            print('---- related_searches FILE SPOSTATO')


def get_inline_shopping():
    position = 1
    div_obj = {}
    div_obj['Keyword'] = []
    div_obj['Position'] = []
    div_obj['Titles'] = []
    div_obj['Merchant'] = []
    div_obj['Price'] = []
    div_obj['Value'] = []
    #div_obj['Currency'] = []
    div_obj['Link'] = []

    try:
        soup = soup_from_file(f'{html_file}/{file}'.format(file=file,html_file=html_file))
        html_inline_shopping = soup.find("div", {"class": "cu-container"})
        #print(html_inline_shopping)
        inline_shoppings = html_inline_shopping.find_all('div',class_=['mnr-c', 'pla-unit'])
        #print(inline_shoppings)

        for inline_shopping in inline_shoppings:
            keyword = soup.find('title').text.strip().split('-')[0]
            #print(keyword)
            div_obj['Keyword'].append(keyword)
            #posizione + 1
            div_obj['Position'].append(position)
            #print(position)
            position +=1
            title = inline_shopping.find('a', {'class' : 'plantl pla-unit-title-link'}).text.strip()
            title = re.sub(' +',' ',title.replace('\n',''))
            title = title[:len(title)//2]
            #print(title)
            div_obj['Titles'].append(title)
            merchant = inline_shopping.find('div', {'class' : 'LbUacb'}).text.strip()
            merchant = re.sub(' +',' ',merchant.replace('\n',''))
            merchant = merchant[:len(merchant)//2]
            #print(merchant)
            div_obj['Merchant'].append(merchant)
            price = inline_shopping.find('div', {'class' : 'e10twf T4OwTb'}).text.strip()
            price = re.sub(' +',' ',price.replace('\n',''))
            #print(price)
            div_obj['Price'].append(price)
            only_value = price.replace(",", ".")
            value_comma = re.sub("[^\d\.]", "", only_value)
            value = value_comma.replace(".", ",")
            #print(value)
            div_obj['Value'].append(value)
            #currency = re.sub('[^a-zA-Z]+', '', price)
            #print(currency)
            #div_obj['Currency'].append(currency)
            link = inline_shopping.find('a', {'class' : 'plantl'}).attrs['href']
            #print(link)
            div_obj['Link'].append(link)
        #print(div_obj)
        div_obj_df = pd.DataFrame(div_obj, index=None)
        #print(div_obj_df)
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d-%H")
        div_obj_df.to_csv(f'{output_files}/{dt_string}-{file_inline_shopping}', mode='a', header=False, index=False, encoding='UTF-8', sep=';')
        print('---- inline_shopping')
    except:
        print('---- inline_shopping_skipped')


def get_ads():
    position = 1
    div_obj = {}
    div_obj['Keyword'] = []
    div_obj['Position'] = []
    div_obj['Titles'] = []
    div_obj['Link'] = []
    div_obj['Domain'] = []
    div_obj['Description'] = []


    print('ads')


#lista di file
files = [file for file in os.listdir(html_file) if '.html' in file]
for file in files:
    print(file)
    get_organic_results()
    get_related_searches()
    get_inline_shopping()
    #get_ads()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y-%H")
    timestr_now = str(datetime.now())
    print(timestr_now)
    print(f'----------Numero File Analizzati {count_file}')
    count_file +=1



# #
# #singolo file
# file = '20210209-100641-bidoni+spazzatura.html'
# #print(file)
# #get_related_searches()
# #get_organic_results()
# get_inline_shopping()
# #get_ads()
