#encoding:utf8
import urllib2
import cookielib

#获取cookie,并将保存在变量中的cookie打印出来
def Cookie():
	#声明一个CookieJar对象来保存cookie
	cookie = cookielib.CookieJar()
	#创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	#构建opener
	opener = urllib2.build_opener(handler)
	#创建请求
	res = opener.open('http://www.baidu.com')
	for item in cookie:
		print 'name:' + item.name + '-value:' + item.value

#将cookie保存在文件中
def saveCookie():
	#设置保存cookie的文件
	filename = 'cookie.txt'
	#声明一个MozillaCookieJar对象来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	#创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	#构建opener
	opener = urllib2.build_opener(handler)
	#创建请求
	res = opener.open('http://www.baidu.com')
	#保存cookie到文件
	#ignore_discard的意思是即使cookies将被丢弃也将它保存下来
	#ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
	cookie.save(ignore_discard=True,ignore_expires=True)

#从文件中获取cookie并且访问(我们通过这个方法就可以打开保存在本地的cookie来模拟登录)
def getCookie():
	#创建一个MozillaCookieJar对象
	cookie = cookielib.MozillaCookieJar()
	#从文件中的读取cookie内容到变量
	cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
	#打印cookie内容,证明获取cookie成功
	for item in cookie:
		print 'name:' + item.name + '-value:' + item.value
	#利用获取到的cookie创建一个opener
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	res = opener.open('http://www.baidu.com')
	print res.read()