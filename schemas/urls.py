from django.urls import path
from .views import *

urlpatterns = [
    path('', SchemaListView.as_view(), name='schemas'),
    path('create/', create_schema, name='create_schema'),
    path('delete/<int:pk>', delete_schema, name='schema_delete'),
    path('update/<int:pk>', update_schema, name='schema_update'),
    path('detail/<int:pk>', SchemaDetailView.as_view(), name='schema_detail'),
    path('delete_column/<int:pk>/', DeleteColumnView.as_view(), name="delete_column"),
    path('download_csv/<int:dataset_id>', download, name='download_csv')
    ]