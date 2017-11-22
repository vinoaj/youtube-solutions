from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen
from PIL import Image
import pandas as pd
import io


class YouTubeVideo:
    def __init__(self, video_id):
        self.video_id = video_id
        self.path_to_thumbnail = self.get_path_to_thumbnail()

    def download_thumbnail(self):
        response = urlopen(self.path_to_thumbnail)
        img = response.read()
        img_io = io.BytesIO(img)

        img_obj = Image.open(img_io)
        img_obj = img_obj.resize((200, 150), Image.LANCZOS)

        filename = 'downloads/youtube-thumbnail-{video_id}.jpg'.format(
            video_id=self.video_id)
        img_obj.save(filename)

    def get_path_to_thumbnail(self, quality='hq'):
        path_pattern = 'https://i.ytimg.com/vi/{video_id}/{quality}default.jpg'
        path = path_pattern.format(video_id=self.video_id, quality=quality)
        return path

    @staticmethod
    def get_video_id_from_url(url):
        """Extract the video ID from a given YouTube URL
           TODO: validate URL is a valid YouTube URL
           TODO: throw exception if no query parameters
           TODO: throw exception if no v query parameter
        """
        url_parts = urlparse(url)
        q_dict = parse_qs(url_parts.query)
        video_id = q_dict['v'][0]
        return video_id


def process_csv(csv_path):
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        url = row['YouTube URL']
        video_id = YouTubeVideo.get_video_id_from_url(url)
        video = YouTubeVideo(video_id)
        video.download_thumbnail()


if __name__ == '__main__':
    process_csv('URLs.csv')