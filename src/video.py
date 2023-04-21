import os
from googleapiclient.discovery import build
import json

class Video:
    api_key = os.getenv("API_KEY_YOUTUBE")
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video = Video.youtube.videos().list(part='snippet,statistics,'
                                                'contentDetails,topicDetails', id=video_id).execute()
        self.title = self.video['items'][0]['snippet']['title'] #название видео
        self.url = "https://www.youtube.com/watch?v=" + video_id #ссылка на видео
        self.view_count = self.video['items'][0]['statistics']['viewCount'] #количество просмотров
        self.like_count = self.video['items'][0]['statistics']['likeCount']  #количество лайков

    def __str__(self):
        return f'{self.title}'
class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id


# vdud = Video('BBotskuyw_M')
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# video3 = Video('PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# print(video3.video)
# print(video3.view_count)
# print(video3.like_count)

