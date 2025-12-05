from django.urls import path

from . import views

urlpatterns = [
    path("grover", views.execute_code, name='grover'),
    path("dj", views.execute_code_dj, name='dj'),
    path("teleportation", views.execute_code_teleportation, name='teleportation'),
    path('get_code_text/', views.get_code_text, name='get_code_text'),
    path('save_new_code/', views.save_new_code, name='save_new_code'),
    path('save_current_code/', views.save_current_code, name='save_current_code'),
    path('contact/', views.contact, name='contact'),
    path('update-code/', views.update_code, name='update_code'),
    path('set_code_name/', views.set_code_name, name='set_code_name'),
    path('get_code_name/', views.get_code_name, name='get_code_name'),
    
]