import scrapy
from RedditScraper.items import RedditscraperItem
import matplotlib.pyplot as plt
import numpy as np

class RedditSpider(scrapy.Spider):
	name = "reddit"
	start_urls = [
	"https://www.reddit.com/r/ucsd",
	"https://www.reddit.com/r/UCSD/?count=25&after=t3_8gf2nr",
	"https://www.reddit.com/r/UCSD/?count=50&after=t3_8g4ljj"
	]

	def parse(self, response):
		words = {}
		for selector in response.xpath("//div[@class='entry unvoted']//div[@class='top-matter']"):
			item = RedditscraperItem()
			item["title"] = selector.xpath("p[@class='title']/a/text()").extract()
			item["link"] = selector.xpath("p[@class='title']/a/@href").extract()
			item["posting_time"] = selector.xpath("p[@class='tagline ']/time/text()").extract()
			for c in selector.xpath("p[@class='title']/a/text()").extract()[0].split():
				if c not in words.keys():
					words[c] = 0
				words[c] += 1
			yield item

		print(words)
		fig = plt.figure(figsize=(18,10))
		plt.bar(range(len(words)), list(words.values()), color='g')
		plt.xticks(range(len(words)), list(words.keys()))
		locs, labels = plt.xticks()
		plt.setp(labels, rotation=90)
		plt.show()

