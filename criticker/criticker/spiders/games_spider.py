import scrapy

from .movies_spider import MoviesSpider
from ..items import CritickerGamesItem


class GamesSpider(MoviesSpider):
    name = "games_spider"
    allowed_domains = ["criticker.com"]
    start_urls = ["https://games.criticker.com/games"]

    def parse_item(
        self, response: scrapy.http.response.Response, on_netflix: bool
    ) -> CritickerGamesItem:
        """
        Extract data from given item url
        :param response: scrapy response object
        :return: Criticker Game item object
        """
        game_data = CritickerGamesItem()
        game_data["url"] = response.url.strip("/")
        game_data["uid"] = self.extract_uid_from_url(game_data["url"])
        game_data["type"] = response.xpath(
            '//*[@id="fi_info_type"]/text()'
        ).extract_first()
        game_data["name"] = response.xpath(
            '//h1/span[@itemprop="name"]/text()'
        ).extract_first()
        game_data["date_published"] = response.xpath(
            '//h1/span[@itemprop="datePublished"]/text()'
        ).extract_first()
        game_data["image_urls"] = response.xpath(
            '//div[@id="poster"]/img/@src'
        ).extract_first()
        game_data["description"] = " ".join(
            [
                _.extract().strip()
                for _ in response.xpath('//span[@itemprop="description"]//text()')
            ]
        ).strip()

        if not game_data["description"]:
            game_data["description"] = None
        more_info_elem = response.xpath('//div[@id="fi_moreinfo"]')
        h = more_info_elem.xpath("./p")
        for i, hi in enumerate(h):
            hi_ = hi.attrib["id"]
            label = self.extract_label_from_id(hi_)
            if "aka" in label:
                game_data[label] = response.xpath(
                    '//p[@id="{}"]/text()'.format(hi_)
                ).extract_first()
            else:
                game_data[label] = self.extract_more_info(hi)
        game_data["trailer_url"] = response.xpath(
            '//div[@id="fi_trailer"]/iframe/@src'
        ).extract_first()
        if game_data["trailer_url"] == "http://www.youtube.com/watch?v=":
            game_data["trailer_url"] = None
        game_data["rss_feed_url"] = response.xpath(
            '//*[@id="fi_titlerss"]/a/@href'
        ).extract_first()
        game_data["avg_percentile"] = response.xpath(
            '//span[@itemprop="ratingValue"]/text()'
        ).extract_first()
        game_data["n_ratings"] = response.xpath(
            '//span[@itemprop="reviewCount"]/text()'
        ).extract_first()
        return game_data
