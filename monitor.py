from scrapyd_api import ScrapydAPI


scrapyd = ScrapydAPI()

print(scrapyd.list_jobs('ScrapyRedisTest'))
print(scrapyd.list_spiders('ScrapyRedisTest'))
scrapyd.schedule('ScrapyRedisTest','jobbole')