from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import PostForm

import pytube
from moviepy.editor import VideoFileClip
import pywhisper
import os
import gradio as gr
import hashlib
import time



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
            transc = "--- %s seconds ---" % (time.time() - start_time) +'---------------' + AudiotoText(filename) 

        else:
            enlace = 'noooooo'

    return render(request, 'transcriformulario/formulario.html',  {'transc': transc})


