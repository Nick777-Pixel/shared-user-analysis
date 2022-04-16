#code to figure out what core users are shared across multiple wordpress sites

import csv
import requests
from collections import defaultdict, Counter



#not using yet
# import json
# import lxml
# import altair as alt
# import traceback
# import heapq
# import collections
# from bs4 import BeautifulSoup
# from urllib.request import Request, urlopen
# from urllib.parse import urlparse, urlunparse
# from urllib.error import HTTPError
# import re
# import pandas as pd 



with open('sites.csv') as f:
    reader = csv.reader(f)
    #should probably make this all read the normal layout of csvs as a column not row
    sites = list(reader)[0] 

hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'}

users = []

for url in sites:
    id_num = 0
    fail_num = 0
    success_num = 0 
    #on like globalresearch and prob others bc the id numbers are like 4157 not 1-1000
    #the # after users/ is id not the index in that list tho they're sometimes the same
    print('trying: ' + url)
    print('authors names:')
    site_users_list = []
    try:
        #makes sure the site has this wordpress bug
        full_url = 'http://' + url + '/wp-json/wp/v2/users/'
        r = requests.get(full_url, headers=hdr)
        test = r.json()[0]['name']
        #tries to find the first 1000 authors (bc some numbers are randomly blocked but you have to keep counting)
        for i in range(1000):
            #should try to pass a bunch of failures then stop wasting time 
               # ADD A FEATURE for if fail number = 30 and success number > 2 and <10 then try the old way on users/  
            if fail_num <= 29: #really this should be like 10 in a row not 30 total probably
                try:
                    id_num += 1
                    full_url = 'http://' + url + '/wp-json/wp/v2/users/' + str(id_num)
                    r = requests.get(full_url, headers=hdr)
                    author = r.json()['name']
                    print(author)
                    if author not in users:
                        users.append(author)
                        site_users_list.append(author)

                except:
                    fail_num += 1
                    print(fail_num)
                    pass

    except:
        print(url + ' did not work')
        pass

    try:
        full_url = 'http://' + url + '/wp-json/wp/v2/users/'
        r = requests.get(full_url, headers=hdr)
        response_json = r.json()
        for user in response_json:
            print("TRYING: " + user['name'])
            if user['name'] not in site_users_list:
                print("ADDING UNSEEN USER: " + user['name'])
                site_users_list.append(user['name'])
                users.append(user['name'])
    except Exception as e: print(e)

 
    print(str(len(site_users_list)) + " users found on " + url)
    #add if site users len < 5 bs4 scrape for authors and contributors page


print(Counter(users))

#write results to file except counter is a weird object? check type?
#also store all sites an author was on and a count of how many times they were mentioned as columns

# with open('users_counted.txt', 'w') as f:
#     print(mydictionary, file=f)


#magic method run if main
#put everything into functions