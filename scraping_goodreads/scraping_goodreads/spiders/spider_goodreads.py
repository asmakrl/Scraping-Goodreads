import scrapy
from ..items import ScrapingGoodreadsItem


class GoodreadsSpider( scrapy.Spider ):

  name = 'goodreads'

  page_number = 2

  start_urls = [

    'https://www.goodreads.com/shelf/show/data-science'

    ]
  
  base_url = 'https://www.goodreads.com/'
  
  reviews_ratings = []

  informations = ScrapingGoodreadsItem()

  
  lenBooks = 0
  
  #First parsing method to get the book's link
  def parse(self, response):
    
    books = response.css(".elementList a.bookTitle::attr(href)")
    GoodreadsSpider.lenBooks = len(books)
    for link in books:
      for  page in range(1,11):
        url = GoodreadsSpider.base_url+link.get()+'?page='+str(page)
        yield response.follow(url, callback=self.parse_reviews)
  
  #second parse method to extract informations out of the links
  def parse_reviews(self, response):

    items = ScrapingGoodreadsItem()
    
    #if (GoodreadsSpider.page_number==2):
    title = response.css('#bookTitle::text').extract_first().strip()
    GoodreadsSpider.informations['titles'] = title
    authors = response.css("a.authorName>span ::text").extract_first().strip()
    GoodreadsSpider.informations['authors'] = authors
    global_rating = response.css("#bookMeta span ::text").extract_first().strip()
    GoodreadsSpider.informations['global_rating'] = global_rating
      
    reviews_dict = {}
    GoodreadsSpider.reviews_ratings = []
    review_block = response.css(".review")
   
    for review in review_block:

      if review.css("span[id^='reviewTextContainer'] a") : 
         
        if review.css(".readable span:not(span[id^='freeTextContainer'])") and review.css("span:not(blockquote)"):
           reviews = review.css("span[id^='freeText'] ::text").extract()
        
      
      else:  

        if review.css(".readable span[id^='freeTextContainer'] ") and review.css("span:not(blockquote)"):
          reviews =  review.css("span[id^='freeText'] ::text").extract()
        
      items['review'] = ' '.join([str(item).strip() for item in reviews])
      
      ratings = 0
      
      for span in review.css("span.p10"):
        ratings+=1  
      items['rating'] = ratings

      reviews_dict = {'reviews': items['review'] , 'ratings': items['rating']}
      GoodreadsSpider.reviews_ratings.append(reviews_dict)
      GoodreadsSpider.informations['reviews'] = GoodreadsSpider.reviews_ratings
      
    GoodreadsSpider.informations['reviews'] = GoodreadsSpider.reviews_ratings
    
    yield {'Books' : GoodreadsSpider.informations}


 
      