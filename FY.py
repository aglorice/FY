# -*- coding = utf-8 -*-
# @Time :2022/11/11 12:49
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :pythonProject12
# @File :  FY.py
import re
import time

import pymysql as pymysql
import requests
from bs4 import BeautifulSoup


class FY:
    def __init__(self,base_url,city):
        # 网址
        self.base_url = base_url  # 网站的首页地址
        #
        self.city = city
        self.sees = requests.session()  # 实例化会话一个会话对象
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.131 Safari/537.36'}
        # 所有区域的路径
        self.areasPath = []
        # 所有区域的名字
        self.areasName = []
        # 所有的数据

    # 请求页面
    def getUrl(self, url):
        """
        :param url: 待请求的url
        :return: 返回请求的页面
        """
        response = self.sees.get(url, headers=self.headers).text
        souphtml = BeautifulSoup(response, 'html.parser')
        return souphtml

    # 拼接url
    def connectionURL(self, url, path):
        """
        :param url:  需要拼接的url
        :param path: 拼接的部分
        :return: 拼接好的url
        """
        return url + path

    # 去除\t \n
    def clear(self, text):
        """
        :param text: 需要过滤的数据
        :return: 过滤好的数据
        """
        return text.replace('\t', '').replace('\n', '')

    # 获取该区域有多少页
    def getPageNumber(self, response, str):
        """
        :param response: 每个区域的首页面
        :param str: path
        :return: 该区域一共有多少页数
        """
        str = str + 'b'
        try:
            return int(response.find_all('a', class_='last')[0].get('href').replace(str, '').replace('/', ''))
        except Exception as e:
            print(e)
            return 91

    # 数据库
    def saveDb(self, data):
        """
        :param data: 需要保存的数据
        :return: null
        """
        db = pymysql.connect(host="", port=3306, user="root", password="", database="",
                             charset='utf8mb4')  # 连接数据库
        cursor = db.cursor()
        sql = """insert into FY(name, url, address, addressurl, price, area, issell, phone,size,city) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,
                       (
                           data["name"],
                           data["url"],
                           data["address"],
                           data["address_url"],
                           data["price"],
                           data["area"],
                           data["issell"],
                           data["phone"],
                           data['size'],
                           data['city'],
                       ),
                       )
        try:
            db.commit()

        except Exception as e:
            print(e)
        cursor.close()

    # 获取所有区域的path 和 名称
    def getAreas(self):
        """
        获取所有区域的path和名称
        """
        soup = self.getUrl(self.base_url)
        soup = soup.find_all(id="quyu_name")
        for i in soup:
            soup = i.find_all("a")
        for i in soup:
            if i.text == "不限":
                continue
            else:
                self.areasName.append(i.text)
                self.areasPath.append(i.get('href'))

    # 多区域爬取
    def getAllArea(self):
        for i in self.areasPath:
            print("正在爬" + i)
            pageurl = self.connectionURL(self.base_url, i)
            response = self.getUrl(pageurl)
            pagenumber = self.getPageNumber(response, i)

            self.getPages(pagenumber, pageurl, self.areasName[self.areasPath.index(i)])

    # 多页爬取
    def getPages(self, pageNumber, pageurl, pagename):
        """
        :param pageNumber: 爬取页数
        :param pageurl: 爬取区域的url
        :return: 该区域所有的房源数据
        """

        for i in range(91, pageNumber + 1):
            pageurl_1 = pageurl + 'b' + str(i)
            response = self.getPage(pageurl_1, pagename)
            print(response)

    # 单页爬取
    def getPage(self, pageurl, pagename):
        """
        :param pageurl: 该区域的第一页的url
        :return: 该页所有的房源数据
        """
        all_room = []

        url = []
        name = []
        size = []
        address = []
        address_url = []
        price = []
        phone = []
        issell = []

        li_response = ""

        response = self.getUrl(pageurl)

        response = response.find_all(id="newhouse_loupan_list")
        for i in response:
            ul_response = i.find_all("ul")
            for j in ul_response:
                li_response = j.find_all("li")

        # 好多循环啊😭 😭 😭
        for i in li_response:
            for j in i.find_all("div", class_="nlc_details"):
                if "新房已售完" in j.text or "价格待定" in j.text or "400-176" not in j.text:
                    continue
                # 名字
                for k in j.find_all("div", class_='nlcd_name'):
                    for l in k.find_all("a"):
                        url.append(l.get('href'))
                        name.append(self.clear(l.text))
                # 房间大小
                for k in j.find_all('div', class_='house_type clearfix'):
                    size.append(self.clear(k.text))
                # 地址 phone
                for k in j.find_all('div', class_='relative_message clearfix'):
                    for l in k.find_all("a"):
                        address.append(self.clear(l.text))
                        address_url.append(l.get('href'))
                    for l in k.find_all("div", class_='tel'):
                        phone.append(self.clear(l.text))
                # 价格
                for k in j.find_all('div', class_='nhouse_price'):
                    price.append(self.clear(k.text))
                # 出售情况
                for k in j.find_all('div', class_='fangyuan'):
                    for l in k.find_all("span"):
                        issell.append(self.clear(l.text))
        for i in range(len(name)):
            room = {
                'name': name[i],
                'url': url[i],
                'size': size[i],
                'address': address[i],
                'address_url': address_url[i],
                'price': price[i],
                'phone': phone[i],
                'issell': issell[i],
                'area': pagename,
                'city':self.city
            }
            self.saveDb(room)
            all_room.append(room)
        if not all_room:
            return
        return all_room
