
#智立方爬取某一老师的相关的科研人员信息
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup
import bs4
from lxml import etree
from selenium import webdriver
import time
def geturl(Num):
    Str = "\""+Num+"\""
    driver = webdriver.Chrome()
    url = 'http://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&SID=6FAEOvziD7rmWrbUJk6&search_mode=GeneralSearch'
    driver.get(url)
    driver.find_element_by_id("clearIcon1").click()
    driver.find_element_by_id("value(input1)").send_keys(Num)
    driver.find_element_by_id("WOS_GeneralSearch_input_form_sb").click()
    url1 = driver.current_url
    driver.close()
    return url1
# 该函数用Requests库将网页爬取下来
def getHTMLText(url):
    # 爬取网页的通用代码框架
    try:
        kv = {'user-agent': 'Mozilla/5.0'}#该参数是设置用浏览器的形式访问网站
        r = requests.get(url, headers=kv,timeout=30)#爬取网页生成response对象
        r.raise_for_status()
        r.encoding = r.apparent_encoding#判断是否爬取成功
        return r.text         #返回爬虫的文本内容
    except:
        return ""

def html_parse(html,ID):
    if html is None:
        print("html count:", html)
        return
    try:
        tree = etree.HTML(html)
        re_people=tree.xpath("//div[@class='search-results-data-cite']/a/text()")
        agency=tree.xpath(".//div[@class='alum_text']/span/text()")
        print(re_people,agency)
        Str=""
        if len(re_people)==0:
            Str = "0" + "," + agency[0] + "," + agency[1]

        else:
            Str = re_people[0] + "," + agency[0] + "," + agency[1]
        return Str
    except:
        print(ID)
#把list里信息输出到txt文件中
def Output(uinfo):
    fout = open('WosOutput.txt', 'a', encoding='utf-8')
    for data in uinfo:
        fout.write(data+'\n')
    fout.close()
#解析网页获得对应科研人员的url中的ID
#通过定位该ID可以找到该科研人员各个相关页面


def main():
    uinfo=[]

    queryFile = open("wos1.txt", 'r', encoding='utf-8')
    for query in queryFile:
        fout = open('WosOutput.txt', 'a', encoding='utf-8')
        # 将输入文件中的每一行分割成导师姓名和学校
        splitRes = query.split(',')
        if len(splitRes) != 3:
            print(query, ' 格式不正确')
        else:
            uinfo = []
            ID = query.split(',')[0]
            Name = query.split(',')[1]
            Num = query.split(',')[2][4:-1]
            # new_url = "https://baike.baidu.com/item/"+parse.quote(name)
            # 根据导师姓名和学校构造需要访问的url
            url = geturl(Num)
            html = getHTMLText(url)
            data = html_parse(html,ID)
            Str = str(ID)+","+str(Name)+","+str(Num)+","+str(data)
            print(Str)
            fout.write(Str+ '\n')
            fout.close()

    queryFile.close()

main()