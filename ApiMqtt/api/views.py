from django.shortcuts import render

import paho.mqtt.client as mqtt
from .models import MQTTMessage  # Importa el modelo que definiste en models.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MQTTMessageSerializer  # Importa el serializador

# Crear un cliente MQTT
mqtt_client = mqtt.Client()

# Definir las funciones de callback MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión establecida con éxito.")
        client.subscribe("Octave/Prueba")
    else:
        print(f"Error en la conexión. Código de retorno: {rc}")

def on_message(client, userdata, message):
    topic = "Octave/Prueba"
    payload = message.payload.decode('utf-8')
    print(f"Mensaje recibido en el tópico: {topic}")
    print(f"Contenido del mensaje: {payload}")

    # Guardar el mensaje en la base de datos de Django
    mqtt_message = MQTTMessage(topic=topic, payload=payload)
    mqtt_message.save()

# Asignar las funciones de callback al cliente MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Especificar el broker MQTT y el puerto
broker_address = "192.168.1.201"
port = 1883

# Conectar el cliente al broker
mqtt_client.connect(broker_address, port=port)

# Iniciar el bucle de mensajes del cliente en un hilo separado
mqtt_client.loop_start()


@api_view(['GET'])
def get_mqtt_data(request):
    # Obtener los mensajes MQTT almacenados en la base de datos
    mqtt_messages = MQTTMessage.objects.all()
    data = []
    for message in mqtt_messages:
        data.append({
            'topic': message.topic,
            'payload': message.payload,
            'timestamp': message.timestamp
        })
    return Response(data)

@api_view(['GET'])
def get_mqtt_data(request):
    # Obtener los mensajes MQTT almacenados en la base de datos
    mqtt_messages = MQTTMessage.objects.all()

    # Serializar los objetos MQTTMessage usando el serializador
    serializer = MQTTMessageSerializer(mqtt_messages, many=True)

    return Response(serializer.data)