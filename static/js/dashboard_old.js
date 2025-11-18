// Funcionalidad para el dashboard de monitoreo

// Datos simulados del sistema
let systemData = {
    waterLevel: 75,
    phLevel: 6.5,
    waterTemp: 22,
    nutrientLevel: 85,
    irrigationActive: true,
    lightActive: true
};

// Función para actualizar el nivel de agua
function updateWaterLevel() {
    const waterLevelElement = document.getElementById('waterLevel');
    const waterLevelBar = document.getElementById('waterLevelBar');

    waterLevelElement.textContent = systemData.waterLevel;
    waterLevelBar.style.width = systemData.waterLevel + '%';

    // Cambiar color según el nivel
    if (systemData.waterLevel < 30) {
        waterLevelBar.style.background = 'linear-gradient(90deg, #e74c3c 0%, #c0392b 100%)';
        addAlert('warning', 'Nivel de agua bajo. Se recomienda rellenar el tanque.', 'Ahora');
    } else if (systemData.waterLevel > 90) {
        waterLevelBar.style.background = 'linear-gradient(90deg, #f39c12 0%, #e67e22 100%)';
    } else {
        waterLevelBar.style.background = 'linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%)';
    }
}

// Función para actualizar el nivel de pH
function updatePHLevel() {
    const phLevelElement = document.getElementById('phLevel');
    const phIndicator = document.getElementById('phIndicator');

    phLevelElement.textContent = systemData.phLevel.toFixed(1);

    // Calcular posición del indicador (pH 5.5 a 8.5 = 0% a 100%)
    const minPH = 5.5;
    const maxPH = 8.5;
    const position = ((systemData.phLevel - minPH) / (maxPH - minPH)) * 100;
    phIndicator.style.left = Math.max(0, Math.min(100, position)) + '%';

    // Alertas de pH
    if (systemData.phLevel < 6.0 || systemData.phLevel > 7.5) {
        addAlert('warning', `Nivel de pH fuera del rango óptimo: ${systemData.phLevel.toFixed(1)}`, 'Ahora');
    }
}

// Función para actualizar la temperatura del agua
function updateWaterTemp() {
    const waterTempElement = document.getElementById('waterTemp');
    const tempBar = document.getElementById('tempBar');

    waterTempElement.textContent = systemData.waterTemp;

    // Calcular altura de la barra (18°C a 26°C = 0% a 100%)
    const minTemp = 18;
    const maxTemp = 26;
    const height = ((systemData.waterTemp - minTemp) / (maxTemp - minTemp)) * 100;
    tempBar.style.height = Math.max(0, Math.min(100, height)) + '%';

    // Alertas de temperatura
    if (systemData.waterTemp < 18 || systemData.waterTemp > 26) {
        addAlert('warning', `Temperatura del agua fuera del rango: ${systemData.waterTemp}°C`, 'Ahora');
    }
}

// Función para actualizar el nivel de nutrientes
function updateNutrientLevel() {
    const nutrientLevelElement = document.getElementById('nutrientLevel');
    const nutrientBar = document.getElementById('nutrientBar');

    nutrientLevelElement.textContent = systemData.nutrientLevel;
    nutrientBar.style.width = systemData.nutrientLevel + '%';

    // Alerta de nutrientes bajos
    if (systemData.nutrientLevel < 30) {
        nutrientBar.style.background = 'linear-gradient(90deg, #e74c3c 0%, #c0392b 100%)';
        addAlert('danger', 'Nivel de nutrientes crítico. Añadir nutrientes inmediatamente.', 'Ahora');
    } else if (systemData.nutrientLevel < 50) {
        nutrientBar.style.background = 'linear-gradient(90deg, #f39c12 0%, #e67e22 100%)';
    } else {
        nutrientBar.style.background = 'linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%)';
    }
}

// Función para actualizar el estado de irrigación
function updateIrrigationStatus() {
    const irrigationIcon = document.getElementById('irrigationIcon');
    const irrigationStatus = document.getElementById('irrigationStatus');
    const toggleBtn = document.getElementById('toggleIrrigation');

    if (systemData.irrigationActive) {
        irrigationIcon.textContent = '💧';
        irrigationStatus.textContent = 'Ciclo en progreso';
        toggleBtn.textContent = 'Detener Irrigación';
        toggleBtn.classList.remove('btn-primary');
        toggleBtn.classList.add('btn-secondary');
    } else {
        irrigationIcon.textContent = '⏸️';
        irrigationStatus.textContent = 'Sistema pausado';
        toggleBtn.textContent = 'Iniciar Irrigación';
        toggleBtn.classList.remove('btn-secondary');
        toggleBtn.classList.add('btn-primary');
    }
}

