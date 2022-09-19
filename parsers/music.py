from bs4 import BeautifulSoup as BS

from urllib.parse import quote
import json 


from requester import Request
from requester.utils import Response
from utils.logger import info


class YoutubeSearch:
    '''Basic youtube searching'''
    _api = 'https://www.youtube.com/results?search_query='

    @classmethod
    async def search(cls, title: str) -> dict:
        
        track_name = title.strip().replace('  ', ' ').replace(' ', '+')
        track_name = quote(track_name, safe='+()', encoding='utf-8') # quoting url 
        url = f'{cls._api}{track_name}'

        response_data = await Request().fetch(url=url)  # getiing response content
        data = cls.get_json(response=response_data)

        return cls.get_data(data=data)

    @staticmethod
    def get_json(response: Response) -> dict | None:
        """
        Fetching json data from youtube searching card and converting response into python dictionary
        """
        if response.content:
            soup = BS(response.content, 'lxml')
            items = soup.select('script[nonce]')
            for item in items:
                if 'var ytInitialData = ' in item.text:
                    return json.loads(item.text.split('var ytInitialData = ')[-1].strip()[:-1])

        raise Exception(f'A site content expected, got {type(response.content).__name__}')

    @staticmethod
    def get_data(data: dict) -> dict:
        '''
        Fetching data from youtube card
        '''
        try:
            fetched_data: dict = {}
            content = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'] \
                ['contents'][0]['itemSectionRenderer']['contents']
            for item in content:
                if len(fetched_data) == 5:
                    break 
                if (video_data := item.get('videoRenderer')): # basic video
                    title = video_data['title']['runs'][0].get('text')
                elif (video_data := item.get('radioRenderer')): # maybe a mix
                    title = video_data['title'].get('simpleText')

                if video_data:
                    url = 'https://www.youtube.com' + video_data['navigationEndpoint']['commandMetadata']['webCommandMetadata'].get('url')
                    fetched_data[url] = title
        except KeyError as key:
            info(f'Got an issue {key} key is not defind')
        else:
            return fetched_data

async def search(title: str) -> dict:
    return await YoutubeSearch.search(title=title)
