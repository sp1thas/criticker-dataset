# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

string_serializer = lambda x: str(x) if x else None
int_serializer = lambda x: int(x) if x else None
float_serializer = lambda x: float(x) if x else None


class CritickerMoviesItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(serializer=string_serializer)
    name = scrapy.Field(serializer=string_serializer)
    date_published = scrapy.Field(serializer=int_serializer)
    start_date = scrapy.Field(serializer=int_serializer)
    end_date = scrapy.Field(serializer=int_serializer)
    poster_url = scrapy.Field(serializer=string_serializer)
    description = scrapy.Field(serializer=string_serializer)
    genres = scrapy.Field(serializer=string_serializer)
    countries = scrapy.Field(serializer=string_serializer)
    directors = scrapy.Field(serializer=string_serializer)
    creators = scrapy.Field(serializer=string_serializer)
    writers = scrapy.Field(serializer=string_serializer)
    actors = scrapy.Field(serializer=string_serializer)
    trailer_url = scrapy.Field(serializer=string_serializer)
    rss_feed_url = scrapy.Field(serializer=string_serializer)
    avg_percentile = scrapy.Field(serializer=float_serializer)
    n_ratings = scrapy.Field(serializer=int_serializer)
    akas = scrapy.Field(serializer=str)
    type = scrapy.Field(serializer=string_serializer)
    franchises = scrapy.Field(serializer=string_serializer)
    uid = scrapy.Field(serializer=string_serializer)

