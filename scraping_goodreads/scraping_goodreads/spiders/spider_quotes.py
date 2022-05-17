import scrapy
from ..items import ScrapingGoodreadsItem


class QuoteSpider( scrapy.Spider ):

  name = 'quotes'

  page_number = 2

  start_urls = [
    
    'https://www.goodreads.com/book/show/10210.Jane_Eyre?page=1'
    
    ]

     
  
  # First parse method
  def parse( self, response ):
    
    items = ScrapingGoodreadsItem()

    #div_title= response.css('div.leftContainer')
    
    #for divs in div_title:

   # title = response.css('#bookTitle::text').extract_first().strip()
    #authors = response.css.css("a.authorName>span ::text").extract_first().strip()
    #description = response.css.css("#description span ::text").extract()
    review_block = response.css(".review")
    for review in review_block:
      reviews = review.css(".readable span ::text").extract()
      
    
      items['reviews'] = reviews

    #items['titles'] = title
    #items['authors'] = authors
    #items['description'] = description
    
      yield items
    
    next_page = 'https://www.goodreads.com/book/show/10210.Jane_Eyre?page='+ str(QuoteSpider.page_number) 
    if QuoteSpider.page_number<=5:
      QuoteSpider.page_number+=1
      
      yield response.follow(next_page, callback=self.parse)
