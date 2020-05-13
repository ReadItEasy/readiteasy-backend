from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_book),
    path('book/', views.get_book_chapter),
    path('language-detector/', views.language_detector),
    path('languages/', views.get_languages),
    path('mandarin/', views.get_mandarin_book),
    path('english/', views.get_english_book),
    path('japanese/', views.get_japanese_book),
    # path('user-known-words/', views.get_user_known_words)
]