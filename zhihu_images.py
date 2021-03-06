#encoding:utf-8
import requests,os,time,json,cookielib,re
from PIL import Image
from pyquery import PyQuery as pq

class Spider:
        def __init__(self):
                self.homeUrl = 'https://www.zhihu.com'
                self.siteUrl = 'https://www.zhihu.com/question/'
                self.captchaUrl = 'https://www.zhihu.com/captcha.gif'
                self.headers = {
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch, br',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Host':'www.zhihu.com',               
                        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                }
                global session
                session = requests.session()

        #获取xsrf
        def getXsrf(self):
                url = self.homeUrl
                headers = self.headers
                res = session.get(url,headers = self.headers)
                d = pq(res.content)
                xsrf = d("input[name='_xsrf']").attr('value')
                return xsrf

        #获取验证码
        def getCaptcha(self):
                url = self.captchaUrl + '?r=' + str(int(time.time()*1000)) + '&type=login'
                headers = self.headers
                res = session.get(url,headers = headers)
                img = './captcha.gif'
                with open(img,'wb') as f:
                        f.write(res.content)
                print u'请打开captcha.gif文件，填写验证码:'
                im = Image.open(img)
                im.show()               
                captcha = raw_input()
                return captcha

        def getImages(self):
                url = 'https://www.zhihu.com/node/QuestionAnswerListV2'
                headers = self.headers
                offset = 10
                if not os.path.exists('./images'):
                        os.makedirs('./images')
                while(True):
                        params = json.dumps({"url_token":self.num, "pagesize": 10, "offset": offset})
                        data = {'method':'next','_xsrf':self.getXsrf(),'params':params}
                        if offset > self.max_offset:
                                print u'图片爬取结束'
                                exit()
                        res = session.post(url,headers = headers,data = data)
                        listdata = res.json()['msg']
                        if not listdata:
                                print u'图片爬取完毕'
                                return
                        else:
                                print 'The page '+str(offset/10)+' of the image is being crawled'
                                for data in listdata:
                                        d = pq(data)
                                        eles = d(".origin_image.zh-lightbox-thumb.lazy")
                                        for ele in eles:
                                                srcUrl = pq(ele).attr("data-original")
                                                filename = './images/'+os.path.basename(srcUrl)
                                                if not os.path.exists(filename):
                                                        src = requests.get(srcUrl)
                                                        with open(filename,'wb') as img:
                                                                img.write(src.content)
                                                                if os.path.getsize(filename) < self.size:
                                                                        os.remove(filename)
                                offset += 10

        def setValue(self,status):
                if not status:                        
                        username = raw_input("Please enter your username:")
                        password = raw_input('Please enter your password:')
                        self.username = username #用户名
                        self.password = password #密码  
                num = raw_input('Please enter a question number:')
                size = raw_input('Filter the image size(kb):')
                max_page = raw_input('Crawl the total number of pages set:')

                if not num:num = 37709992
                if not size:size = 100
                if not max_page:max_page = 1          

                self.num = num #问题编号
                self.size = int(size)*1000 #文件大小
                self.max_offset = int(max_page)*10 #下载文件总页数的偏移量

        def saveCookies(self):
                with open('./cookies.txt','w') as output:
                        cookies = session.cookies.get_dict()
                        json.dump(cookies,output)
                        print u"成功生成cookie文件:cookies.txt"

        def getCookies(self):
                if os.path.exists('./cookies.txt'):
                        with open('./cookies.txt','r') as f:
                                cookies = json.load(f)
                                session.cookies.update(cookies)
                                return True
                else:
                        print u"cookie文件不存在"
                        return False

        #登录
        def login(self):
                headers = self.headers
                xsrf = self.getXsrf()
                captcha = self.getCaptcha()
                if re.match(r"^1\d{10}$", self.username):
                        type = 'phone_num'
                else:
                        type = 'email'
                url = 'http://www.zhihu.com/login/'+type
                data = {type:self.username,'password':self.password,'_xsrf':xsrf,'captcha':captcha,'remember_me':'true'}
                res = session.post(url,data = data,headers = headers)
                print res.json()['msg']
                self.saveCookies()
                if res.json()['r']==1:
                        print u'登录失败'
                        exit()

        def index(self):
                status = self.getCookies()
                self.setValue(status)
                if not status:self.login()
                self.getImages()


spider = Spider()
spider.index()