// Función para actualizar el estado de iluminación
function updateLightStatus() {
    const lightIcon = document.getElementById('lightIcon');
    const lightStatus = document.getElementById('lightStatus');
    const toggleBtn = document.getElementById('toggleLight');

    if (systemData.lightActive) {
        lightIcon.textContent = '💡';
        lightStatus.textContent = 'Ciclo diurno activo';
        toggleBtn.textContent = 'Apagar Luces';
        toggleBtn.classList.remove('btn-primary');
        toggleBtn.classList.add('btn-secondary');
    } else {
        lightIcon.textContent = '🌙';
        lightStatus.textContent = 'Ciclo nocturno activo';
        toggleBtn.textContent = 'Encender Luces';
        toggleBtn.classList.remove('btn-secondary');
        toggleBtn.classList.add('btn-primary');
    }
}

// Función para añadir alertas
function addAlert(type, message, time) {
    const alertsList = document.getElementById('alertsList');

    // Verificar si la alerta ya existe
    const existingAlerts = alertsList.querySelectorAll('.alert-message');
    for (let alert of existingAlerts) {
        if (alert.textContent === message) {
            return; // No agregar alerta duplicada
        }
    }

    const icons = {
        info: 'ℹ️',
        warning: '⚠️',
        danger: '🚨',
        success: '✅'
    };

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <span class="alert-icon">${icons[type]}</span>
        <span class="alert-message">${message}</span>
        <span class="alert-time">${time}</span>
    `;

    // Insertar al principio de la lista
    alertsList.insertBefore(alertDiv, alertsList.firstChild);

    // Limitar el número de alertas a 5
    while (alertsList.children.length > 5) {
        alertsList.removeChild(alertsList.lastChild);
    }
}

// Función para simular cambios en los datos
function simulateDataChanges() {
    // Nivel de agua disminuye gradualmente
    systemData.waterLevel -= Math.random() * 0.5;
    systemData.waterLevel = Math.max(0, systemData.waterLevel);

    // pH varía ligeramente
    systemData.phLevel += (Math.random() - 0.5) * 0.1;
    systemData.phLevel = Math.max(5.0, Math.min(8.5, systemData.phLevel));

    // Temperatura varía ligeramente
    systemData.waterTemp += (Math.random() - 0.5) * 0.3;
    systemData.waterTemp = Math.max(15, Math.min(30, systemData.waterTemp));

    // Nutrientes disminuyen gradualmente
    systemData.nutrientLevel -= Math.random() * 0.3;
    systemData.nutrientLevel = Math.max(0, systemData.nutrientLevel);

    // Actualizar todas las visualizaciones
    updateAllMetrics();
}

// Función para actualizar todas las métricas
function updateAllMetrics() {
    updateWaterLevel();
    updatePHLevel();
    updateWaterTemp();
    updateNutrientLevel();
    updateIrrigationStatus();
    updateLightStatus();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar valores
    updateAllMetrics();

    // Toggle de irrigación
    document.getElementById('toggleIrrigation').addEventListener('click', function() {
        systemData.irrigationActive = !systemData.irrigationActive;
        updateIrrigationStatus();

        if (systemData.irrigationActive) {
            addAlert('success', 'Sistema de irrigación iniciado', 'Ahora');
        } else {
            addAlert('info', 'Sistema de irrigación detenido', 'Ahora');
        }
    });

    // Toggle de iluminación
    document.getElementById('toggleLight').addEventListener('click', function() {
        systemData.lightActive = !systemData.lightActive;
        updateLightStatus();

        if (systemData.lightActive) {
            addAlert('success', 'Sistema de iluminación encendido', 'Ahora');
        } else {
            addAlert('info', 'Sistema de iluminación apagado', 'Ahora');
        }
    });

    // Botón de añadir nutrientes
    document.getElementById('addNutrients').addEventListener('click', function() {
        systemData.nutrientLevel = Math.min(100, systemData.nutrientLevel + 30);
        updateNutrientLevel();
        addAlert('success', 'Nutrientes añadidos al sistema', 'Ahora');
    });

    // Simular actualización de datos cada 5 segundos
    setInterval(simulateDataChanges, 5000);

    // Actualizar timestamps cada minuto
    setInterval(function() {
        const timeElements = document.querySelectorAll('.last-update span');
        timeElements.forEach(function(el, index) {
            const minutes = Math.floor(Math.random() * 5) + 1;
            el.textContent = `Hace ${minutes} min`;
        });
    }, 60000);
});

// Función para exportar datos (para futuro uso)
function exportData() {
    const dataToExport = {
        timestamp: new Date().toISOString(),
        ...systemData
    };
    console.log('Datos exportados:', dataToExport);
    return dataToExport;
}

// Función para recibir datos desde un servidor (para futuro uso)
function fetchDataFromServer() {
    // Aquí se implementaría la conexión con el backend
    console.log('Solicitando datos del servidor...');
}
