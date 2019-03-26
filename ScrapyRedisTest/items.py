# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import scrapy
import re


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def convert_date(value):
    value = value.strip().replace('·', '').replace(' ','')
    try:
        create_time = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.now()

    return create_time


def get_like_nums(value):
    if not value:
        value = 0
    else:
        value = int(value)
    return value


def get_comments_nums(value):
    match_comments = re.match(".*?(\d+).*", value)
    if match_comments:
        comments_nums = match_comments.group(1)
    else:
        comments_nums = '0'

    return int(comments_nums)


def get_fav_nums(value):
    match_fav = re.match(".*?(\d+).*", value)
    if match_fav:
        fav_nums = match_fav.group(1)
    else:
        fav_nums = '0'

    return int(fav_nums)


def remove_comments_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(convert_date)
    )
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    like_nums = scrapy.Field(
        input_processor=MapCompose(get_like_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_fav_nums)
    )
    comments_nums = scrapy.Field(
        input_processor=MapCompose(get_comments_nums)
    )

    tags = scrapy.Field(
        input_processor=MapCompose(remove_comments_tags),
        output_processor=Join(',')
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = 'INSERT INTO article_test(title,url,create_time,url_obj_id,front_image_url,front_image_path,like_nums,fav_nums,comments_nums,tags,content) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)'
        params = (
            self['title'],self['url'],self['create_time'],
            self['url_obj_id'],self['front_image_url'],self['front_image_path'],
            self['like_nums'],self['fav_nums'],self['comments_nums'],
            self['tags'],self['content']
        )
        return insert_sql, params