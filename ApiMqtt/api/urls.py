from django.urls import path
from .views import get_mqtt_data  # Importa la vista que definiste en views.py

urlpatterns = [
    # Agrega la URL para obtener los datos MQTT a través de la API
    path('mqtt-data/', get_mqtt_data, name='get_mqtt_data'),
  
]
