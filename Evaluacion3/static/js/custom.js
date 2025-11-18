// JavaScript personalizado para Logística Global Ltda.

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚛 Sistema de Logística Global Ltda. cargado');
    
    // Agregar animaciones a las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // Confirmación antes de eliminar
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });
    
    // Tooltip de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Highlight de navbar activo
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Mensaje de bienvenida en consola
    console.log('%c¡Bienvenido a Logística Global Ltda.!', 'color: #3b82f6; font-size: 20px; font-weight: bold;');
    console.log('%cAPI REST disponible en /api/', 'color: #10b981; font-size: 14px;');
    console.log('%cDocumentación Swagger en /swagger/', 'color: #f59e0b; font-size: 14px;');
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Función para formatear números
function formatNumber(number) {
    return new Intl.NumberFormat('es-CL').format(number);
}

// Función para formatear moneda chilena
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(amount);
}

// Exportar funciones globalmente
window.logistica = {
    showNotification,
    formatNumber,
    formatCurrency
};
