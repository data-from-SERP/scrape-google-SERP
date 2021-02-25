import pandas as pd 
import os

#incollare tutti i file con le 3 colonne related_search in questo file
aggregate_file = 'all_related_keywords.txt'


# creazione dataframe con query univohe e unito con started_query
#
df_related = pd.read_csv('all_related_keywords.txt' , encoding='utf-8', sep=';',names=['Query','Related Keywords', 'Url'],header=None) 
#print(df.head(10)) 
#print(df['Related Keywords'])
related_dataframe = df_related['Related Keywords']
print(related_dataframe)



df_original = pd.read_csv('all_related_keywords.txt' , encoding='utf-8', sep=';',names=['Query','Related Keywords', 'Url'],header=None) 
started_df = df_original['Query']
print(started_df)


new_query = pd.concat([related_dataframe, started_df], ignore_index=True)
#print(new_query)
new_query = new_query.drop_duplicates()
#print(new_query)

#print('ooooooooooooooooooooookkkkkkkkkkkkkkkkkkkkkkkk')

# rimozione started query da new_query
# creo 2 liste e rimuove i valori da una all'altra
list_new_query = new_query.to_list()
#print(list_new_query)
list_started_df = started_df.to_list()
#print(list_started_df)

print('inizio eliminazione kw originale dalle related')
def_query_list = [x for x in list_new_query if x not in list_started_df]

print('inizia a scrivere il primo file')
with open('def_query_list.txt', 'w', encoding='utf-8') as f:
    for item in def_query_list:
        f.write("%s\n" % item)


print('spezzo file')

number_of_files = 3

with open('def_query_list.txt') as infp:
    files = [open('%d.txt' % i, 'w') for i in range(number_of_files)]
    for i, line in enumerate(infp):
        files[i % number_of_files].write(line)
    for f in files:
        f.close()
