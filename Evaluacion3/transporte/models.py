from django.db import models


class Vehiculo(models.Model):
    """Modelo para vehículos terrestres"""
    
    TIPO_CHOICES = [
        ('CAMION', 'Camión'),
        ('FURGON', 'Furgón'),
        ('BUS', 'Bus'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    patente = models.CharField(max_length=10, unique=True)
    capacidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
    
    def __str__(self):
        return f"{self.tipo} - {self.patente} ({self.marca})"


class Aeronave(models.Model):
    """Modelo para aeronaves"""
    
    TIPO_CHOICES = [
        ('AVION', 'Avión'),
        ('HELICOPTERO', 'Helicóptero'),
    ]
    
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)
    capacidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    
    class Meta:
        verbose_name = 'Aeronave'
        verbose_name_plural = 'Aeronaves'
    
    def __str__(self):
        return f"{self.tipo} {self.modelo} - {self.matricula}"


class Conductor(models.Model):
    """Modelo para conductores de vehículos terrestres"""
    
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=20, unique=True)
    vigente = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
    
    def __str__(self):
        estado = "Vigente" if self.vigente else "No Vigente"
        return f"{self.nombre} - Lic: {self.licencia} ({estado})"


class Piloto(models.Model):
    """Modelo para pilotos de aeronaves"""
    
    nombre = models.CharField(max_length=100)
    certificacion = models.CharField(max_length=50, unique=True)
    horas_vuelo = models.IntegerField()
    
    class Meta:
        verbose_name = 'Piloto'
        verbose_name_plural = 'Pilotos'
    
    def __str__(self):
        return f"{self.nombre} - Cert: {self.certificacion} ({self.horas_vuelo}h)"


class Ruta(models.Model):
    """Modelo para rutas de transporte"""
    
    TIPO_TRANSPORTE_CHOICES = [
        ('TERRESTRE', 'Terrestre'),
        ('AEREO', 'Aéreo'),
    ]
    
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    tipo_transporte = models.CharField(max_length=15, choices=TIPO_TRANSPORTE_CHOICES)
    
    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
    
    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.tipo_transporte})"


class Cliente(models.Model):
    """Modelo para clientes"""
    
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f"{self.nombre} - RUT: {self.rut}"


class Carga(models.Model):
    """Modelo para cargas"""
    
    tipo = models.CharField(max_length=100)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cargas')
    
    class Meta:
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'
    
    def __str__(self):
        return f"{self.tipo} - {self.peso_kg}kg (Cliente: {self.cliente.nombre})"


class Despacho(models.Model):
    """Modelo para despachos"""
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_RUTA', 'En Ruta'),
        ('ENTREGADO', 'Entregado'),
    ]
    
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name='despachos')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    piloto = models.ForeignKey(Piloto, on_delete=models.SET_NULL, null=True, blank=True, related_name='despachos')
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE, related_name='despachos')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        transporte = self.vehiculo if self.vehiculo else self.aeronave
        personal = self.conductor if self.conductor else self.piloto
        return f"Despacho #{self.id} - {self.ruta} - {self.estado} ({transporte})"
