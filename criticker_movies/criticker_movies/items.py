# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

string_serializer = lambda x: str(x) if x else None
int_serializer = lambda x: int(x) if x else None
float_serializer = lambda x: float(x) if x else None


class CritickerBaseItem(scrapy.Item):
    url = scrapy.Field(serializer=string_serializer)
    name = scrapy.Field(serializer=string_serializer)
    avg_percentile = scrapy.Field(serializer=string_serializer)
    akas = scrapy.Field(serializer=str)
    n_ratings = scrapy.Field(serializer=int_serializer)
    genres = scrapy.Field(serializer=string_serializer)
    type = scrapy.Field(serializer=string_serializer)
    uid = scrapy.Field(serializer=string_serializer)
    trailer_url = scrapy.Field(serializer=string_serializer)
    rss_feed_url = scrapy.Field(serializer=string_serializer)
    poster_url = scrapy.Field(serializer=string_serializer)
    description = scrapy.Field(serializer=string_serializer)
    date_published = scrapy.Field(serializer=int_serializer)
    franchises = scrapy.Field(serializer=string_serializer)


class CritickerGamesItem(CritickerBaseItem):
    platforms = scrapy.Field(serializer=string_serializer)
    developers = scrapy.Field(serializer=string_serializer)
    publishers = scrapy.Field(serializer=string_serializer)
    children = scrapy.Field(serializer=str)


class CritickerMoviesItem(CritickerBaseItem):
    directors = scrapy.Field(serializer=string_serializer)
    creators = scrapy.Field(serializer=string_serializer)
    writers = scrapy.Field(serializer=string_serializer)
    actors = scrapy.Field(serializer=string_serializer)
    on_netflix = scrapy.Field(serializer=int_serializer)
    start_date = scrapy.Field(serializer=int_serializer)
    end_date = scrapy.Field(serializer=int_serializer)

