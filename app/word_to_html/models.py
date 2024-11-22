from django.db import models

class Converted_Document(models.Model):
    def get_upload_path(instance, filename):
        if filename.endswith(('.docx', '.doc')): 
            return f'documents_stock/{filename}'
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif')):
            return f'img_stock/{filename}'

        
    document = models.FileField(upload_to=get_upload_path)
    original_filename = models.CharField(max_length=255, default='file')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.original_filename
    
    
    
    
    class Meta:
        verbose_name = 'Converted Document'
        verbose_name_plural ='Converted Documents'
    