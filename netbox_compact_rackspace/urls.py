from django.urls import path
from .views import CompactRackSpaceView

# Имя должно строго совпадать с именем папки-пакета
app_name = 'netbox_compact_rackspace'

urlpatterns = [
    path('', CompactRackSpaceView.as_view(), name='compact_rackspace'),
]
