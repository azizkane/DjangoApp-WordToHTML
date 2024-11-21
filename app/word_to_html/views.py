from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

from .models import ConvertedDocument
from .serializers import ConvertedDocumentSerializer

import mammoth
from PIL import Image
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

class ConvertDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        file = request.FILES.get('document')
        if not file:
            return Response({"error": "No document uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Handle different file types
            if file.name.endswith(('.docx', '.doc')):
                file_path = default_storage.save(f"documents_stock/{file.name}", file)
                full_file_path = default_storage.path(file_path)
                
                with open(full_file_path, 'rb') as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html_content = result.value
                    
            elif file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = default_storage.save(f"img_stock/{file.name}", file)
                image = Image.open(default_storage.path(file_path))
                
                html_content = f"""
                    <div class="image-container">
                        <img src='/media/img_stock/{file.name}' 
                            alt='{file.name}'>
                        <div class="image-caption">
                            {file.name}
                        </div>
                    </div>
                """

            else:
                return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)

            # Save to database
            converted_document = ConvertedDocument.objects.create(
                document=file,
                original_filename=file.name.lower(),
            )


            # Enhanced template context
            context = {
                'html_content': html_content,
                'filename': file.name,
                'file_type': 'document' if file.name.endswith(('.docx', '.doc')) else 'image',
                'created_at': converted_document.created_at
            }
            
            # rendered_html = render_to_string('C:/xampp/htdocs/dev/django\WordToHTML/app/word_to_html/templates/template.html', context)
            rendered_html = render_to_string('../templates/template.html', context)  # Relative path example
            response = HttpResponse(rendered_html, content_type='text/html')
            response['Content-Disposition'] = f'inline; filename="{converted_document.original_filename}.html"'
            return response

        except Exception as e:
            if 'converted_document' in locals():
                converted_document.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class DocumentListView(APIView):
    def get(self, request):
        documents = ConvertedDocument.objects.all()
        serializer = ConvertedDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
class DocumentDetailView(APIView):
    def get(self, request, pk):
        document = get_object_or_404(ConvertedDocument, pk=pk)
        try:
            file_path = document.document.path
            
            if file_path.endswith(('.docx', '.doc')):
                with open(file_path, 'rb') as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    html_content = result.value
                    
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                html_content = f"""
                    <div class="image-container">
                        <img src='{document.document.url}' 
                             alt='{document.original_filename}'>
                        <div class="image-caption">
                            {document.original_filename}
                        </div>
                    </div>
                """
            else:
                raise ValueError("Unsupported file type.")

            context = {
                'html_content': html_content,
                'filename': document.original_filename,
                'file_type': 'document' if file_path.endswith(('.docx', '.doc')) else 'image',
                'created_at': document.created_at
            }

            rendered_html = render_to_string('template.html', context)
            response = HttpResponse(rendered_html, content_type='text/html')
            response['Content-Disposition'] = f'inline; filename="{document.original_filename}.html"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        document = get_object_or_404(ConvertedDocument, pk=pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
