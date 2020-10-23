import scrapy
import json
from tabulate import tabulate

class TopAnimeSpider(scrapy.Spider):
    name = "top_50_anime"

    start_urls = [
        'https://myanimelist.net/topanime.php'
    ]

    def parse(self, response):
        # anime_dict = response.css("table.top-ranking-table tr.ranking-list div.clearfix a.hoverinfo_trigger::text") \
        #     .getall()
        anime_dict = response.css("table.top-ranking-table tr.ranking-list div.detail h3.hoverinfo_trigger a::text") \
            .getall()
        filename = 'Top50Anime.txt'
        with open(filename, 'w') as f:
            for index, key in enumerate(anime_dict):
                print('{}. {}\n'.format(index + 1, key))
                f.write('{}. {}\n'.format(index + 1, key))
        self.log('Saved file %s' % filename)


class CompletedAnimeSpider(scrapy.Spider):
    name = "completed_anime"

    start_urls = [
        'https://myanimelist.net/animelist/AmazingAli?status=2&order=4&order2=0'
    ]

    def parse(self, response):
        data_item_string = response.css("table.list-table::attr(data-items)").getall()

        anime_dict_list = json.loads(data_item_string[0])  # Reads the string and converts it into list of dictionaries

        anime_titles = [d['anime_title'] for d in anime_dict_list]
        anime_ratings = [d['score'] for d in anime_dict_list]
        anime_stats = [list(a) for a in zip(anime_titles, anime_ratings)]
        print (anime_stats)
        filename = 'CompletedAnimeList.txt'
        with open(filename, 'w') as f:
            print(tabulate(anime_stats, headers=['Anime Name', 'Rating'], showindex=True, tablefmt='fancy_grid'))
            f.write(tabulate(anime_stats, headers=['Anime Name', 'Rating'], showindex=True, tablefmt='fancy_grid'))
        self.log('Saved file %s' % filename)
