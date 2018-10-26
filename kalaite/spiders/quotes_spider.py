import scrapy
from kalaite.items import KalaiteItem

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	
	def start_requests(self):
		urls = [
			'http://www.lednets.com/zh/News/Company/index.html'
		]
	
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def parse(self,response):
		page = response.url.split('/')[-2]
		filename = 'quotes-%s.html' % page
		with open(filename,"wb") as f:
			f.write(response.body)
		self.log("Saved file %s" % filename)
		for sel in response.xpath('//a'):
			item=KalaiteItem()
			item['title']=sel.xpath('a/text()').extract()
			item['link']=sel.xpath('a/@href').extract()
			item['desc']=sel.xpath('text()').extract()
			yield item

