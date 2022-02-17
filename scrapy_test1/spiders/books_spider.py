import scrapy
import os


BASE_URL = "https://books.toscrape.com/"
CAT_URL = BASE_URL + "catalogue/"


class BooksSpider(scrapy.Spider):
    name = "books_spider"
    start_urls = [
        'https://books.toscrape.com/catalogue/category/books/travel_2/index.html',
    ]

    def parse(self, response):
        books_page_links = response.css("div.side_categories ul li ul li a")
        yield from response.follow_all(books_page_links, self.parse_books)



    def parse_books(self, response):
        pagination_links = response.css("ul.pager li.next a")
        yield from response.follow_all(pagination_links, self.parse_books)
        for book in response.css('article.product_pod'):
            yield {
                'book title': book.css('div.image_container a img::attr(alt)').get(),
                'book price': book.css('div.product_price p.price_color::text').get(),
                'book image URL': BASE_URL + str(book.css('div.image_container a img::attr(src)').re(r"(../../../../+)(.+)")[1]),
                'book details page URL': CAT_URL + str(book.css('div.image_container a::attr(href)').re(r"(../../../+)(.+)")[1]),
            }

# COMMAND TO RUN THE SPIDER
# scrapy crawl books_spider -O books.json

