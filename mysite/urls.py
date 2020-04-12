from django.urls import path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('resin', views.resin, name='resin'),
    path('output', views.output, name='output'),
]