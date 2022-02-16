import speech_recognition as sr
from os import path
from pydub import AudioSegment
import os
from moviepy.editor import *
import json


selection = input('Input mp4 file to convert? (Y/N): ')

# convert mp4 to mp3 file
if selection.lower() == 'y':
        videopath = input('Enter the mp4 file path: ')
        # video = VideoFileClip(videopath)
        filepath = 'transcript.wav'
        # video.audio.write_audiofile(filepath)
        os.system(f'ffmpeg -i {videopath} -ab 160k -ac 2 -ar 44100 -vn {filepath}')
        # # convert mp3 file to wav    
        # os.system(f'ffmpeg -i {filepath} transcript.wav')
                                                   
        sound = AudioSegment.from_file(filepath, 'wav')

else:
        filepath = input('enter mp3 file path: ')

                                                   
        os.system(f'ffmpeg -i {filepath} transcript.wav')

        filepath = 'transcript.wav'

        # convert mp3 file to wav    
        sound = AudioSegment.from_file(filepath, 'wav')

list_of_transcripts = []
size = (float(os.path.getsize(filepath)) / 1000000)
if size > 3800:
        amt = (float(os.path.getsize(filepath)) / 1000000) / 3800
        fraction = 3.8 / (float(os.path.getsize(filepath) / 1000000))
else:
        amt = (float(os.path.getsize(filepath)) / 1000000) / 3800

count = 0
point_1 = 0
while amt > 1:  
        if count == 0:
                point_2 = len(sound) * fraction
                filename = f'transcript-{count+1}.wav'
                list_of_transcripts.append(filename)   
                sound[:point_2].export(filename, format='wav')
                point_1 = point_2
                amt -= 1
                count += 1
        else:
                point_2 = point_2 + len(sound) * fraction
                filename = f'transcript-{count+1}.wav'
                list_of_transcripts.append(filename)   
                sound[point_1:point_2].export(filename, format='wav')
                point_1 = point_2
                amt -= 1
                count += 1

filename = f'transcript-{count+1}.wav'
list_of_transcripts.append(filename)   
sound[point_1:].export(filename, format='wav')

list_of_files = []
for item in list_of_transcripts:
        amt = (float(os.path.getsize(item)) / 1000000)
        if amt > 10.0:
                amt = (float(os.path.getsize(item)) / 1000000) / 10.0
                fraction = 10.0 / (float(os.path.getsize(item) / 1000000))
        count = 0
        point_1 = 0
        while amt > 1:  
                if count == 0:
                        point_2 = len(sound) * fraction
                        filename = f'wav-{count+1}.wav'
                        list_of_files.append(filename)   
                        sound[:point_2].export(filename, format='wav')
                        point_1 = point_2
                        amt -= 1
                        count += 1
                else:
                        point_2 = point_2 + len(sound) * fraction
                        filename = f'wav-{count+1}.wav'
                        list_of_files.append(filename)   
                        sound[point_1:point_2].export(filename, format='wav')
                        point_1 = point_2
                        amt -= 1
                        count += 1

        filename = f'wav-{count+1}.wav'
        list_of_files.append(filename)   
        sound[point_1:].export(filename, format='wav')

json_file = input('Enter the path to your Google Cloud API Key (json file): ')
# use the audio file as the audio source                                        
r = sr.Recognizer()
# use the audio file as the audio source  
count = 0                                      
for file in list_of_files:
        perc = int((count * 100) / len(list_of_files))
        print(f'{perc}% Completed...', end='\r')
        with sr.AudioFile(file) as source:
                audio = r.record(source)  # read the entire audio file    
                with open(json_file, 'r') as json_content:
                        GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.loads(json_content.read())
        with open('transcript.txt', 'a+') as f:
                f.writelines('\n' + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        count += 1

print('\nCOMPLETE!')