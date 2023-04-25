#!/usr/bin/env python3

from YoutubeChannelCrawler import YouTubeChannelCrawler
from DiscordWebhook import DiscordWebhook
from time import sleep

# read all indexed video IDs from file
videos = []
with open('./videoIDs.txt', "r") as file:
    for line in file:
        videos.append(line.rstrip('\n'))
    file.close()

# create Youtube Crawler
channel_id = 'UCP4A1An8dNSxcA8Lj55qVvQ'  # FHTW Podcast
yt_channel = YouTubeChannelCrawler(filepath_yt_api_key='./yt-api-key.txt', yt_channel_id=channel_id)

# create Discord Webhook
discord_webhook = DiscordWebhook(filepath_webhook='./discord-webhook-fhtwpodcast.txt')

while True:
    # crawl for latest video on channel
    latest_video = yt_channel.latest_video()
    # check if a video was found and if it has not been indexed before
    if latest_video is not None and latest_video['videoId'] not in videos:
        # new video on the channel, announce to discord channel
        if discord_webhook.send_msg("Here's the latest FHTW Podcast episode:\n" +\
                                 latest_video['videoTitle'] +\
                                 '\nCheck it out here: ' +\
                                 'https://youtube.com/watch?v=' + latest_video['videoId']):
            # successfully posted to discord channel, therefore add video ID to index
            videos.append(latest_video['videoId'])
            with open('./videoIDs.txt', "a") as file:
                file.write(latest_video['videoId'] + '\n')
                file.close()
    sleep(900)  # hence 15 minutes
