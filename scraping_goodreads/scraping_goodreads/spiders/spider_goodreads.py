import scrapy
from ..items import ScrapingGoodreadsItem
import requests


class GoodreadsSpider( scrapy.Spider ):

  name = 'goodreads'

  page_number = 2

  start_urls = [
    
    'https://www.goodreads.com/book/show/10210.Jane_Eyre'
    #'https://www.goodreads.com/genres/list'

    ]
    
  reviews_ratings = []

  informations = ScrapingGoodreadsItem()


  # First parse method
  def parse( self, response ):
    
    items = ScrapingGoodreadsItem()
    
    if (GoodreadsSpider.page_number == 2):
      title = response.css('#bookTitle::text').extract_first().strip()
      GoodreadsSpider.informations['titles'] = title

      authors = response.css("a.authorName>span ::text").extract_first().strip()
      GoodreadsSpider.informations['authors'] = authors

      global_rating = response.css("#bookMeta span ::text").extract_first().strip()
      GoodreadsSpider.informations['global_rating'] = global_rating

    
    #description = response.css.css("#description span ::text").extract()
    
    reviews_dict = {}

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
      items['review'] =' '.join([str(item).strip() for item in reviews])
      
      ratings = 0
      
      for span in review.css("span.p10"):
         ratings+=1  
      items['rating'] = ratings

      reviews_dict = {'reviews': items['review'] , 'ratings': items['rating']}
      GoodreadsSpider.reviews_ratings.append(reviews_dict)

    next_page = 'https://www.goodreads.com/book/show/10210.Jane_Eyre?page='+ str(GoodreadsSpider.page_number) 
   
    if response:

      GoodreadsSpider.page_number+=1
      
      yield response.follow(next_page, callback=self.parse)
    
    request = requests.head(next_page)
    code_status = request.status_code
    website_isup = code_status == 400
    print(website_isup)
    if website_isup:
      GoodreadsSpider.informations['reviews'] = GoodreadsSpider.reviews_ratings
      yield {'Books' : GoodreadsSpider.informations}