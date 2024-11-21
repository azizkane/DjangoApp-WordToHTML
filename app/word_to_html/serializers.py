from  rest_framework import serializers
from .models import ConvertedDocument

class ConvertedDocumentSerializer(serializers.Serializer):
    class Meta :
        Model = ConvertedDocument
        fields = '__all__'