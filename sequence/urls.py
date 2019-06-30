from django.urls import path
from sequence import views

urlpatterns = [
    path('short_sequences/<int:pk>/', views.ShortSequenceDetail.as_view()),
    path('short_sequences/<str:tikee>/', views.ShortSequenceList.as_view()),
    path('short_sequences/', views.ShortSequenceCreate.as_view()),

    path('long_sequences/<int:pk>/', views.LongSequenceDetail.as_view()),
    path('long_sequences/<str:tikee>/', views.LongSequenceList.as_view()),
    path('long_sequences/', views.LongSequenceCreate.as_view()),
]
