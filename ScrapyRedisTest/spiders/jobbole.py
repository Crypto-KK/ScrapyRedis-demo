from urllib import parse

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from ScrapyRedisTest.items import JobboleArticleItem, ArticleItemLoader
from ScrapyRedisTest.utils.common import get_md5


class MySpider(RedisSpider):
    name = 'jobbole'
    redis_key = 'jobbole:start_urls'
    allowed_domains = ['blog.jobbole.com']

    def parse(self, response):
        """
        获取列表页中的url，并交给解析函数
        """
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first()
            post_url = post_node.css('::attr(href)').extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):

        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)

        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_obj_id', get_md5(response.url))
        item_loader.add_xpath('create_time', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url', response.meta.get('front_image_url', ''))
        item_loader.add_xpath('like_nums', '//span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath('fav_nums', '//span[contains(@class, "bookmark-btn")]/text()')
        item_loader.add_xpath('comments_nums', '//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath('content', '//div[@class="entry"]')
        item_loader.add_xpath('tags', '//p[@class="entry-meta-hide-on-mobile"]/a/text()')

        article_item = item_loader.load_item()

        yield article_item