from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render

from .models import (
    Vehiculo, Aeronave, Conductor, Piloto,
    Ruta, Despacho, Cliente, Carga
)
from .serializers import (
    VehiculoSerializer, AeronaveSerializer, ConductorSerializer,
    PilotoSerializer, RutaSerializer, DespachoSerializer,
    ClienteSerializer, CargaSerializer
)


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar vehículos terrestres.
    Permisos: IsAuthenticatedOrReadOnly (lectura pública, modificación autenticada)
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'marca']
    search_fields = ['patente', 'marca']
    ordering_fields = ['capacidad_kg', 'tipo']


class AeronaveViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar aeronaves.
    Permisos: IsAuthenticatedOrReadOnly (lectura pública, modificación autenticada)
    """
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'modelo']
    search_fields = ['matricula', 'modelo']
    ordering_fields = ['capacidad_kg', 'tipo']


class ConductorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar conductores.
    Permisos: IsAuthenticated (requiere autenticación JWT)
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vigente']
    search_fields = ['nombre', 'licencia']
    ordering_fields = ['nombre']


class PilotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pilotos.
    Permisos: IsAuthenticated (requiere autenticación JWT)
    """
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'certificacion']
    ordering_fields = ['nombre', 'horas_vuelo']


class RutaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar rutas.
    Permisos: IsAuthenticated (requiere autenticación JWT)
    """
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_transporte', 'origen', 'destino']
    search_fields = ['origen', 'destino']
    ordering_fields = ['origen', 'destino']


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes.
    Permisos: IsAuthenticatedOrReadOnly (lectura pública, modificación autenticada)
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'rut']
    ordering_fields = ['nombre']


class CargaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cargas.
    Permisos: IsAuthenticatedOrReadOnly (lectura pública, modificación autenticada)
    """
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cliente', 'tipo']
    search_fields = ['tipo']
    ordering_fields = ['peso_kg', 'valor']


class DespachoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar despachos.
    Permisos: IsAuthenticated (requiere autenticación JWT)
    Filtros: estado, ruta, vehiculo, aeronave, cliente
    """
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'ruta', 'vehiculo', 'aeronave', 'carga__cliente']
    search_fields = ['ruta__origen', 'ruta__destino']
    ordering_fields = ['fecha_creacion', 'estado']


# Vistas de templates HTML para el frontend

def home(request):
    """Vista principal con información general"""
    context = {
        'titulo': 'Logística Global Ltda.',
        'descripcion': 'Sistema de Gestión de Transporte Terrestre y Aéreo'
    }
    return render(request, 'home.html', context)


def vehiculos_list(request):
    """Vista para listar vehículos"""
    vehiculos = Vehiculo.objects.all()
    context = {
        'titulo': 'Vehículos',
        'vehiculos': vehiculos
    }
    return render(request, 'vehiculos.html', context)


def aeronaves_list(request):
    """Vista para listar aeronaves"""
    aeronaves = Aeronave.objects.all()
    context = {
        'titulo': 'Aeronaves',
        'aeronaves': aeronaves
    }
    return render(request, 'aeronaves.html', context)


def rutas_list(request):
    """Vista para listar rutas"""
    rutas = Ruta.objects.all()
    context = {
        'titulo': 'Rutas',
        'rutas': rutas
    }
    return render(request, 'rutas.html', context)


def despachos_list(request):
    """Vista para listar despachos"""
    despachos = Despacho.objects.all()
    context = {
        'titulo': 'Despachos',
        'despachos': despachos
    }
    return render(request, 'despachos.html', context)


def clientes_list(request):
    """Vista para listar clientes"""
    clientes = Cliente.objects.all()
    context = {
        'titulo': 'Clientes',
        'clientes': clientes
    }
    return render(request, 'clientes.html', context)
