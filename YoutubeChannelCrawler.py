import googleapiclient.discovery
from googleapiclient.errors import HttpError
# For these imports, install as:
# pip install --upgrade google-api-python-client
# more: https://developers.google.com/youtube/v3/quickstart/python


class YouTubeChannelCrawler:
    yt_resource = None
    yt_playlistId = None

    def __init__(self, filepath_yt_api_key, yt_channel_id):
        # load secret key for the YT API from file
        with open(filepath_yt_api_key, "r") as file_yt_api_key:
            yt_api_key = file_yt_api_key.readline().rstrip('\n')
            file_yt_api_key.close()
        if not yt_api_key:
            # this file had no API key
            return
        self.yt_resource = googleapiclient.discovery.build("youtube", "v3", developerKey=yt_api_key)
        request = self.yt_resource.channels().list(part="contentDetails", id=yt_channel_id)
        response = {}
        try:
            response = request.execute()
        except HttpError:
            # invalid API key
            self.yt_resource = None
        if 'items' in response:
            self.yt_playlistId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        else:
            # invalid channel ID
            self.yt_playlistId = None

    def latest_video(self):
        if self.yt_resource is None:
            # YT resource not ready.
            return None
        request = self.yt_resource.playlistItems().list(part="snippet", playlistId=self.yt_playlistId, maxResults=1)
        try:
            response = request.execute()
        except HttpError:
            # no videos on this channel
            return None
        if 'items' in response:
            video_id = response['items'][0]['snippet']['resourceId']['videoId']
            video_title = response['items'][0]['snippet']['title']
            return {'videoId': video_id, 'videoTitle': video_title}
        else:
            # no videos on this channel
            return None
