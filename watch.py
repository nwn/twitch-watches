#!/usr/bin/env python3

import tweepy
import urllib.request
from twitchstream.outputvideo import TwitchOutputStreamRepeater
import numpy as np
from time import sleep
from PIL import Image
from argparse import ArgumentParser
from sys import stderr

class Twitter:
    def __init__(self, api_key, api_secret_key):
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        self.api = tweepy.API(auth)

    def pull_image(self, user_id):
        user = self.api.get_user(user_id)
        image_url = user.profile_image_url.replace('_normal', '')
        image = Image.open(urllib.request.urlopen(image_url)).convert("RGB")
        return image

user_id = 'screenshakes'

def __main__():
    parser = ArgumentParser(description='Stream Twitter profile pictures to Twitch')
    parser.add_argument('twitter_key', help='Twitter API key')
    parser.add_argument('twitter_secret_key', help='Twitter API secret key')
    parser.add_argument('twitch_stream_key', help='Twitch stream key')
    args = parser.parse_args()

    twitter = Twitter(args.twitter_key, args.twitter_secret_key)

    width = 1280
    height = 1152
    depth = 3
    with TwitchOutputStreamRepeater(
        twitch_stream_key = args.twitch_stream_key,
        width = width,
        height = height) as video_stream:

        while True:
            try:
                frame = np.negative(np.array(twitter.pull_image(user_id)))
                video_stream.send_video_frame(frame)
            except Exception as err:
                print('Frame error: {}'.format(err), file=stderr)
                continue
            sleep(5)

if __name__ == '__main__':
    __main__()
