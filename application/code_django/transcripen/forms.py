from django import forms
from .models import *
from .lang_choices import LANG_CHOICES


class AudioForm(forms.ModelForm):
    
    class Meta:
        model = AudioFile
        fields = ['name','upload_file','language',]
        labels = {'name': 'Nom du fichier','language':'Langue de l\'audio','upload_file': "Fichier audio"}
        
    def __init__(self, *args, **kwargs):
        super(AudioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'btmspace-20'
        self.fields['language'] = forms.ChoiceField(choices=LANG_CHOICES,widget=forms.Select(),required=True) 
        
