from django.contrib import admin
from .models import (
    Vehiculo, Aeronave, Conductor, Piloto,
    Ruta, Despacho, Cliente, Carga
)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['patente', 'tipo', 'marca', 'capacidad_kg']
    list_filter = ['tipo', 'marca']
    search_fields = ['patente', 'marca']


@admin.register(Aeronave)
class AeronaveAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'tipo', 'modelo', 'capacidad_kg']
    list_filter = ['tipo']
    search_fields = ['matricula', 'modelo']


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'licencia', 'vigente']
    list_filter = ['vigente']
    search_fields = ['nombre', 'licencia']


@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'certificacion', 'horas_vuelo']
    search_fields = ['nombre', 'certificacion']
    ordering = ['-horas_vuelo']


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['origen', 'destino', 'tipo_transporte']
    list_filter = ['tipo_transporte']
    search_fields = ['origen', 'destino']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'direccion']
    search_fields = ['nombre', 'rut']


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'peso_kg', 'valor', 'cliente']
    list_filter = ['cliente']
    search_fields = ['tipo']


@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ruta', 'get_transporte', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'ruta__tipo_transporte', 'fecha_creacion']
    search_fields = ['ruta__origen', 'ruta__destino']
    date_hierarchy = 'fecha_creacion'
    
    def get_transporte(self, obj):
        if obj.vehiculo:
            return f"🚛 {obj.vehiculo.patente}"
        elif obj.aeronave:
            return f"✈️ {obj.aeronave.matricula}"
        return "N/A"
    get_transporte.short_description = 'Transporte'
