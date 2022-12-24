import scrapy

from urllib.parse import unquote


class KinopoiskSpider(scrapy.Spider):
    name = 'kinopoisk'
    allowed_domains = ['www.kinopoisk.ru']
    start_urls = ['https://www.kinopoisk.ru/lists/movies/popular/?page=1']

    def parse(self, response, **kwargs):
        for film in response.css('div.styles_root__ti07r'):
            rating = film.css('span.styles_kinopoiskValuePositive__vOb2E::text').get()
            if rating is None:
                rating = film.css('span.styles_kinopoiskValueNeutral__sW9QT::text').get()
            if rating is None:
                rating = film.css('span.styles_kinopoiskValueNegative__Y75Rz::text').get()
            if film.css('span.desktop-list-main-info_secondaryTitle__ighTt::text').get() is None:
                yield {
                    'place': film.css('span.styles_position__TDe4E::text').get(),
                    'name_rus': unquote(film.css('span.styles_mainTitle__IFQyZ::text').get()),
                    'year': str(film.css('span.desktop-list-main-info_secondaryText__M_aus::text').get()).split(",")[0],
                    'rating': rating
                }
            else:
                yield {
                    'place': film.css('span.styles_position__TDe4E::text').get(),
                    'name_rus': unquote(film.css('span.styles_mainTitle__IFQyZ::text').get()),
                    'name_en': film.css('span.desktop-list-main-info_secondaryTitle__ighTt::text').get(),
                    'year':
                        "".join(film.css('span.desktop-list-main-info_secondaryText__M_aus::text').getall()).split(',')[
                            1].strip(),
                    'rating': rating
                }
        next_page = response.css('a.styles_end__aEsmB::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
