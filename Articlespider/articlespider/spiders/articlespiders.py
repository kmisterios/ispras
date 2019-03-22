import scrapy
from scrapy.selector import Selector
from scrapy import Spider
from articlespider.items import Article
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
	start_urls = ["https://www.securitylab.ru"]
	
	def parse(self, response):
		types = (str)(getattr(self, 'type'))
		link = response.css("div.navigation")[0]
		link1 = link.css("nav.nav a::attr(href)").get()
		link2 = link.css('li.sub')[2]
		link2 = link2.css("div.submenu-inner")
		link2 = link2.css('li a::attr(href)').get() 
		if types == 'n':
			yield response.follow(link1, self.parse_news)
		if types == 'a':
			yield response.follow(link2, self.parse_articles)
		if types == 'na' or types == 'an':
			yield response.follow(link1, self.parse_news)
			yield response.follow(link2, self.parse_articles)
				
	def parse_news(self, response):
		start_date = (str)(getattr(self, 'start_date'))
		stop_date = (str)(getattr(self, 'stop_date')) + ' 23:59'
		start_date = datetime.strptime(start_date, '%d.%m.%Y')
		stop_date = datetime.strptime(stop_date, '%d.%m.%Y %H:%M')
		raz = stop_date - start_date
		qdays = raz.days
		locale.setlocale(locale.LC_ALL, '')
		link = response.css("section.articles")[0]
		for art in link.css("article.article"):
			date_st = art.css("div.date::text").get()
			date_st = date_format(date_st)
			data = datetime.strptime(date_st, '%H:%M / %d %b, %Y')
			if data < start_date:
				return 
			if data <= stop_date:
				artlink = art.css('a::attr(href)').get()
				artlink = response.urljoin(artlink)
				yield response.follow(artlink, self.parse_piece_of_news)
		link = response.css("div.pagination")[0]
		link = link.css("li.next a::attr(href)").get()
		if link:
			yield response.follow(link, self.parse_news)
		else:
			print("YOU HAVE REACHED THE LAST PIECE OF NEWS ON THE RESOURCE!!!")
			return
			
	def parse_piece_of_news(self, response):
		item = Article()
		title = response.xpath('//h1/text()')[0].extract()
		link = response.css("article.news-full")[0]
		date = link.css("div.date::text").get()
		datef = date_format(date)
		date = datetime.strptime(datef, '%H:%M / %d %b, %Y')
		text = '' 
		for ar in link.css("div.news-full-content p"):
			text1 = ar.css("::text").getall()
			for t in text1:
				text = text + t
		links = link.css("div.news-full-content a::attr(href)").getall()
		tags = link.css("small a::attr(href)").getall()
		item['title'] = title
		item['date'] = date
		item['text'] = text
		item['tags'] = tags
		item['links'] = links
		return item
		
	def parse_articles(self, response):
		start_date = (str)(getattr(self, 'start_date'))
		stop_date = (str)(getattr(self, 'stop_date')) + ' 23:59'
		start_date = datetime.strptime(start_date, '%d.%m.%Y')
		stop_date = datetime.strptime(stop_date, '%d.%m.%Y %H:%M')
		raz = stop_date - start_date
		qdays = raz.days
		locale.setlocale(locale.LC_ALL, '')
		link = response.css("section.articles")[0]
		for art in link.css("article.article"):
			date_st = art.css("div.date::text").get()
			date_st = date_format(date_st)
			data = datetime.strptime(date_st, '%d %b, %Y')
			if data < start_date:
				return 
			if data <= stop_date:
				artlink = art.css('a::attr(href)').get()
				artlink = response.urljoin(artlink)
				yield response.follow(artlink, self.parse_article)
		link = response.css("div.pagination")[0]
		link = link.css("li.next a::attr(href)").get()
		if link:
			yield response.follow(link, self.parse_articles)
		else:
			print("YOU HAVE REACHED THE LAST ARTICLE ON THE RESOURCE!!!")
			return
			
	def parse_article(self, response):
		item = Article()
		title = response.xpath('//h1/text()')[0].extract()
		link = response.css("article.news-full")[0]
		date = link.css("div.date::text").get()
		datef = date_format(date)
		date = datetime.strptime(datef, '%d.%m.%Y')
		text = ''
		author = ''
		for ar in link.css("div.news-full-content p"):
			text1 = ar.css("::text").getall()
			for t in text1:
				text = text + t			
		if link.css("div.news-full-content p b::text").get():
			author = link.css("div.news-full-content p::text")[1].get()
			text = text.replace(' Автор:' + author +'\r\n','')
			author = author.replace('\r','')
			author = author.replace('\n',' ')
		links = link.css("div.news-full-content a::attr(href)").getall()
		item['title'] = title
		item['date'] = date
		item['text'] = text
		item['links'] = links
		item['author'] = author
		return item		
