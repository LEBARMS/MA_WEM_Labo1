import scrapy


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia_spider"
    start_urls = ['https://fr.wikipedia.org/wiki/Transformation_de_Fourier']
    page_counter = 0  # Initialize page counter
    max_pages = 10  # Set the maximum number of pages to scrape

    def parse(self, response):
        # Extract headings (from the div containing class 'mw-heading mw-heading2')
        headings = response.css('div.mw-heading.mw-heading2 h2::text').getall()

        # Log extracted headings to see what is being scraped
        self.log(f'Extracted headings from {response.url}: {headings}')

        # Yield the headings if found
        if headings:
            yield {'headings': headings}

        # Limit the number of pages crawled to max_pages
        if self.page_counter < self.max_pages:
            self.page_counter += 1

            # Find all the links to follow (example link for other pages)
            # You can adjust the CSS selector to target specific links as needed
            links_to_follow = response.css('a::attr(href)').getall()

            # Filter out external links and only keep internal Wikipedia links
            for link in links_to_follow:
                if link and link.startswith('/wiki/') and not link.startswith('/wiki/Special:'):
                    next_page = response.urljoin(link)
                    yield response.follow(next_page, self.parse)
