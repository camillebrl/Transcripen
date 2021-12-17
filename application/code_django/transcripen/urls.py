from django.urls import path

from . import views

urlpatterns = [ 
    path('',views.index,name='index'),
    path('transcript_file/',views.UploadView.as_view(),name='upload_file'),
    #path('rendertext/',views.text_transcript,name='text_transcript'),
    path('rendertext/<int:textfile_id>/',views.FileDetailView.as_view(), name='textfile_detail'),
    path('retrieve_file/', views.contents, name='retrieve')
]
