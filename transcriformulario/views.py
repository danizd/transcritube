from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import PostForm
from .forms import CanalForm

import pytube
from moviepy.editor import VideoFileClip
import pywhisper
import os
import hashlib
import time

import scrapetube



def download_video(url):
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(18)
    stream.download()
    return stream.default_filename

def convert_to_mp3(filename):
    clip = VideoFileClip(filename)
    clip.audio.write_audiofile(filename[:-4] + ".mp3")
    clip.close()

def AudiotoText(filename):
    model = pywhisper.load_model("base")
    result = model.transcribe(filename)
    print(result["text"])
    sonuc = result["text"]
    return sonuc

def transcribe(link, model):
  m = "base"
  if model != None and model != "":
    m = model
  
  print('''
    Esta herramienta convertirá los vídeos de Youtube en archivos mp3 y luego los transcribirá a texto utilizando Whisper.
    ''')
  print("Descargando video... Por favor, espere.")
  try:
      filename = download_video(link)
  except:
      return "No es un enlace válido..."
  try:
      convert_to_mp3(filename)
  except:
      return "Error de conversión de vídeo a mp3"
  try:
      name = filename[:-4]
      model = pywhisper.load_model( model )
      result = model.transcribe(filename[:-4] + ".mp3")
      result = result["text"]
      print(filename)
      os.remove(filename)
      os.remove(filename[:-4] + ".mp3")
      return result
  except:
      return "Error de transcripción de audio a texto"



def formulario(request):
    start_time = time.time()

    transc = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        enlace = ''
        if form.is_valid():
            form.errors
            enlace = form.cleaned_data.get('enlace')
            filename = download_video(enlace)
            #transc = "--- %s seconds ---" % (time.time() - start_time) +'---------------' + AudiotoText(filename) 
            transc = '<h2>'+filename+'</h2>'+AudiotoText(filename) 

        else:
            enlace = 'noooooo'

    return render(request, 'transcriformulario/formulario.html',  {'transc': transc})


def canal(request):
    listado = []
    canal_id = 'aa'
    if request.method == 'POST':
        form = CanalForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.errors
            canal_id = form.cleaned_data.get('canal')
            print('canal_id '+canal_id)
            '''videos = scrapetube.get_channel('UU9-y-6csu5WGm29I7JiwpnA')
            for video in videos:
                listado = video['videoId']'''



            from urllib.request import urlopen
            
            # import json
            import json

            key = 'AIzaSyALOtM3eKMfAL-y9nh2vANAF9nRRa3ACPE'
            #canal_id = 'UCvsU0EGXN7Su7MfNqcTGNHg'


            url = "https://www.googleapis.com/youtube/v3/search?key=AIzaSyALOtM3eKMfAL-y9nh2vANAF9nRRa3ACPE&channelId="+canal_id+"&part=snippet,id&order=date&maxResults=50"
            

            response = urlopen(url)
            data_json = json.loads(response.read())
            print(url)
            if  'items' in data_json  or len(data_json['items']) != 0:
                for i in data_json['items']:
                    print(i)
                    if  'id' in i or len(i['id']) != 0:
                        if  'videoId' in i['id']:
                            listado.append('<a href="https://www.youtube.com/watch?v='+i['id']['videoId']+'">'+ i['snippet']['title']+'</a>')
            else:
                listado = ['Algo lle pasa a este canal']
 

        else:
            listado = ['noooooo']
        print(listado)
    return render(request, 'transcriformulario/canal.html',  {'listado': listado})



def blogger(request):

    blogger = 'En proceso...'
    return render(request, 'transcriformulario/blogger.html',  {'blogger': blogger})


