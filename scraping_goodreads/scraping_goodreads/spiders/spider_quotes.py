import scrapy
from ..items import ScrapingGoodreadsItem


class QuoteSpider( scrapy.Spider ):

  name = 'quotes'
  start_urls = [

      'http://quotes.toscrape.com/'
  ]
    
  
  # First parse method
  def parse( self, response ):

    items = ScrapingGoodreadsItem()

    div_quotes= response.css('div.quote')
    
    for quotes in div_quotes:

      titles = quotes.css('span.text::text').extract()
      authors = quotes.css('small.author::text').extract()
      tags = quotes.css('a.tag::text').extract()

      items['titles'] = titles
      items['authors'] = authors
      items['tags'] = tags

      yield items