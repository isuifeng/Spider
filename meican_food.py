#encoding:utf-8
import requests,json,cookielib,time,datetime,smtplib
from pyquery import PyQuery as pq

class Meican:
	def __init__(self):
		isWork = self.isWorkDay()
		if not isWork:
			exit()
		self.loginUrl = 'https://meican.com/account/directlogin'
		self.headers = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch, br',
                        'Accept-Language':'zh-CN,zh;q=0.8',   
                        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                }
        	global session
        	session = requests.session()

	def isWorkDay(self):
    		dayOfWeek = datetime.datetime.now().weekday()
		week = ['周一','周二','周三','周四','周五','周六','周日']
		print week[dayOfWeek]
		if dayOfWeek==5 or dayOfWeek==6:
			return False
		else:
			return True

	def login(self):
    		url = self.loginUrl
	    	headers = self.headers
    		data = {'username':'','loginType':'username','password':'','remember':'true'}
    		res = session.post(url,data = data,headers = headers)
		date = time.strftime('%Y-%m-%d', time.localtime( time.time()))
		#date = '2016-10-20'
		searchUrl = 'https://meican.com/preorder/api/v2.1/calendarItems/list?beginDate=' + date + '&endDate=' + date + '&noHttpGetCache=' + str(int(time.time()*1000)) + '&withOrderDetail=false'
        	r = session.get(url=searchUrl, headers=headers)
		try:
		        status = r.json()['dateList'][0]['calendarItemList'][1]['corpOrderUser']['corpOrderStatus']
		except:
			status = 'no dinner'
		print status
		return
		if status == 'ON_THE_WAY':
			print 'OK'
		elif status == 'no dinner':
			print 'No'

meican = Meican()
meican.login()
        
