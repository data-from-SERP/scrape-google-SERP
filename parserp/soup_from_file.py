from bs4 import BeautifulSoup
import __main__

html_file = 'output_html'


def get_soup_from_file(file):
    file_location = html_file+'/'+file
    file = open(file_location,encoding='utf-8')
    print(file)
    global soup
    soup = BeautifulSoup(file,'html.parser')
    #print(soup)
    return soup
