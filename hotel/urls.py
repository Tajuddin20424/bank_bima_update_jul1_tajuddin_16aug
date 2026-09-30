from django.urls import path
from . import views


urlpatterns = [

    path('',views.hotel_view,name='hotel'),

    path('save-hotel/',views.save_hotel,name='save_hotel'),

    path('update-hotel/',views.update_hotel,name='update_hotel'),

    path('load-hotel/',views.load_hotel,name='load_hotel'),

    path('delete-hotel/',views.delete_hotel,name='delete_hotel'),

]