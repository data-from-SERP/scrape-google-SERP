import os, time, sqlite3, random, io, urllib
import pandas as pd

from pandas import DataFrame
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from scrape_prepare import create_db_and_folder

create_db_and_folder()

#
# Variabili
uule = 'w+CAIQICIFSXRhbHk'
hl = 'IT'
gl = 'it'
domain_search = 'https://www.google.it/search?q='

config_file = 'config_file'
input_data = 'input_data'
output_html = 'output_html'
teporary_file = 'teporary_file'
file_kw = input_data+'/keywords.txt'
file_proxies = config_file+'/proxies_list.txt'
db_name_keyword = teporary_file+'/Keywords_list.db'
db_name_proxy = teporary_file+'/Proxy_list.db'
test_proxy = 'output_html/test_proxy.txt'

def select_proxy():
    conn = sqlite3.connect(db_name_proxy)
    c = conn.cursor()
    data=pd.read_sql_query("SELECT PROXY FROM PROXY_LIST WHERE TIME = ( SELECT MIN(TIME) FROM PROXY_LIST);",conn)
    #print(type(data['PROXY'].iat[0]))
    global proxy
    proxy = (data['PROXY'].iat[0])
    print(f'---------------------Request IP is {proxy}')
    timestr_now = str(datetime.now())
    #print(timestr_now)
    #global timestr
    timestr = datetime.fromisoformat(timestr_now).timestamp()
    #print(timestr)
    c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr,proxy))
    conn.commit()
    c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr,proxy,))
    conn.commit()
    #print('pausa 1 sec')
    conn.close()

def select_keyword():
    print('-------------------------')
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    data = pd.read_sql_query("SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 LIMIT 1;",conn)
    #print(type(data['KEYWORDS'].iat[0]))
    global keyword
    keyword = (data['KEYWORDS'].iat[0])
    c.execute("Update KEYWORDS_LIST set CHECKING = 1 where KEYWORDS = ?",(keyword,))
    conn.commit()
    conn.close()
    num = random.randint(1,2)
    #print(f'pausa {num} sec')

    #print(keyword)
    global new_keyword
    new_keyword = urllib.parse.quote_plus(keyword)
    #print(new_keyword)


select_proxy()

