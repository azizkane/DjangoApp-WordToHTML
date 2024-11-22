from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('convert/', ConvertDocumentView.as_view(), name='convert-document'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

