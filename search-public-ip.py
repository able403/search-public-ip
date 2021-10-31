#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import sys
import json
import queue
import threading
import time
import datetime
q = queue.Queue()
threadnum = 50
keyip=[]
urlkeyip=[]
urlip=[]

domain_list = open("domain.txt").read().splitlines()
for url in domain_list:
    q.put(url)

def run():
    while not q.empty():
        urls = q.get()
        head = {'Connection': 'close', 'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch, br', 'Accept-Language': 'zh-CN,zh;q=0.8', }
        url = 'http://ip-api.com/json/' + urls
        try:
            time.sleep(1)
            requests.packages.urllib3.disable_warnings()
            r = requests.get(url=url, verify=False, headers=head, timeout=3)
            if r.status_code == 200:
                data = r.json()
                ip = data['query']
                location = data['country'] + ' - ' + data['city']
                urldata = urls + '   ' + ip + '  ' + 'country-city:  ' + location + '    '
                urldata =urls    
                if(ip[0:3] in ['111','123','234']):#key ip 
                    print(urls + '   ' + ip + '  ' + 'country-city:  ' + location + '    ')
                    urlkeyip.append(urldata)
                    keyip.append(ip)
                else:
                    urlip.append(urldata)
        except:
            pass 

if __name__ == '__main__':
    print('start search pubic-ip.....')
    start = datetime.datetime.now()
    for i in range(threadnum):
        t = threading.Thread(target=run)
        t.start()
        t.join()
        with open("keyurl.txt", "w") as f:
            for data in urlkeyip:
                f.write(data + "\n")
                with open("allurl.txt", "w") as ff:
                    for data in urlip:
                        ff.write(data + "\n")
    end = datetime.datetime.now()
    print(end-start)