#
#creazione e apertura browsers
option = webdriver.ChromeOptions()
#Removes navigator.webdriver flag
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
#Proxy
option.add_argument(f'proxy-server={proxy}')
#headless
#option.add_argument("--headless")
#incognito
option.add_argument('--incognito')
#
#creazione e apertura browsers
driver = webdriver.Chrome('./chromedriver',options=option)
driver.maximize_window()
#driver.get(f'https://www.google.it/?hl={hl}&gl={gl}&tci={tci}&uule={uule}&sourceid=chrome&ie=UTF-8')
#print(driver.title)
'''
try:
    iframe = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.find_element_by_xpath('//*[@id="introAgreeButton"]').click()
except:
    print('Accettazione Cookie non richiesta')
'''
num_random_process = random.randint(15,20)
for _ in range(num_random_process):
    select_keyword()
    print(f'new_keyword ------- {new_keyword}')
    #accettazione cookie
    new_url = f'{domain_search}{new_keyword}&oq={new_keyword}&hl={hl}&gl={gl}&uule={uule}&sourceid=chrome&ie=UTF-8'
    #print(new_url)
    driver.get(new_url)
    current_url = driver.current_url
    captcha_url = 'sorry/index?continue'
    print(current_url)
    if captcha_url in current_url:
        print('captcha trovato in URL')
        timestr = time.strftime('%Y%m%d-%H%M%S')
        with open(test_proxy, 'a') as f:
            f.write(f"{proxy};{timestr};Richiesta Captcha;{new_keyword};\n")
            print('file scritto correttamente')
        conn = sqlite3.connect(db_name_keyword)
        c = conn.cursor()
        c.execute("Update KEYWORDS_LIST set CHECKING = 0 where KEYWORDS = ?",(keyword,))
        conn.commit()
        conn.close()
        conn = sqlite3.connect(db_name_proxy)
        c = conn.cursor()
        print('---------------------Proxy da posticipare '+proxy)
        postpone_time = str(datetime.now() + timedelta(hours=2))
        timestr_postpone = datetime.fromisoformat(postpone_time).timestamp()
        c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr_postpone,proxy))
        conn.commit()
        conn.close()
        driver.close()
        exit()
    else:
        print('---------------procediamo')
    
    try:
        iframe = driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        driver.find_element_by_xpath('//*[@id="introAgreeButton"]').click()
        driver.switch_to.default_content()
        print('Accettazione Cookie andata a buon fine')
    except:
        print('Accettazione Cookie non richiesta')
    
    timestr = time.strftime('%Y%m%d-%H%M%S')
    filename = f'{output_html}/{timestr}-{new_keyword}.html'
    print(filename)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    #print(soup)
    #driver.execute_script("window.scrollTo(0, Y)")
    #print('Scroll di pagina effettuato')
    with open(filename, mode="w",  encoding="utf8") as code:
        code.write(str(soup.prettify()))
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #print('Scroll di pagina effettuato')
    if os.path.exists(filename):
        statinfo = os.stat(filename)
        print(statinfo.st_size)
        if statinfo.st_size > 70000:

            #primo controllo
            if soup.find('div',id='introAgreeButton') is None:
                print('YYYYYYYYYY-no introAgreeButton')
            else:
                print('XXXXXXXXXX-introAgreeButton')
                os.remove(filename)
                print('file HTML eliminato correttamente')
                conn = sqlite3.connect(db_name_keyword)
                c = conn.cursor()
                c.execute("Update KEYWORDS_LIST set CHECKING = 0 where KEYWORDS = ?",(keyword,))
                conn.commit()
                conn.close()
                with open(test_proxy, 'a') as f:
                    f.write(f"{proxy};{timestr};Richiesta Fallita;{new_keyword};\n")
                    print('Log scritto correttamente')
                conn = sqlite3.connect(db_name_proxy)
                c = conn.cursor()
                #print(type(data['PROXY'].iat[0]))
                print('---------------------Proxy da posticipare '+proxy)
                postpone_time = str(datetime.now() + timedelta(minutes=5))
                timestr_postpone = datetime.fromisoformat(postpone_time).timestamp()
                c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr_postpone,proxy))
                conn.commit()
                conn.close()
                driver.delete_all_cookies()
                driver.close()
                exit()
                
            #secondo controllo
            if soup.find('div',id='sub-frame-error-details') is None:
                print('YYYYYYYYYY-no sub-frame-error-details')
            else:
                print('XXXXXXXXXX-sub-frame-error-details')
                os.remove(filename)
                print('file HTML eliminato correttamente')
                conn = sqlite3.connect(db_name_keyword)
                c = conn.cursor()
                c.execute("Update KEYWORDS_LIST set CHECKING = 0 where KEYWORDS = ?",(keyword,))
                conn.commit()
                conn.close()
                with open(test_proxy, 'a') as f:
                    f.write(f"{proxy};{timestr};Richiesta Fallita;{new_keyword};\n")
                    print('Log scritto correttamente')
                conn = sqlite3.connect(db_name_proxy)
                c = conn.cursor()
                print('---------------------Proxy da posticipare '+proxy)
                postpone_time = str(datetime.now() + timedelta(minutes=5))
                timestr_postpone = datetime.fromisoformat(postpone_time).timestamp()
                c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr_postpone,proxy))
                conn.commit()
                conn.close()
                driver.delete_all_cookies()
                driver.close()
                exit()

            print('YYYYYYYYYY-no captcha')
            conn = sqlite3.connect(db_name_keyword)
            c = conn.cursor()
            c.execute("Update KEYWORDS_LIST set SUM = 2 where KEYWORDS = ?",(keyword,))
            conn.commit()
            num = random.randint(1,5)
            print("Record Updated successfully ")
            c.close()
            with open(test_proxy, 'a') as f:
                f.write(f"{proxy};{timestr};Esecuzione Corretta;{new_keyword}\n")
                print('file scritto correttamente')
            driver.delete_all_cookies()


        else:
            print('file minore di 70 KB')
            os.remove(filename)
            print('file HTML eliminato correttamente')
            conn = sqlite3.connect(db_name_keyword)
            c = conn.cursor()
            c.execute("Update KEYWORDS_LIST set CHECKING = 0 where KEYWORDS = ?",(keyword,))
            conn.commit()
            conn.close()
            with open(test_proxy, 'a') as f:
                f.write(f"{proxy};{timestr};Richiesta Captcha;{new_keyword};\n")
                print('file scritto correttamente')
            conn = sqlite3.connect(db_name_proxy)
            c = conn.cursor()
            print('---------------------Proxy da posticipare '+proxy)
            postpone_time = str(datetime.now() + timedelta(minutes=50))
            timestr_postpone = datetime.fromisoformat(postpone_time).timestamp()
            c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",(timestr_postpone,proxy))
            conn.commit()
            conn.close()
            driver.delete_all_cookies()
            driver.close()
            exit()

    else:
        print('File non esiste')

print('Keywords scansionata con successo')
driver.delete_all_cookies()
driver.close()
exit()
