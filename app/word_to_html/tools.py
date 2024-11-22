from django.template.loader import render_to_string
from django.http import HttpResponse
import mammoth

def convert_docx_to_html(file_path):
    with open(file_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

def create_image_html(file_name, image_url):
    return f"""
        <div class="image-container">
            <img src='{image_url}' 
                alt='{file_name}'>
            <div class="image-caption">
                {file_name}
            </div>
        </div>
    """

def create_html_response(html_content, context, filename):
    rendered_html = render_to_string('template.html', context)
    response = HttpResponse(rendered_html, content_type='text/html')
    response['Content-Disposition'] = f'inline; filename="{filename}.html"'
    return response

def get_file_type(filename):
    if filename.endswith(('.docx', '.doc')):
        return 'document'
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return 'image'
    return None
