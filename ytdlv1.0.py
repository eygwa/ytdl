import PySimpleGUI as sg      
from pytube import YouTube
import subprocess
import os

#extremely simple download function, adapted from: https://www.kaggle.com/code/aliabdien/youtube-video-and-audio-downloader/
def downloadVideo(url, type):
#todo
    try: yt = YouTube(url)
    except: 
        print('invalid link')
        return "invalid link"
    
    if type=='audio': 
        streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
    else: 
        streams = yt.streams.filter(progressive=True).order_by('resolution').desc()

    qual=streams[0].download() # get highest quality

    print(yt.title+' downloaded')

    if type=='audio':
        try: subprocess.run('ffmpeg -y -i "'+yt.title+'.webm" "'+yt.title+'.mp3"', shell=True)
        except:
            return 'file error, perhaps the mp3 aready exists'
        os.remove(yt.title+'.webm', dir_fd = None)
        
    return "downloaded " + yt.title

#below here is our gui, adapted from simplegui cookbook
sg.theme('DarkAmber')

layout = [[sg.Text('Paste Url Here:')],      
          [sg.Input(key='-IN-')],  
          [sg.Text('output type')],
          [sg.Radio('mp3', True, key='a', default=True), sg.Radio('mp4', True, key='v')],  
          [sg.Button('download'), sg.Exit()],
          [sg.Text('Waiting', key='updates')]]      

window = sg.Window('video downloader', layout)      

while True:                             # The Event Loop
    event, values = window.read() 
    if event=='download':
        window['updates'].update('downloading')
        if(values['a']): type='audio'
        else: type='video'
        ret = downloadVideo(values['-IN-'], type)
        window['updates'].update(ret)
        
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

window.close()