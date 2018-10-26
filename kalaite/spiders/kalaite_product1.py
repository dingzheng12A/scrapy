import scrapy
import os
from urllib import request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import response
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from kalaite.items import KalaiteItem
import re
pattern=re.compile(r'src="(.*\.png)"', re.M)
basedir="/Deploy/Devops/templates/dist/"
class DmozSpider(scrapy.Spider):
    name = "spider_product1"
    allowed_domains = ["lednets.com"]
    start_urls = [
        "http://www.lednets.com/zh/News/Express/index.html",
    ]
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.set_page_load_timeout(60)

    def parse_pages(self,response):
        item=KalaiteItem()
        #print("url:%s" % response.url)
        titles=Selector(response).xpath('//div[@class="detailtop"]/h2/text()').extract()
        contents=Selector(response).xpath('//div[@class="detailtxt"]//text()').extract()
        createday=Selector(response).xpath('//div[@class="bdsharebuttonbox"]/span/text()').extract()
        allcontent=Selector(response).xpath('//div[@class="detailtxt"]').extract()
        print("allcontent:%s" % allcontent)
        item['type']="product"
        item['title']=titles
        item['content']=contents
        item['date']=createday
        item['allcontent']=allcontent
        #print("item:%s" % item)
            
	    
        #print("content:%s" %(contents))
        images=Selector(response).xpath('//div[@class="detailtxt"]//img/@src').extract()
        item['img_url']=[]
        for image in images:
            downimage="/".join(image.split("/")[2:])
            print("image:%s downimage:%s" % (image,downimage))
            imgdir=basedir+os.path.dirname(downimage)
            if not image.startswith("http"):
               item['img_url'].append("static/"+downimage)
            else:
               item['img_url'].append("static/"+str(downimage))
            #print("imgdir:%s" % imgdir)
            if not os.path.exists(imgdir):
               os.makedirs(imgdir)
            with open(os.path.join(imgdir,os.path.basename(downimage)),'wb') as f:
                 req=request.urlopen('http://www.lednets.com/'+image)
                 f.write(req.read())
                 f.close()
        yield item
    def parse(self,response):
        url_set = set()
        self.driver.get(response.url)
        next_pages=[]
        while True:
              wait=WebDriverWait(self.driver,20)
              wait.until(lambda driver:driver.find_elements_by_xpath('//a[@class="newmore"]'))
              sel_list=self.driver.find_elements_by_xpath('//a[@class="newmore"]')
              urllist = [ sel.get_attribute("href") for sel in sel_list ]
              url_set |= set(urllist)
              try:
                  wait.until(lambda driver:driver.find_element_by_xpath('//a[@class="laypage_next"]'))           
                  next_page=self.driver.find_element_by_xpath('//a[@class="laypage_next"]')
                  print("next_page:%s" % next_page.get_attribute("href"))
                  next_pages.append(next_page.get_attribute("href"))
                  next_page.click()
              except:
                  print("lasted page receive")
                  break
        with open("urllist.txt","w") as f:
             f.write(repr(url_set))
        f.close()
        for url in url_set:
             yield scrapy.Request(url,callback=self.parse_pages)
