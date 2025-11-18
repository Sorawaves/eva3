from rest_framework import serializers
from .models import (
    Vehiculo, Aeronave, Conductor, Piloto,
    Ruta, Despacho, Cliente, Carga
)


class VehiculoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Vehiculo"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = ['id', 'tipo', 'tipo_display', 'patente', 'capacidad_kg', 'marca']


class AeronaveSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Aeronave"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Aeronave
        fields = ['id', 'modelo', 'matricula', 'capacidad_kg', 'tipo', 'tipo_display']


class ConductorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Conductor"""
    
    class Meta:
        model = Conductor
        fields = ['id', 'nombre', 'licencia', 'vigente']


class PilotoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Piloto"""
    
    class Meta:
        model = Piloto
        fields = ['id', 'nombre', 'certificacion', 'horas_vuelo']


class RutaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Ruta"""
    tipo_transporte_display = serializers.CharField(source='get_tipo_transporte_display', read_only=True)
    
    class Meta:
        model = Ruta
        fields = ['id', 'origen', 'destino', 'tipo_transporte', 'tipo_transporte_display']


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cliente"""
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'rut', 'direccion']


class CargaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Carga"""
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    
    class Meta:
        model = Carga
        fields = ['id', 'tipo', 'peso_kg', 'valor', 'cliente', 'cliente_nombre']


class DespachoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Despacho"""
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    ruta_detalle = RutaSerializer(source='ruta', read_only=True)
    vehiculo_detalle = VehiculoSerializer(source='vehiculo', read_only=True)
    aeronave_detalle = AeronaveSerializer(source='aeronave', read_only=True)
    conductor_detalle = ConductorSerializer(source='conductor', read_only=True)
    piloto_detalle = PilotoSerializer(source='piloto', read_only=True)
    carga_detalle = CargaSerializer(source='carga', read_only=True)
    
    class Meta:
        model = Despacho
        fields = [
            'id', 'ruta', 'ruta_detalle', 
            'vehiculo', 'vehiculo_detalle',
            'aeronave', 'aeronave_detalle',
            'conductor', 'conductor_detalle',
            'piloto', 'piloto_detalle',
            'carga', 'carga_detalle',
            'estado', 'estado_display',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate(self, data):
        """Validación personalizada para asegurar coherencia entre tipo de transporte y vehículo/aeronave"""
        ruta = data.get('ruta')
        vehiculo = data.get('vehiculo')
        aeronave = data.get('aeronave')
        conductor = data.get('conductor')
        piloto = data.get('piloto')
        
        if ruta:
            if ruta.tipo_transporte == 'TERRESTRE':
                if not vehiculo:
                    raise serializers.ValidationError("Para transporte terrestre se requiere un vehículo")
                if not conductor:
                    raise serializers.ValidationError("Para transporte terrestre se requiere un conductor")
                if aeronave or piloto:
                    raise serializers.ValidationError("El transporte terrestre no puede tener aeronave ni piloto")
            
            elif ruta.tipo_transporte == 'AEREO':
                if not aeronave:
                    raise serializers.ValidationError("Para transporte aéreo se requiere una aeronave")
                if not piloto:
                    raise serializers.ValidationError("Para transporte aéreo se requiere un piloto")
                if vehiculo or conductor:
                    raise serializers.ValidationError("El transporte aéreo no puede tener vehículo ni conductor")
        
        return data
