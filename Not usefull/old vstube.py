import sys
import time
import threading
from pytube import YouTube
import pyperclip

file_path = r'C:\Users\Vivek Saikhom\Downloads\pytube download'

RED = "\033[91m"
RESET = "\033[0m"
GREEN = '\033[92m'


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


def list_available_resolutions(yt):
    video_streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
    vid_resolutions = {stream.resolution for stream in video_streams}
    return sorted(vid_resolutions, reverse=True)


def download_video_at_resolution(yt, res, name, output_path):
    loading(RED + 'loading' + RESET)
    spinner = Spinner()
    spinner.start()
    video_stream = yt.streams.filter(res=res, progressive=True).first()
    if video_stream:
        video_stream.download(output_path=output_path, filename=f'{name}.mp4')
        spinner.stop()
        print(GREEN + "Video Download completed with vsTube!")
    else:
        spinner.stop()
        print(f"No video found at {res} resolution.")


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


def yt_video(name, output_path):
    loading(RED + 'loading' + RESET)
    spinner = Spinner()
    spinner.start()
    video_stream = yts.streams.get_highest_resolution()
    video_stream.download(output_path=output_path, filename=f'{name}.mp4')
    spinner.stop()
    print(GREEN + "Video Download completed with vsTube!" + RESET)


def yt_audio(name, output_path):  # Modified function
    loading(RED + 'loading' + RESET)
    audio_stream = yts.streams.get_audio_only()
    audio_stream.download(output_path=output_path, filename=f'{name}.mp3')
    print(GREEN + 'Audio Download completed with vsTube' + RESET)


video_url = input("Enter the Youtube Link: ")
yts = YouTube(video_url)
print(f'The Title of the Video is \n {GREEN + yts.title + RESET}')
pyperclip.copy(yts.title)


print('\n')
user = input('Enter 1 for High video, 2 for audio, or 3 for video with specific resolution: ')
name_title = input('Give the name of the video or press CTRL + V: ')
sys.stdout.flush()
sys.stdout.write('\r ')
print('\n')

try:
    if user == '1':
        yt_video(name_title, file_path)
    elif user == '2':
        yt_audio(name_title, file_path)
    elif user == '3':
        loading(RED + 'loading Resolution' + RESET)
        resolutions = list_available_resolutions(yts)
        print("Available resolutions: ")

        for resolution in resolutions:
            print(resolution)
        chosen_resolution = input("Enter desired resolution (e.g., 720p): ")
        download_video_at_resolution(yts, chosen_resolution, name_title, file_path)
    else:
        print('Please enter a valid option.')
except Exception as e:
    print(f"An error occurred: {e}")
