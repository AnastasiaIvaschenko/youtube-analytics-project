import os
from googleapiclient.discovery import build
import isodate
import datetime


class Playlist:
    api_key = os.getenv("API_KEY_YOUTUBE")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        self.playlist = self.youtube.playlists().list(part="snippet,contentDetails", id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title'] #название плэйлиста
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id #ссылка на плэйлист
        self.playlist_videos = self.youtube.playlistItems().list(  #получить данные по видеороликам в плейлисте
                                            playlistId=playlist_id,
                                            part='contentDetails',
                                            maxResults=50,
                                            ).execute()
        '''получить все id видеороликов из плейлиста'''
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        '''получить информацию о видеороликах из плейлиста по их id (video_id)'''
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=','.join(self.video_ids)
                                               ).execute()

    @property
    def total_duration(self):
         '''возвращает объект класса `datetime.timedelta`
         с суммарной длительность плейлиста (обращение как к свойству, использовать `@property`)'''

         duration_total = datetime.timedelta()

         for video in self.video_response['items']:
             # YouTube video duration is in ISO 8601 format
             iso_8601_duration = video['contentDetails']['duration']
             duration = isodate.parse_duration(iso_8601_duration)
             duration_total += duration
         return duration_total


    def show_best_video(self):
        '''dозвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)'''
        total_likes_count = 0
        url = None
        for video in self.video_response['items']:
            video_id = video['id']
            like_count: int = int(video['statistics']['likeCount'])
            if total_likes_count < like_count:
                url = f'https://youtu.be/{video_id}'

        return url




# playlist1 = Playlist('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
# print(playlist1.video_response)
# likeCount: int = playlist1.video_response['items'][0]['statistics']['likeCount']
# print(likeCount)
# print(playlist1.show_best_video())

