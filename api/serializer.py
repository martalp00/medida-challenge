from rest_framework import serializers
from .models import Event, EventsRequest, EventsResponse

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsRequest
        fields = '__all__'

class EventsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsResponse
        fields = '__all__'