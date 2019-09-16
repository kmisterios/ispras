1) Clean "res1.json" file
2)To run the spyder you have to write the atributes like this:
scrapy crawl article -o res1.json -a start_date=dd.mm.yyyy -a stop_date=dd.mm.yyyy -a type=n (a /na /an)
Where 'n' - for parcing news, 'a' - for parce articles, 'na' и 'an' - for parce articles and news.
