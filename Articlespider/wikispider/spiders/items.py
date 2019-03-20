from scrapy import Item, Field

class Article(Item):
    title = Field()
    date = Field()
    text = Field()
    tags = Field()
