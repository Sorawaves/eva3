from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para la API REST
router = DefaultRouter()
router.register(r'vehiculos', views.VehiculoViewSet, basename='vehiculo')
router.register(r'aeronaves', views.AeronaveViewSet, basename='aeronave')
router.register(r'conductores', views.ConductorViewSet, basename='conductor')
router.register(r'pilotos', views.PilotoViewSet, basename='piloto')
router.register(r'rutas', views.RutaViewSet, basename='ruta')
router.register(r'clientes', views.ClienteViewSet, basename='cliente')
router.register(r'cargas', views.CargaViewSet, basename='carga')
router.register(r'despachos', views.DespachoViewSet, basename='despacho')

# URLs combinadas: API y Templates
urlpatterns = [
    # API REST endpoints
    path('api/', include(router.urls)),
    
    # Vistas HTML con templates
    path('', views.home, name='home'),
    path('vehiculos/', views.vehiculos_list, name='vehiculos_list'),
    path('aeronaves/', views.aeronaves_list, name='aeronaves_list'),
    path('rutas/', views.rutas_list, name='rutas_list'),
    path('despachos/', views.despachos_list, name='despachos_list'),
    path('clientes/', views.clientes_list, name='clientes_list'),
]
