#encoding:utf-8
import requests,json,cookielib
from pyquery import PyQuery as pq

class Meican:
	def __init__(self):
		self.loginUrl = 'https://meican.com/login'
		self.headers = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch, br',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Host':'www.zhihu.com',               
                        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                }
        global session
        session = requests.session()

	def getPage(self):
		url = self.loginUrl
		headers = self.headers
		res = session.get(url,headers = headers)
		print res.content

meican = Meican()
meican.getPage()
        