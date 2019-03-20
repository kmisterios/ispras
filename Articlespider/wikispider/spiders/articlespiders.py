from scrapy.selector import Selector
from scrapy import Spider
from wikispider.items import Article
import json
from datetime import datetime
import locale

def date_format(date_str):
	date_str = date_str.replace('Января', 'Янв')
	date_str = date_str.replace('Февраля', 'Фев')
	date_str = date_str.replace('Марта', 'Мар')
	date_str = date_str.replace('Апреля', 'Апр')
	date_str = date_str.replace('Мая', 'Май')
	date_str = date_str.replace('Июня', 'Июн')
	date_str = date_str.replace('Июля', 'Июл')
	date_str = date_str.replace('Августа', 'Авг')
	date_str = date_str.replace('Сентября', 'Сен')
	date_str = date_str.replace('Октября', 'Окт')
	date_str = date_str.replace('Ноября', 'Ноя')
	date_str = date_str.replace('Декабря', 'Дек')
	return date_str

class ArticleSpider(Spider):
	name = "article"
	allowed_domains = ["www.securitylab.ru"]
	start_urls = ["https://www.securitylab.ru"] #https://www.securitylab.ru/articles/
	
	def parse(self, response):
		link = response.css("div.navigation")[0]
		link = link.css("nav.nav a::attr(href)").get()
		link = response.urljoin(link)
		yield response.follow(link, self.parse_start)
				
	def parse_start(self, response):
		locale.setlocale(locale.LC_ALL, '')
		link = response.css("section.articles")[0]
		ind = 0
		for art in link.css("article.article"):
			date_st = art.css("div.date::text").get()
			date_st = date_format(date_st)
			data = datetime.strptime(date_st, '%H:%M / %d %b, %Y') #for news
			#data = datetime.strptime(date_st, '%d %b, %Y') #for articles
			if data.year == 2018:
				ind = 1
				break
			if data.month == 1:
				artlink = art.css('a::attr(href)').get()
				artlink = response.urljoin(artlink)
				yield response.follow(artlink, self.parse_article)
		link = response.css("div.pagination")[0]
		link = link.css("li.next a::attr(href)").get()
		link = response.urljoin(link)
		if ind == 0:
			yield response.follow(link, self.parse_start)

	def parse_article(self, response):
		item = Article()
		title = response.xpath('//h1/text()')[0].extract()
		link = response.css("article.news-full")[0]
		date = link.css("div.date::text").get()
		datef = date_format(date)
		date = datetime.strptime(datef, '%H:%M / %d %b, %Y')
		#date = datetime.strptime(datef, '%d %b, %Y')
		text = []
		for ar in link.css("div.news-full-content p"):
			text.extend(ar.css("::text").getall())
		links = link.css("div.news-full-content a::attr(href)").getall()
		tags = link.css("small a::attr(href)").getall()
		item['title'] = title
		item['date'] = date
		item['text'] = text
		item['tags'] = tags
		item['links'] = links
		return item		
