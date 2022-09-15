from pytube import YouTube

import os
from pathlib import Path
import shutil

from config import ROOT_DIR
from ffmpeg import ffmpeg
from utils import sync_to_async


class Converter:
    '''A class that simply converting audio_file to mp3'''
    def __init__(self, url: str, path: str) -> None:
        self.youtube = YouTube(url)
        self.path = ROOT_DIR / str(path)

        file_path = self._download()
        self._converter(file=file_path)
      
              
    def _download(self) -> Path:
        '''Search and download as webm'''
        os.makedirs(self.path, exist_ok=True)
        file = self.youtube.streams.filter(only_audio=True)[-1].download(self.path) # 160kpbs opus max

        return file

    def _converter(self, file) -> None:
        '''Converting from webp to mp3 with ffmpeg'''
        base, ext = os.path.splitext(file)
        temporary = f'{self.path}/temporary_name{ext}' 

        os.rename(file, temporary)
        name, _ = os.path.splitext(temporary)
    
        os.system(f'{ffmpeg} -i {temporary} -b:a 160k -vn {name}.mp3')
        os.rename(f'{name}.mp3', f'{base}.mp3')
 
  
@sync_to_async
def download(url: str, path: str) -> None:
    Converter(url=url, path=path)
    
@sync_to_async
def clear(path):
    shutil.rmtree(path)
    