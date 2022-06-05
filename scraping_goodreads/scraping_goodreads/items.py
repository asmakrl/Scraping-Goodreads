# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from optparse import IndentedHelpFormatter
import scrapy


class ScrapingGoodreadsItem(scrapy.Item):
    # define the fields for your item here like:
    titles = scrapy.Field()
    
    authors = scrapy.Field()

    #description = scrapy.Field()
    reviews = scrapy.Field()
    review = scrapy.Field()

    global_rating = scrapy.Field()

    ratings = scrapy.Field()
    rating = scrapy.Field()

    Informations = scrapy.Field()
    reviews_dict = scrapy.Field()
    Books = scrapy.Field()