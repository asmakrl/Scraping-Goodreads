import scrapy
from ..items import ScrapingGoodreadsItem


class GoodreadsSpider( scrapy.Spider ):

  name = 'goodreads'

  page_number = 2

  start_urls = [
    
    'https://www.goodreads.com/book/show/10210.Jane_Eyre'
    #'https://www.goodreads.com/genres/list'

    ]

  # First parse method
  def parse( self, response ):
    
    items = ScrapingGoodreadsItem()
    

    title = response.css('#bookTitle::text').extract_first().strip()
    items['titles'] = title

    authors = response.css("a.authorName>span ::text").extract_first().strip()
    items['authors'] = authors

    global_rating = response.css("#bookMeta span ::text").extract_first().strip()
    items['global_rating'] = global_rating

    
    #description = response.css.css("#description span ::text").extract()
    
    
    review_block = response.css(".review")
    
    #if review_block.css(".readable:not(a)"):
   
    for review in review_block:

      if review.css("span[id^='reviewTextContainer'] a") : 
        
         #text_container = review.css(".readable span:not(span[id^='freeTextContainer'])")

         if review.css(".readable span:not(span[id^='freeTextContainer'])") and review.css("span:not(blockquote)"):
           reviews = review.css("span[id^='freeText'] ::text").extract()
        
      
      else:  
        
        #text_container2 = review.css(".readable span[id^='freeTextContainer'] ")

        if review.css(".readable span[id^='freeTextContainer'] ") and review.css("span:not(blockquote)"):
          reviews =  review.css("span[id^='freeText'] ::text").extract()
        

      items['reviews'] =' '.join([str(item).strip() for item in reviews])
      
      ratings = 0
      
      for span in review.css("span.p10"):
         ratings+=1
         
      items['ratings'] = ratings
    
    
    #items['description'] = description
    
      yield items
    
    next_page = 'https://www.goodreads.com/book/show/10210.Jane_Eyre?page='+ str(GoodreadsSpider.page_number) 
   
    if response:

      GoodreadsSpider.page_number+=1
      
      yield response.follow(next_page, callback=self.parse)
