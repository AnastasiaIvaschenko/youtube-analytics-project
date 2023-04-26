from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv

load_dotenv()
class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv("API_KEY_YOUTUBE")
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id) -> None:
        self.__channel_id = channel_id #id канала
        self.channel_info = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']#название канала
        self.description = self.channel_info['items'][0]['snippet']['description'] #описание канала
        self.url = "https://www.youtube.com/watch?v=" + channel_id #ссылка на канал
        self.subscribers_count = int(self.channel_info['items'][0]['statistics']['subscriberCount']) #количество подписчиков
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount'] #количество видео
        self.views_count = self.channel_info['items'][0]['statistics']['viewCount'] #общее количество просмотров
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        '''возвращает объект для работы с YouTube API'''
        return cls.youtube


    def to_json(self, name):
        '''сохраняет в файл значения атрибутов экземпляра `Channel`'''
        with open(name, 'w+', encoding="utf-8") as f:
            a = {'channel_id': self.__channel_id,
                 'title': self.title,
                 'description': self.description,
                 'url': self.url,
                 'subscribers_count': self.subscribers_count,
                 'video_count': self.video_count,
                 'views_count': self.views_count}
            json.dump(a, f, ensure_ascii=False)


    def __str__(self):
        return f'{self.title} ({self.url})'


    def __add__(self, other):
        if type(other) == Channel:
            return self.subscribers_count + other.subscribers_count
        else:
            raise TypeError


    def __sub__(self, other):
        return self.subscribers_count - other.subscribers_count

    def __lt__(self, other):
        return self.subscribers_count < other.subscribers_count

    def __le__(self, other):
        return self.subscribers_count <= other.subscribers_count

    def __eq__(self, other):
        return self.subscribers_count == other.subscribers_count







