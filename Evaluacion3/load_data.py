"""
Script para cargar datos iniciales en la base de datos
Ejecutar con: python manage.py shell < load_data.py
O desde el shell de Django:
    python manage.py shell
    >>> exec(open('load_data.py').read())
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistica.settings')
django.setup()

from transporte.models import (
    Vehiculo, Aeronave, Conductor, Piloto,
    Ruta, Cliente, Carga, Despacho
)
from django.contrib.auth.models import User

def cargar_datos():
    print("🔄 Iniciando carga de datos de ejemplo...")
    
    # Limpiar datos existentes (opcional, comentar si no deseas borrar)
    # Despacho.objects.all().delete()
    # Carga.objects.all().delete()
    # Cliente.objects.all().delete()
    # Ruta.objects.all().delete()
    # Piloto.objects.all().delete()
    # Conductor.objects.all().delete()
    # Aeronave.objects.all().delete()
    # Vehiculo.objects.all().delete()
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@logisticaglobal.cl',
            password='admin123'
        )
        print("✅ Superusuario creado (usuario: admin, contraseña: admin123)")
    
    # 1. Crear Vehículos
    print("\n📦 Creando vehículos...")
    vehiculos_data = [
        {'tipo': 'CAMION', 'patente': 'ABCD12', 'capacidad_kg': 15000.00, 'marca': 'Mercedes-Benz'},
        {'tipo': 'CAMION', 'patente': 'EFGH34', 'capacidad_kg': 20000.00, 'marca': 'Volvo'},
        {'tipo': 'FURGON', 'patente': 'IJKL56', 'capacidad_kg': 2500.00, 'marca': 'Ford Transit'},
        {'tipo': 'FURGON', 'patente': 'MNOP78', 'capacidad_kg': 3000.00, 'marca': 'Renault Master'},
        {'tipo': 'BUS', 'patente': 'QRST90', 'capacidad_kg': 5000.00, 'marca': 'Scania'},
    ]
    vehiculos = []
    for data in vehiculos_data:
        vehiculo, created = Vehiculo.objects.get_or_create(
            patente=data['patente'],
            defaults=data
        )
        vehiculos.append(vehiculo)
        if created:
            print(f"  ✅ Vehículo {data['patente']} creado")
        else:
            print(f"  ℹ️  Vehículo {data['patente']} ya existe")
    print(f"✅ Total: {len(vehiculos)} vehículos")
    
    # 2. Crear Aeronaves
    print("\n✈️ Creando aeronaves...")
    aeronaves_data = [
        {'modelo': 'Boeing 737', 'matricula': 'CC-ABC', 'capacidad_kg': 50000.00, 'tipo': 'AVION'},
        {'modelo': 'Cessna 208', 'matricula': 'CC-DEF', 'capacidad_kg': 1500.00, 'tipo': 'AVION'},
        {'modelo': 'Bell 407', 'matricula': 'CC-GHI', 'capacidad_kg': 800.00, 'tipo': 'HELICOPTERO'},
        {'modelo': 'Airbus A320', 'matricula': 'CC-JKL', 'capacidad_kg': 45000.00, 'tipo': 'AVION'},
    ]
    aeronaves = []
    for data in aeronaves_data:
        aeronave, created = Aeronave.objects.get_or_create(
            matricula=data['matricula'],
            defaults=data
        )
        aeronaves.append(aeronave)
        if created:
            print(f"  ✅ Aeronave {data['matricula']} creada")
        else:
            print(f"  ℹ️  Aeronave {data['matricula']} ya existe")
    print(f"✅ Total: {len(aeronaves)} aeronaves")
    
    # 3. Crear Conductores
    print("\n🚗 Creando conductores...")
    conductores_data = [
        {'nombre': 'Juan Pérez González', 'licencia': 'A2-12345678', 'vigente': True},
        {'nombre': 'María López Silva', 'licencia': 'A3-23456789', 'vigente': True},
        {'nombre': 'Carlos Rodríguez Muñoz', 'licencia': 'A2-34567890', 'vigente': True},
        {'nombre': 'Ana Martínez Rojas', 'licencia': 'A3-45678901', 'vigente': False},
    ]
    conductores = []
    for data in conductores_data:
        conductor, created = Conductor.objects.get_or_create(
            licencia=data['licencia'],
            defaults=data
        )
        conductores.append(conductor)
        if created:
            print(f"  ✅ Conductor {data['nombre']} creado")
        else:
            print(f"  ℹ️  Conductor {data['nombre']} ya existe")
    print(f"✅ Total: {len(conductores)} conductores")
    
    # 4. Crear Pilotos
    print("\n🛩️ Creando pilotos...")
    pilotos_data = [
        {'nombre': 'Roberto Sánchez Torres', 'certificacion': 'CPL-001234', 'horas_vuelo': 5000},
        {'nombre': 'Laura Fernández Castro', 'certificacion': 'ATPL-005678', 'horas_vuelo': 8500},
        {'nombre': 'Diego Ramírez Vargas', 'certificacion': 'CPL-009012', 'horas_vuelo': 3200},
    ]
    pilotos = []
    for data in pilotos_data:
        piloto, created = Piloto.objects.get_or_create(
            certificacion=data['certificacion'],
            defaults=data
        )
        pilotos.append(piloto)
        if created:
            print(f"  ✅ Piloto {data['nombre']} creado")
        else:
            print(f"  ℹ️  Piloto {data['nombre']} ya existe")
    print(f"✅ Total: {len(pilotos)} pilotos")
    
    # 5. Crear Rutas
    print("\n🗺️ Creando rutas...")
    rutas_data = [
        {'origen': 'Santiago', 'destino': 'Valparaíso', 'tipo_transporte': 'TERRESTRE'},
        {'origen': 'Santiago', 'destino': 'Concepción', 'tipo_transporte': 'TERRESTRE'},
        {'origen': 'Santiago', 'destino': 'Antofagasta', 'tipo_transporte': 'AEREO'},
        {'origen': 'Santiago', 'destino': 'Puerto Montt', 'tipo_transporte': 'AEREO'},
        {'origen': 'Valparaíso', 'destino': 'Viña del Mar', 'tipo_transporte': 'TERRESTRE'},
        {'origen': 'Santiago', 'destino': 'Punta Arenas', 'tipo_transporte': 'AEREO'},
    ]
    rutas = []
    for data in rutas_data:
        ruta, created = Ruta.objects.get_or_create(
            origen=data['origen'],
            destino=data['destino'],
            tipo_transporte=data['tipo_transporte'],
            defaults=data
        )
        rutas.append(ruta)
        if created:
            print(f"  ✅ Ruta {data['origen']} → {data['destino']} creada")
        else:
            print(f"  ℹ️  Ruta {data['origen']} → {data['destino']} ya existe")
    print(f"✅ Total: {len(rutas)} rutas")
    
    # 6. Crear Clientes
    print("\n👥 Creando clientes...")
    clientes_data = [
        {'nombre': 'Empresa Retail S.A.', 'rut': '76.123.456-7', 'direccion': 'Av. Libertador Bernardo O\'Higgins 1234, Santiago'},
        {'nombre': 'Distribuidora Nacional Ltda.', 'rut': '77.234.567-8', 'direccion': 'Calle Bandera 567, Santiago'},
        {'nombre': 'Comercial Import Export SpA', 'rut': '78.345.678-9', 'direccion': 'Av. Apoquindo 3456, Las Condes'},
        {'nombre': 'Grupo Empresarial del Sur', 'rut': '79.456.789-0', 'direccion': 'Calle Arturo Prat 890, Concepción'},
        {'nombre': 'Alimentos Procesados Chile', 'rut': '80.567.890-1', 'direccion': 'Camino a Melipilla Km 15, Santiago'},
    ]
    clientes = []
    for data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            rut=data['rut'],
            defaults=data
        )
        clientes.append(cliente)
        if created:
            print(f"  ✅ Cliente {data['nombre']} creado")
        else:
            print(f"  ℹ️  Cliente {data['nombre']} ya existe")
    print(f"✅ Total: {len(clientes)} clientes")
    
    # 7. Crear Cargas (solo si no existen)
    print("\n📦 Creando cargas...")
    if Carga.objects.count() == 0:
        cargas = [
            Carga.objects.create(
                tipo='Electrodomésticos',
                peso_kg=5000.00,
                valor=15000000.00,
                cliente=clientes[0]
            ),
            Carga.objects.create(
                tipo='Alimentos no perecibles',
                peso_kg=8000.00,
                valor=5000000.00,
                cliente=clientes[4]
            ),
            Carga.objects.create(
                tipo='Repuestos automotrices',
                peso_kg=2500.00,
                valor=8000000.00,
                cliente=clientes[1]
            ),
            Carga.objects.create(
                tipo='Productos electrónicos',
                peso_kg=1200.00,
                valor=25000000.00,
                cliente=clientes[2]
            ),
            Carga.objects.create(
                tipo='Material de construcción',
                peso_kg=12000.00,
                valor=6000000.00,
                cliente=clientes[3]
            ),
            Carga.objects.create(
                tipo='Textiles',
                peso_kg=3500.00,
                valor=4500000.00,
                cliente=clientes[0]
            ),
            Carga.objects.create(
                tipo='Equipamiento médico',
                peso_kg=800.00,
                valor=18000000.00,
                cliente=clientes[2]
            ),
        ]
        print(f"✅ {len(cargas)} cargas creadas")
    else:
        cargas = list(Carga.objects.all()[:7])
        print(f"ℹ️  Ya existen {Carga.objects.count()} cargas, usando existentes")
    
    # 8. Crear Despachos (solo si no existen)
    print("\n🚚 Creando despachos...")
    if Despacho.objects.count() == 0:
        despachos = [
            # Despacho terrestre 1
            Despacho.objects.create(
                ruta=rutas[0],  # Santiago - Valparaíso
                vehiculo=vehiculos[0],
                conductor=conductores[0],
                carga=cargas[0],
                estado='ENTREGADO'
            ),
            # Despacho terrestre 2
            Despacho.objects.create(
                ruta=rutas[1],  # Santiago - Concepción
                vehiculo=vehiculos[1],
                conductor=conductores[1],
                carga=cargas[4],
                estado='EN_RUTA'
            ),
            # Despacho terrestre 3
            Despacho.objects.create(
                ruta=rutas[4],  # Valparaíso - Viña del Mar
                vehiculo=vehiculos[2],
                conductor=conductores[2],
                carga=cargas[5],
                estado='PENDIENTE'
            ),
            # Despacho aéreo 1
            Despacho.objects.create(
                ruta=rutas[2],  # Santiago - Antofagasta
                aeronave=aeronaves[0],
                piloto=pilotos[0],
                carga=cargas[1],
                estado='ENTREGADO'
            ),
            # Despacho aéreo 2
            Despacho.objects.create(
                ruta=rutas[3],  # Santiago - Puerto Montt
                aeronave=aeronaves[1],
                piloto=pilotos[1],
                carga=cargas[2],
                estado='EN_RUTA'
            ),
            # Despacho aéreo 3
            Despacho.objects.create(
                ruta=rutas[5],  # Santiago - Punta Arenas
                aeronave=aeronaves[3],
                piloto=pilotos[2],
                carga=cargas[6],
                estado='PENDIENTE'
            ),
            # Despacho con helicóptero
            Despacho.objects.create(
                ruta=rutas[2],  # Santiago - Antofagasta
                aeronave=aeronaves[2],
                piloto=pilotos[0],
                carga=cargas[3],
                estado='EN_RUTA'
            ),
        ]
        print(f"✅ {len(despachos)} despachos creados")
    else:
        print(f"ℹ️  Ya existen {Despacho.objects.count()} despachos")
    
    print("\n" + "="*60)
    print("✅ CARGA DE DATOS COMPLETADA CON ÉXITO")
    print("="*60)
    print("\nResumen:")
    print(f"  - Vehículos: {Vehiculo.objects.count()}")
    print(f"  - Aeronaves: {Aeronave.objects.count()}")
    print(f"  - Conductores: {Conductor.objects.count()}")
    print(f"  - Pilotos: {Piloto.objects.count()}")
    print(f"  - Rutas: {Ruta.objects.count()}")
    print(f"  - Clientes: {Cliente.objects.count()}")
    print(f"  - Cargas: {Carga.objects.count()}")
    print(f"  - Despachos: {Despacho.objects.count()}")
    print(f"  - Usuarios: {User.objects.count()}")
    print("\n💡 Credenciales de acceso:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("\n🔗 Accede a:")
    print("   - Admin: http://localhost:8000/admin/")
    print("   - API: http://localhost:8000/api/")
    print("   - Swagger: http://localhost:8000/swagger/")
    print("   - Frontend: http://localhost:8000/")

if __name__ == '__main__':
    cargar_datos()
