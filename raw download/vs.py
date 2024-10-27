import sys
import time
import threading
import requests

RED = "\033[91m"
RESET = "\033[0m"
GREEN = '\033[92m'

print(GREEN + r'''
           _____      _
 __   ____|_   _|   _| |__   ___
 \ \ / / __|| || | | | '_ \ / _ \
  \ V /\__ \| || |_| | |_) |  __/
   \_/ |___/|_| \__,_|_.__/ \___|

''' + RESET)

def loading(name):
    for _ in range(20):
        sys.stdout.write(RED)
        sys.stdout.write(f'\r{name}.')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write(f'\r{name}..')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write(f'\r{name}...')
        sys.stdout.flush()
        time.sleep(.1)
        sys.stdout.write('\r ')
        sys.stdout.write(RESET)

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']:
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        self.spinner_thread = None
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        percent = 0
        while self.busy:
            sys.stdout.write(next(self.spinner_generator) + f" {percent}%")
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b' * (len(str(percent)) + 1 + 2))
            percent = (percent + 1) % 101

    def start(self):
        self.busy = True
        sys.stdout.write('Downloading ')
        self.spinner_thread = threading.Thread(target=self.spinner_task)
        self.spinner_thread.start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write('\b' * 12)
        sys.stdout.write(' ' * 12)
        sys.stdout.write('\b' * 12)

def fetch_video_details(api_key, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"An error occurred: {response.status_code}")
        return None

def get_video_download_link(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def download_video(video_url, name):
    loading(RED + 'loading' + RESET)
    spinner = Spinner()
    spinner.start()
    try:
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(f"{name}_vstube.mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(GREEN + "Video Download completed with vsTube!")
    except Exception as e:
        print(f"An error occurred while downloading video: {e}")
    finally:
        spinner.stop()

api_key = "YOUR_YOUTUBE_DATA_API_KEY"
video_url = input("Enter the Youtube Link: ")

# Extract video ID from the URL
video_id = video_url.split("v=")[-1]

try:
    video_details = fetch_video_details(api_key, video_id)
    if video_details:
        video_title = video_details['items'][0]['snippet']['title']
        print(f'The Title of the Video is \n {GREEN + video_title + RESET}')
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

print('\n')
name_title = input('Give the name of the video: ')
sys.stdout.flush()
sys.stdout.write('\r ')
print('\n')

try:
    video_download_link = get_video_download_link(video_id)
    download_video(video_download_link, name_title)
except Exception as e:
    print(f"An error occurred: {e}")
