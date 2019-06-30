from sequence.models import ShortSequence, LongSequence
from rest_framework import serializers
from rest_framework.exceptions import ParseError

class ShortSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortSequence
        fields = ('id', 'tikee_id', 'name', 'description', 'start', 'interval', 'duration', 'upload_to_cloud', \
            'image_format', 'keep_local_copy', 'sequence_id', 'shooting_status', 'nb_images_on_sd', 'nb_images_uploaded')
    
    def validate_duration(self, value):
        if value <= 0:
            raise ParseError(detail="Duration must be strictly positive", code = ParseError.status_code)
        return value
        
    def validate_intervale(self, value):
        if value <= 0:
            raise ParseError(detail="Intervale must be strictly positive", code = ParseError.status_code)
        return value
        

class LongSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongSequence
        fields = ('id', 'tikee_id', 'name', 'description', 'start', 'end', 'upload_to_cloud','image_format',\
             'keep_local_copy', 'sequence_id', 'shooting_status', 'nb_images_on_sd', 'nb_images_uploaded', 'infinite_duration')

    def validate(self, data):
        if data['start'] > data['end'] and data['infinite_duration'] is False:
            raise serializers.ValidationError("end must occur after start")
        elif data['end'] is None and data['infinite_duration'] is False:
            raise serializers.ValidationError("end must be set")
        return data