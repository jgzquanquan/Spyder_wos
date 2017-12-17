import re
# from threading import Thread
from multiprocessing import Process
from multiprocessing import Manager
import requests
import time
import xlrd
from bs4 import BeautifulSoup
from lxml import etree

class SpiderMain(object):
    def __init__(self, sid, kanming):
        self.hearders = {
            'Origin': 'https://apps.webofknowledge.com',
            'Referer': 'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=R1ZsJrXOFAcTqsL6uqh&preferencesSaved=',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.form_data = {
            'fieldCount': 1,
            'action': 'search',
            'product': 'WOS',
            'search_mode': 'GeneralSearch',
            'SID': sid,
            'max_field_count': 25,
            'formUpdated': 'true',
            'value(input1)': kanming,
            'value(select1)': 'TI',
            'value(hidInput1)': '',
            'limitStatus': 'collapsed',
            'ss_lemmatization': 'On',
            'ss_spellchecking': 'Suggest',
            'SinceLastVisit_UTC': '',
            'SinceLastVisit_DATE': '',
            'period': 'Range Selection',
            'range': 'ALL',
            'startYear': '1982',
            'endYear': '2017',
            'update_back2search_link_param': 'yes',
            'ssStatus': 'display:none',
            'ss_showsuggestions': 'ON',
            'ss_query_language': 'auto',
            'ss_numDefaultGeneralSearchFields': 1,
            'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A'
        }
        self.form_data2 = {
            'product': 'WOS',
            'prev_search_mode': 'CombineSearches',
            'search_mode': 'CombineSearches',
            'SID': sid,
            'action': 'remove',
            'goToPageLoc': 'SearchHistoryTableBanner',
            'currUrl': 'https://apps.webofknowledge.com/WOS_CombineSearches_input.do?SID=' + sid + '&product=WOS&search_mode=CombineSearches',
            'x': 48,
            'y': 9,
            'dSet': 1
        }

    def craw(self, root_url,i):
        try:
            s = requests.Session()
            r = s.post(root_url, data=self.form_data, headers=self.hearders)
            r.encoding = r.apparent_encoding
            tree = etree.HTML(r.text)
            cited = tree.xpath("//div[@class='search-results-data-cite']/a/text()")
            download = tree.xpath(".//div[@class='alum_text']/span/text()")
            flag = 0
            print(i,cited, download,r.url)
            flag=0
            return cited, download, flag
        except Exception as e:
            # 出现错误，再次try，以提高结果成功率
            if i == 0:
                print(e)
                print(i)
                flag = 1
                return cited, download, flag





    def delete_history(self):
        murl = 'https://apps.webofknowledge.com/WOS_CombineSearches.do'
        s = requests.Session()
        s.post(murl, data=self.form_data2, headers=self.hearders)





root_url = 'https://apps.webofknowledge.com/WOS_GeneralSearch.do'

if __name__ == "__main__":
    # sid='6AYLQ8ZFGGVXDTaCTV9'

    root = 'http://www.webofknowledge.com/'
    s = requests.get(root)
    sid = re.findall(r'SID=\w+&', s.url)[0].replace('SID=', '').replace('&', '')

    data = xlrd.open_workbook('2015年研究生发表论文.xlsx')
    table = data.sheets()[2]
    nrows = table.nrows
    ncols = table.ncols
    ctype = 1
    xf = 0
    for i in range(2, nrows):
        csv = open('2015_3.csv', 'a')
        fail = open('fail.txt', 'a')
        if i % 100 == 0:
            # 每一百次更换sid
            s = requests.get(root)
            sid = re.findall(r'SID=\w+&', s.url)[0].replace('SID=', '').replace('&', '')
        kanming = table.cell(i, 5).value
        obj_spider = SpiderMain(sid, kanming)
        cited,download,flag = obj_spider.craw(root_url,i)
        if flag==1:
            fail.write(str(i)+'\n')
        else:
            if len(cited)==0:
                cited.append(0)
                print(cited)
            if len(download)==0:
                download.append(0)
                download.append(0)
                print(download)
        csv.write(str(i) +  ',' + str(cited[0]) + ',' + str(download[0]) + ',' + str(download[1]) +'\n')
        csv.close()