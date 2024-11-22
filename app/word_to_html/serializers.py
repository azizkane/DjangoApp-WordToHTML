from  rest_framework import serializers
from .models import Converted_Document

class ConvertedDocumentSerializer(serializers.Serializer):
    class Meta :
        Model = Converted_Document
        fields = '__all__'