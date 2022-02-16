import speech_recognition as sr
from os import path
from pydub import AudioSegment
import os
from moviepy.editor import *


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

# use the audio file as the audio source                                        
r = sr.Recognizer()
# use the audio file as the audio source  
count = 0                                      
for file in list_of_files:
        perc = int((count * 100) / len(list_of_files))
        print(f'{perc}% Completed...', end='\r')
        with sr.AudioFile(file) as source:
                audio = r.record(source)  # read the entire audio file    
                GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
        "type": "service_account",
        "project_id": "hazel-sphinx-312721",
        "private_key_id": "21264675d24cac75b61e0cf951ee0de2c2897832",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDxKrEQXF55ATg5\nDIKdWCMYkAJNSM7HDzFnt6B6kFBx7hMhpuSQw1GLxFR9ZGgTYcabRkeaNH+L7z50\nl7XzDcIWRSdL5DNEt02zslWdWzxJAUOUFdYkwrV6Wt5JY9aEfi28GoYX8pNS2x/T\n/dBBWhO5ATucnqPNqgCCSJRJSYwSndjngtq1C4NVwZ6BarHowq1J3FN6HrE/0K+0\n4qX347l7J32KQNLk4p8qi7ULU0lBQiMpvhDmYlysh70yR4Ub7cWqPpu5vQfqycUr\n9ORshumQZpclSIFf4syJ6YSEnMRq3aQdOCEaYi8lDuhjslRSeJW4LMMbJdgmSrax\nhOXYnYdrAgMBAAECggEAAs4ZQpRmr1mDctfBkysNVB4y6YtTFbgzBRQXa3rddY+P\n14QVfNY7a2qXITZ3X6gd38N6j2T/QpHN+ziihRdDmSiabD24wkVabmeWHMnUC5/I\nMfFcolZ+GnC6BbhlZTHmTGTAlcDVYmZjEzga79bE4PVHNoClNFNbfdMdEYq19Kd0\nlEqhkFVW/lUgjxh/6HrpU+REhWvOtp1H/5bbtJL8ik6z0zF11tl+SoLFkNoX5rjG\nfEHtr8eMO8wmA27aeYKqsCZUFM4NQeM9EFieQIwYEMeoQ6t2R3nKeOJA5WFlOKwr\ntLQpHzQFK/oyg4sr3gdmGmh5K8hSfM4lULezc/9zQQKBgQD4rbSpagtKx+vamDzp\nfC23bu92pg9JqPNgUN9zchHldcFVPtUeG2Wrp0gryzDi4eI8lhHq+yJGRiZoOn5k\ngeI5lvuV6MaE+IHIC4ruVkRGiDtMQupTGLgbTVdrBvkDVWarEUEJ2Z2xUoCQadgE\nkrELWcH8E4kww+T4xJahXUVGqwKBgQD4RF6c9XhEAgMjt5FDejTdLnEP1KPfmiZo\n5tTPHpQ9E4QTscX/bND+VS1h71TDzAObYD5xIdtZ4VXryWRLtYR5f30U/vvTn44Z\n9hy0abFGg6T7EcZ5kDmK5IZOrPznLamYIC3HVSGUHnrsk7JSLpcnjHm7nmK+U9/a\nLnziY2vCQQKBgB1bnH13qHeenIiE+oPyBg+myBxwxFNE396aDZc6e0Rkn3tp3I0e\nXOVj7VBGP7I5SpUuflUIauZy96vMZAmHj+aOnYr4HR+rmt68Bh3XD15oTN/W8oT2\n4R1QByb6fsFW/rTpZ407JLO/crAZ3sfDbaVSZmVVBRg9uDVqOAI62afbAoGBAKeO\nRSi7xuJnVUUa1DBtXxZUDLx5b+wudnPgLopnAfdCn6ZHGfFsuJSeWhW52ESZAWox\nB5OFHSzJFxsefdFW/cSeVYYBHWbTTa2Z2/+rQZjsqkFE2uYaf6uM1lRtDfbca5Sf\nSyY3/4SfGalneTdb+GoZteL5X31C0FbJf0Gvhf/BAoGAcaCB9W0qTp5jc+eYlsmi\nBMue0sIUb5Wt54nB4/RWEYIaVK+vbNJVwQCumEU3/xVR0IbB5cvhCT85Ta824HDm\nLRWP++7H0b+7JObQL2F4Ni7ZaTZ9ShhQq/pUqNsAGwanqAQNcN5POlumJ932rPtA\nV62XAQlZyd77rljRgfOVeFw=\n-----END PRIVATE KEY-----\n",
        "client_email": "209089118325-compute@developer.gserviceaccount.com",
        "client_id": "109989505865884461974",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/209089118325-compute%40developer.gserviceaccount.com"
        }
        """
        with open('transcript.txt', 'a+') as f:
                f.writelines('\n' + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        count += 1

print('\nCOMPLETE!')