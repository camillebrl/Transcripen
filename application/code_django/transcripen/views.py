from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import AudioFile, TextFile
from .forms import AudioForm
from .algo_transcript import speech_recognition_algorithm, speech_algorithm
from django.views.generic import *
from django.contrib import messages
from .client_audio import start_client_transmission
from django.views.generic.detail import DetailView
from socket import error as socket_error

# Create your views here.
def detail(request, textfile_id):
    return HttpResponse(" You're at the transcript file: %s." % textfile_id)
    
def index(request):
    latest_file_list = AudioFile.objects.order_by('-add_date')[:5]
    context = {'latest_file_list': latest_file_list}
    return render(request,'index.html',context)
    
def contents(request):
    try:
        start_client_transmission()
        messages.success(request,'Audio bien récupéré dans le dossier Document')
    except socket_error as e:
        messages.error(request,'Problème de connexion. Veuillez à ce que le stylo soit connecté')
    return render(request,'receive.html')
    
"""def text_transcript(request,id,lines):
    audio = AudioFile.objects.get(id=id)
    text = audio.textfile_set.create(name=audio.name+"_transcribed",text_file=lines)
    try:
        text.save()
    except ValueError as e:
    	messages.warning(request,e)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename='+audio.name+"_transcribed"
    response.writelines(lines)
    return response
"""
def textfile_save(id,lines):
    audio = AudioFile.objects.get(id=id)
    text = audio.textfile_set.create(name=audio.name+" ",text_file=lines)
    try:
        text.save()
    except ValueError as e:
    	messages.warning(request,e)
    return text.id

class FileDetailView(View):
    """ def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)"""

    def get(self,request,*args,**kwargs):
        textfile = get_object_or_404(TextFile,pk=kwargs['textfile_id'])
        context = { 'object' : textfile }
        return render(request,'textfile_detail.html', context) 
        
   
        

class UploadView(FormView):
    template_name = 'upload.html'
    form_class = AudioForm
    
    def post(self,request):
        form = AudioForm(request.POST,request.FILES)
        
        try: 
            if form.is_valid():
                try:
                    new_audiofile = form.save()
                    lines = speech_recognition_algorithm(new_audiofile.upload_file,new_audiofile.language)
                    #audio_split = speech_algorithm(new_audiofile.upload_file,new_audiofile.language)
                    #response = text_transcript(request,new_audiofile.id,lines)
                    new_textfile_id = textfile_save(new_audiofile.id,lines)
                    response = redirect(reverse('textfile_detail',kwargs={'textfile_id': new_textfile_id,}))
                except ValueError as e:
                    messsages.warning(request,e)
            else:
                messages.warning(request,"Le formulaire n'est pas valide: "+str(form.errors)) 
                response =  render(request,self.template_name,{'form':form})
        except ValueError as ei:
            messsages.warning(request,ei)
            response =  render(request,'index.html')
                   
        return response
