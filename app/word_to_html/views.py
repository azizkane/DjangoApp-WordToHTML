from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from pathlib import Path

from .models import Converted_Document
from .serializers import ConvertedDocumentSerializer
from .tools import (
    convert_docx_to_html,
    create_image_html,
    create_html_response,
    get_file_type
)

class ConvertDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        file = request.FILES.get('document')
        if not file:
            return Response({"error": "No document uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_type = get_file_type(file.name)
            if not file_type:
                return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)

            if file_type == 'document':
                file_path = default_storage.save(f"documents_stock/{file.name}", file)
                full_file_path = default_storage.path(file_path)
                html_content = convert_docx_to_html(full_file_path)
            else:
                file_path = default_storage.save(f"img_stock/{file.name}", file)
                html_content = create_image_html(file.name, f'/media/img_stock/{file.name}')

            converted_document = Converted_Document.objects.create(
                document=file,
                original_filename=file.name.lower(),
            )

            context = {
                'html_content': html_content,
                'filename': file.name,
                'file_type': file_type,
                'created_at': converted_document.created_at
            }
            
            return create_html_response(html_content, context, converted_document.original_filename)

        except Exception as e:
            if 'converted_document' in locals():
                converted_document.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentDetailView(APIView):
    def get(self, request, pk):
        document = get_object_or_404(Converted_Document, pk=pk)
        try:
            file_path = document.document.path
            file_type = get_file_type(file_path)
            
            if file_type == 'document':
                html_content = convert_docx_to_html(file_path)
            else:
                html_content = create_image_html(document.original_filename, document.document.url)

            context = {
                'html_content': html_content,
                'filename': document.original_filename,
                'file_type': file_type,
                'created_at': document.created_at
            }

            return create_html_response(html_content, context, document.original_filename)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        document = get_object_or_404(Converted_Document, pk=pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
        
class DocumentListView(APIView):
    def get(self, request):
        documents = Converted_Document.objects.all()
        serializer = ConvertedDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    