from youtube_transcript_api import YouTubeTranscriptApi
from threading import Thread
import requests
import scrapetube
from bs4 import BeautifulSoup
import readchar
import urllib.request

handle = input('Enter channel handle: ')
query = input('Enter search string: ')

reverse = False
print('Do you want to search by oldest? [y/n]')
if repr(readchar.readkey()) == 'y':
	reverse = True

print('Searching...')

resp = requests.get(f'https://www.youtube.com/@{handle}')
soup = BeautifulSoup(resp.text, 'html.parser')

channel_id = soup.select_one('meta[property="og:url"]')['content'].strip('/').split('/')[-1]

videos = scrapetube.get_channel(channel_id)
videos = list(map(lambda video: video['videoId'], videos))
print('Amount of videos: ' + str(len(videos)))

results = []
videosSearched = 0
if reverse:
	videos.reverse()

def search(video):
	global videosSearched
	videosSearched += 1

	res = YouTubeTranscriptApi.get_transcript(video)

	transcriptArr = list(map(lambda x: x['text'], res))
	transcript = " ".join(transcriptArr).lower()

	if query in transcript:
		results.append(f'https://www.youtube.com/watch?v={video}')

	print(f'Videos searched: {videosSearched}. Videos matched: {len(results)}')


for video in videos:
	t = Thread(target=search, args=(video, ))
	t.daemon = True
	t.start()
	t.join()

print('')
print('==================== Searching complete. ====================')
print('')
if(len(results) == 0):
	print('No results.')

for result in results:
	print(result)
