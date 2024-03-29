import gc
import hashlib
import os
import re
import typing as t

import pandas as pd
import scrapy  # type: ignore

from src.criticker.items import CritickerMoviesItem  # type: ignore


class MoviesSpider(scrapy.Spider):
    name = "movies_spider"
    allowed_domains = ["criticker.com"]

    slugify_spaces_re = re.compile(r"[\s+\=+\-\[\]'\"]")
    slugiry_remove_re = re.compile(r'\[\]{\}\'":;<>\?!@#\$%\^&\*\(\)~`')
    already_harvested: t.Set[str] = set()
    imdb_title_id_re = re.compile(r"title/(\w+)")

    def __init__(self, old_file: str = "", **kwargs):
        if old_file:
            df = pd.read_csv(old_file)
            self.already_harvested = set(
                _.strip("/") for _ in df["url"].astype(str) if _
            )
            del df
            gc.collect()
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        yield scrapy.FormRequest(
            "https://www.criticker.com/authenticate.php",
            formdata={
                "si_username": os.environ["C_USERNAME"],
                "si_password": os.environ["C_PASSWORD"],
                "goto": "https://www.criticker.com/signedout/",
            },
            callback=self._main_page,
            method="POST",
        )

    def _main_page(self, response, **kwargs):
        yield scrapy.Request("https://www.criticker.com/films/", callback=self.parse)

    def parse(
        self, response: scrapy.http.response.Response, **kwargs
    ) -> scrapy.Request:
        """
        Main scrapy parser

        :param response: scrapy response object
        :return: new scrapy request
        """
        for url in response.xpath(
            '//ul[@class="fl_titlelist"]/li/div[@class="fl_name"]/a/@href'
        ):
            url_val = url.extract()
            if url_val and url_val.strip("/") in self.already_harvested:
                continue
            else:
                yield scrapy.Request(
                    url=url_val,
                    callback=self.parse_item,
                    cb_kwargs={"on_netflix": "/netflix/" in response.url},
                )
        next_url = response.xpath(
            '//li[@class="page-item"]/a[text() = "Next"]/@href'
        ).extract_first()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def slugify(self, string: str) -> str:
        """
        Slugify string

        :param string: input string
        :return: slugified string
        """
        string = string.strip().strip(":")
        string = re.sub(self.slugify_spaces_re, "_", string)
        return re.sub(self.slugiry_remove_re, "", string).lower()

    def extract_label_from_id(self, div_id: str) -> str:
        """
        Extract label from div id

        :param div_id: div id value
        :return: label value
        """
        return self.slugify(div_id.split("_")[-1])

    @staticmethod
    def extract_uid_from_url(url: str) -> str:
        """
        Create uid (md5) based on given url

        :param url: item url
        :return: md5 hash
        """
        r = hashlib.md5(url.strip("/").split("/")[-1].encode())
        return r.hexdigest()

    @staticmethod
    def extract_more_info(elem: scrapy.Selector) -> t.Optional[str]:  # type: ignore
        """
        Extract more infos from given scrapy selector

        :param elem: scrapy selector
        :return: basic item infos
        """
        a_ = [_.extract() for _ in elem.xpath('.//*[local-name(.) != "b"]/text()')]
        a = ", ".join([_.strip() for _ in a_ if len(_.strip()) > 1])
        if a:
            return a

    def parse_item(
        self, response: scrapy.http.response.Response, on_netflix
    ) -> CritickerMoviesItem:
        """
        Extract data from given item url

        :param response: scrapy response object
        :param on_netflix: on netflix flag
        :return: Criticker Movies item object
        """
        movie_data = CritickerMoviesItem()
        movie_data["on_netflix"] = int(on_netflix)
        movie_data["url"] = response.url.strip("/")
        movie_data["uid"] = self.extract_uid_from_url(movie_data["url"])
        movie_data["type"] = response.xpath(
            '//*[@id="fi_info_type"]/text()'
        ).extract_first()
        movie_data["name"] = response.xpath(
            '//h1/span[@itemprop="name"]/text()'
        ).extract_first()
        movie_data["date_published"] = response.xpath(
            '//h1/span[@itemprop="datePublished"]/text()'
        ).extract_first()
        movie_data["start_date"] = response.xpath(
            '//h1/span[@itemprop="startDate"]/text()'
        ).extract_first()
        movie_data["end_date"] = response.xpath(
            '//h1/span[@itemprop="endDate"]/text()'
        ).extract_first()
        movie_data["image_urls"] = response.xpath(
            '//div[@id="poster"]/img/@src'
        ).extract_first()
        movie_data["description"] = " ".join(
            [
                _.extract().strip()
                for _ in response.xpath('//span[@itemprop="description"]//text()')
            ]
        ).strip()

        movie_data["imdb_url"] = response.xpath(
            '//p[@class="fi_extrainfo" and contains(., "More information at")]/a[text()="IMDb"]/@href'
        ).extract_first()
        if movie_data.get("imdb_url"):
            movie_data["imdb_title_id"] = re.search(  # type: ignore
                self.imdb_title_id_re, movie_data["imdb_url"]
            ).group(1)

        if not movie_data["description"]:
            movie_data["description"] = None

        more_info_elem = response.xpath('//div[@id="fi_moreinfo"]')

        h = more_info_elem.xpath("./p")

        for i, hi in enumerate(h):
            try:
                hi_ = hi.attrib["id"]
                label = self.extract_label_from_id(hi_)
                if "aka" in label:
                    movie_data[label] = (
                        response.xpath('//p[@id="{}"]/text()'.format(hi_))
                        .extract_first()
                        .replace("AKA: ", "")
                    )
                else:
                    if label in movie_data.fields:
                        movie_data[label] = self.extract_more_info(hi)
            except:
                continue
        movie_data["trailer_url"] = response.xpath(
            '//div[@id="fi_trailer"]/iframe/@src'
        ).extract_first()
        if movie_data["trailer_url"] == "http://www.youtube.com/watch?v=":
            movie_data["trailer_url"] = None
        movie_data["rss_feed_url"] = response.xpath(
            '//*[@id="fi_titlerss"]/a/@href'
        ).extract_first()
        movie_data["avg_percentile"] = response.xpath(
            '//span[@itemprop="ratingValue"]/text()'
        ).extract_first()
        movie_data["n_ratings"] = response.xpath(
            '//span[@itemprop="reviewCount"]/text()'
        ).extract_first()

        return movie_data
