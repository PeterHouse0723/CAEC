// Funcionalidad para el nuevo dashboard CAEC

// Datos del sistema
let systemData = {
    water: { value: 75, unit: '%', label: 'Nivel Actual', target: 3000 },
    ph: { value: 6.5, unit: 'pH', label: 'Nivel Actual', min: 5.5, max: 8.5 },
    irrigation: {
        value: 'Activo',
        status: true,
        savingPower: 40,           // Potencia en modo ahorro (0-100%)
        savingDuration: 15,        // Duración del modo ahorro en minutos
        abundantDuration: 5        // Duración del modo abundante en minutos
    },
    temperature: { value: 22, unit: '°C', label: 'Temperatura Actual', min: 18, max: 26 },
    nutrient: { value: 85, unit: '%', label: 'Nivel Actual' },
    light: { value: 'Encendido', status: true, intensity: 80 }
};

// Configuración de sensores
const sensorConfig = {
    water: {
        title: 'Nivel de Agua',
        icon: '💧',
        color: '#667eea',
        details: [
            { label: 'Capacidad total', value: '3000 ml' },
            { label: 'Cantidad actual', value: '2250 ml' },
            { label: 'Objetivo diario', value: '3000 ml' }
        ]
    },
    ph: {
        title: 'Nivel pH',
        icon: '🧪',
        color: '#f5576c',
        details: [
            { label: 'Rango óptimo', value: '6.0 - 7.5' },
            { label: 'Estado', value: 'Normal' },
            { label: 'Última calibración', value: 'Hace 2 días' }
        ]
    },
    irrigation: {
        title: 'Sistema de Irrigación',
        icon: '🚿',
        color: '#00f2fe',
        details: [
            { label: 'Estado', value: 'Activo' },
            { label: 'Próximo ciclo', value: '15 min' },
            { label: 'Frecuencia', value: 'Cada 2 hrs' }
        ]
    },
    temperature: {
        title: 'Temperatura del Agua',
        icon: '🌡️',
        color: '#fee140',
        details: [
            { label: 'Rango óptimo', value: '20-24°C' },
            { label: 'Estado', value: 'Óptima' },
            { label: 'Tendencia', value: 'Estable' }
        ]
    },
    nutrient: {
        title: 'Nivel de Nutrientes',
        icon: '⚗️',
        color: '#30cfd0',
        details: [
            { label: 'Cantidad', value: '850 ml' },
            { label: 'Estado', value: 'Bueno' },
            { label: 'Reponer en', value: '5 días' }
        ]
    },
    light: {
        title: 'Sistema de Iluminación',
        icon: '💡',
        color: '#ffd89b',
        details: [
            { label: 'Estado', value: 'Encendido' },
            { label: 'Intensidad', value: '80%' },
            { label: 'Tiempo activo', value: '8 hrs' }
        ]
    }
};

// Función para abrir el modal
function openSensorModal(sensorType) {
    const modal = document.getElementById('sensorModal');
    const config = sensorConfig[sensorType];
    const data = systemData[sensorType];

    // Actualizar título
    document.getElementById('modalTitle').textContent = config.title;

    // Crear visualización según el tipo de sensor
    const visualizationContainer = document.getElementById('visualizationContainer');
    visualizationContainer.innerHTML = '';

    switch(sensorType) {
        case 'temperature':
            visualizationContainer.innerHTML = createThermometerVisualization(data.value);
            break;
        case 'water':
            visualizationContainer.innerHTML = createWaterTankVisualization(data.value);
            break;
        case 'ph':
            visualizationContainer.innerHTML = createPHScaleVisualization(data.value);
            break;
        case 'nutrient':
            visualizationContainer.innerHTML = createBeakerVisualization(data.value);
            break;
        default:
            visualizationContainer.innerHTML = createCircleVisualization(data.value, data.unit, config.icon, config.color, sensorType);
    }

    // Animar la visualización
    setTimeout(() => {
        animateVisualization(sensorType, data.value);
    }, 100);

    // Actualizar detalles
    const detailsContainer = document.getElementById('modalDetails');
    detailsContainer.innerHTML = '';

    config.details.forEach(detail => {
        const row = document.createElement('div');
        row.className = 'detail-row';
        row.innerHTML = `
            <span class="detail-label">${detail.label}:</span>
            <span class="detail-value">${detail.value}</span>
        `;
        detailsContainer.appendChild(row);
    });

    // Mostrar modal
    modal.style.display = 'block';

    // Prevenir scroll del body
    document.body.style.overflow = 'hidden';
}

// Función para cerrar el modal
function closeSensorModal() {
    const modal = document.getElementById('sensorModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// ===== FUNCIONES PARA CREAR VISUALIZACIONES PERSONALIZADAS =====

// Visualización de Termómetro para Temperatura
function createThermometerVisualization(temperature) {
    const tempValue = Math.round(temperature);
    const minTemp = 0;
    const maxTemp = 40;
    const percentage = ((temperature - minTemp) / (maxTemp - minTemp)) * 100;

    return `
        <div class="thermometer-container">
            <div class="thermometer">
                <svg viewBox="0 0 100 300" class="thermometer-svg">
                    <!-- Tubo del termómetro -->
                    <rect x="35" y="40" width="30" height="180" fill="#f0f0f0" stroke="#e65100" stroke-width="2" rx="15"/>

                    <!-- Bulbo del termómetro -->
                    <circle cx="50" cy="240" r="25" fill="#f0f0f0" stroke="#e65100" stroke-width="2"/>

                    <!-- Mercurio (nivel que sube) -->
                    <rect x="40" y="210" width="20" height="0" fill="#e65100" id="mercuryLevel" rx="10"/>
                    <circle cx="50" cy="240" r="20" fill="#e65100"/>

                    <!-- Marcas de temperatura -->
                    <text x="15" y="60" font-size="10" fill="#666">40°</text>
                    <line x1="30" y1="55" x2="35" y2="55" stroke="#666" stroke-width="1"/>

                    <text x="15" y="110" font-size="10" fill="#666">30°</text>
                    <line x1="30" y1="105" x2="35" y2="105" stroke="#666" stroke-width="1"/>

                    <text x="15" y="160" font-size="10" fill="#666">20°</text>
                    <line x1="30" y1="155" x2="35" y2="155" stroke="#666" stroke-width="1"/>

                    <text x="15" y="210" font-size="10" fill="#666">10°</text>
                    <line x1="30" y1="205" x2="35" y2="205" stroke="#666" stroke-width="1"/>
                </svg>
            </div>
            <div class="temperature-display">
                <span class="temp-value">${tempValue}</span>
                <span class="temp-unit">°C</span>
            </div>
        </div>
    `;
}

// Visualización de Tanque de Agua
function createWaterTankVisualization(waterLevel) {
    const levelValue = Math.round(waterLevel);

    return `
        <div class="water-tank-container">
            <svg viewBox="0 0 200 300" class="water-tank-svg">
                <!-- Contenedor del tanque -->
                <rect x="50" y="50" width="100" height="200" fill="none" stroke="#1976d2" stroke-width="3" rx="5"/>

                <!-- Agua dentro del tanque -->
                <rect x="52" y="250" width="96" height="0" fill="#90caf9" id="waterFillLevel" opacity="0.7"/>

                <!-- Ondas en el agua -->
                <path d="" fill="#bbdefb" opacity="0.5" id="waterWave"/>

                <!-- Indicador de porcentaje -->
                <text x="100" y="30" text-anchor="middle" font-size="14" fill="#666">Capacidad</text>
            </svg>
            <div class="water-level-display">
                <span class="level-value">${levelValue}</span>
                <span class="level-unit">%</span>
            </div>
        </div>
    `;
}

// Visualización de Escala pH
function createPHScaleVisualization(phValue) {
    const phRounded = Math.round(phValue);
    const minPH = 0;
    const maxPH = 14;
    const position = ((phValue - minPH) / (maxPH - minPH)) * 100;

    return `
        <div class="ph-scale-container">
            <div class="ph-gradient-bar">
                <div class="ph-colors"></div>
                <div class="ph-marker" id="phMarker" style="left: ${position}%">
                    <div class="marker-arrow"></div>
                    <div class="marker-value">${phRounded}</div>
                </div>
            </div>
            <div class="ph-labels">
                <span>Ácido (0)</span>
                <span>Neutro (7)</span>
                <span>Alcalino (14)</span>
            </div>
            <div class="ph-display">
                <span class="ph-icon">🧪</span>
                <span class="ph-value">${phRounded}</span>
                <span class="ph-text">pH</span>
            </div>
        </div>
    `;
}

// Visualización de Vaso de Laboratorio para Nutrientes
function createBeakerVisualization(nutrientLevel) {
    const levelValue = Math.round(nutrientLevel);

    return `
        <div class="beaker-container">
            <svg viewBox="0 0 200 300" class="beaker-svg">
                <!-- Vaso de laboratorio -->
                <path d="M 70 50 L 70 200 Q 70 250 100 250 Q 130 250 130 200 L 130 50 Z"
                      fill="none" stroke="#6a1b9a" stroke-width="3"/>

                <!-- Líquido dentro del vaso -->
                <path d="M 72 200 Q 72 248 100 248 Q 128 248 128 200 L 128 250 L 72 250 Z"
                      fill="#ce93d8" opacity="0.6" id="nutrientFillLevel"/>

                <!-- Marcas de medición -->
                <line x1="65" y1="100" x2="75" y2="100" stroke="#6a1b9a" stroke-width="1"/>
                <text x="55" y="105" font-size="10" fill="#666">100%</text>

                <line x1="65" y1="150" x2="75" y2="150" stroke="#6a1b9a" stroke-width="1"/>
                <text x="60" y="155" font-size="10" fill="#666">50%</text>

                <line x1="65" y1="200" x2="75" y2="200" stroke="#6a1b9a" stroke-width="1"/>
                <text x="60" y="205" font-size="10" fill="#666">0%</text>
            </svg>
            <div class="nutrient-display">
                <span class="nutrient-value">${levelValue}</span>
                <span class="nutrient-unit">%</span>
            </div>
        </div>
    `;
}

// Visualización de Círculo (para irrigación y luz)
function createCircleVisualization(value, unit, icon, color, sensorType) {
    const displayValue = typeof value === 'number' ? Math.round(value) : value;

    // Si es irrigación, agregar controles especiales
    if (sensorType === 'irrigation') {
        const isActive = systemData.irrigation.status;
        const savingPower = systemData.irrigation.savingPower || 40;
        const abundantDuration = systemData.irrigation.abundantDuration || 5;
        const savingDuration = systemData.irrigation.savingDuration || 15;

        return `
            <div class="circle-progress-container">
                <div class="circle-icon-large">${icon}</div>
                <div class="circle-value-large">
                    <span class="value-main">${displayValue}</span>
                </div>
            </div>
            <div class="irrigation-controls">
                <h3 style="margin: 20px 0 15px 0; color: #333; font-size: 1.2rem;">Control de Irrigación</h3>
                <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 25px;">
                    <button onclick="toggleIrrigation(true)" class="btn ${isActive ? 'btn-active' : ''}"
                            style="padding: 12px 24px; border-radius: 8px; border: 2px solid #424242;
                                   background: ${isActive ? '#424242' : 'white'};
                                   color: ${isActive ? 'white' : '#424242'};
                                   font-weight: 600; cursor: pointer; transition: all 0.3s;">
                        Activar
                    </button>
                    <button onclick="toggleIrrigation(false)" class="btn ${!isActive ? 'btn-active' : ''}"
                            style="padding: 12px 24px; border-radius: 8px; border: 2px solid #757575;
                                   background: ${!isActive ? '#757575' : 'white'};
                                   color: ${!isActive ? 'white' : '#757575'};
                                   font-weight: 600; cursor: pointer; transition: all 0.3s;">
                        Desactivar
                    </button>
                </div>

                <!-- Modo de Ahorro de Energía -->
                <div style="margin-top: 20px; padding: 20px; background: #fafafa; border-radius: 12px; border: 1px solid #e0e0e0;">
                    <h4 style="margin: 0 0 15px 0; color: #424242; font-size: 1rem; font-weight: 600;">⚡ Modo de Ahorro de Energía</h4>

                    <!-- Barra deslizante de potencia -->
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <label style="font-size: 0.9rem; color: #666; font-weight: 500;">Potencia de la bomba:</label>
                            <span id="powerValue" style="font-size: 1.2rem; font-weight: 700; color: #424242;">${savingPower}%</span>
                        </div>
                        <div style="position: relative; height: 40px; background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%); border-radius: 20px; overflow: hidden; border: 2px solid #bdbdbd;">
                            <div id="powerFill" style="position: absolute; left: 0; top: 0; height: 100%; width: ${savingPower}%; background: linear-gradient(90deg, #616161 0%, #424242 100%); transition: width 0.3s ease; border-radius: 18px;"></div>
                            <input type="range" id="powerSlider" min="0" max="100" value="${savingPower}"
                                   oninput="updatePowerSlider(this.value)"
                                   style="position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 10;">
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.75rem; color: #999;">
                            <span>0%</span>
                            <span>50%</span>
                            <span>100%</span>
                        </div>
                    </div>

                    <!-- Duración del modo ahorro -->
                    <div style="margin-top: 15px;">
                        <label style="font-size: 0.9rem; color: #666; font-weight: 500; display: block; margin-bottom: 8px;">Duración del modo ahorro:</label>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <input type="number" id="savingDuration" value="${savingDuration}" min="1" max="120"
                                   style="flex: 1; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 0.95rem;">
                            <span style="color: #666; font-size: 0.9rem; white-space: nowrap;">minutos</span>
                        </div>
                    </div>
                </div>

                <!-- Periodo de Irrigación Abundante -->
                <div style="margin-top: 20px; padding: 20px; background: #fafafa; border-radius: 12px; border: 1px solid #e0e0e0;">
                    <h4 style="margin: 0 0 15px 0; color: #424242; font-size: 1rem; font-weight: 600;">💧 Irrigación Abundante (100%)</h4>
                    <div>
                        <label style="font-size: 0.9rem; color: #666; font-weight: 500; display: block; margin-bottom: 8px;">Duración del periodo abundante:</label>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <input type="number" id="abundantDuration" value="${abundantDuration}" min="1" max="60"
                                   style="flex: 1; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 0.95rem;">
                            <span style="color: #666; font-size: 0.9rem; white-space: nowrap;">minutos</span>
                        </div>
                    </div>
                    <p style="margin: 12px 0 0 0; font-size: 0.8rem; color: #999; line-height: 1.4;">
                        La bomba funcionará al 100% durante este tiempo, luego cambiará automáticamente al modo de ahorro.
                    </p>
                </div>

                <!-- Botón de guardar configuración -->
                <button onclick="saveIrrigationConfig()"
                        style="width: 100%; margin-top: 20px; padding: 14px; background: #424242; color: white; border: none;
                               border-radius: 10px; cursor: pointer; font-weight: 600; font-size: 1rem; transition: all 0.3s;">
                    Guardar Configuración
                </button>
            </div>
        `;
    }

    return `
        <div class="circle-progress-container">
            <div class="circle-icon-large">${icon}</div>
            <div class="circle-value-large">
                <span class="value-main">${displayValue}</span>
                ${unit ? `<span class="value-unit-main">${unit}</span>` : ''}
            </div>
        </div>
    `;
}

// Función para animar las visualizaciones
function animateVisualization(sensorType, value) {
    switch(sensorType) {
        case 'temperature':
            animateThermometer(value);
            break;
        case 'water':
            animateWaterTank(value);
            break;
        case 'nutrient':
            animateBeaker(value);
            break;
    }
}

// Animar termómetro
function animateThermometer(temperature) {
    const mercuryLevel = document.getElementById('mercuryLevel');
    if (!mercuryLevel) return;

    const minTemp = 0;
    const maxTemp = 40;
    const maxHeight = 180;
    const height = ((temperature - minTemp) / (maxTemp - minTemp)) * maxHeight;
    const yPosition = 210 - height;

    setTimeout(() => {
        mercuryLevel.setAttribute('y', yPosition);
        mercuryLevel.setAttribute('height', height);
    }, 50);
}

// Animar tanque de agua
function animateWaterTank(waterLevel) {
    const waterFill = document.getElementById('waterFillLevel');
    if (!waterFill) return;

    const maxHeight = 196;
    const height = (waterLevel / 100) * maxHeight;
    const yPosition = 250 - height;

    setTimeout(() => {
        waterFill.setAttribute('y', yPosition);
        waterFill.setAttribute('height', height);
    }, 50);
}

// Animar vaso de nutrientes
function animateBeaker(nutrientLevel) {
    const nutrientFill = document.getElementById('nutrientFillLevel');
    if (!nutrientFill) return;

    // Aquí puedes agregar lógica para animar el nivel de nutrientes
    // Similar al tanque de agua
}

// Función para actualizar el círculo de progreso
function updateCircleProgress(value, sensorType) {
    const circle = document.getElementById('circleProgress');
    const circumference = 2 * Math.PI * 90; // radio = 90

    let percentage;

    // Calcular porcentaje según el tipo de sensor
    if (sensorType === 'ph') {
        // Para pH, mapear 5.5-8.5 a 0-100%
        percentage = ((value - 5.5) / (8.5 - 5.5)) * 100;
    } else if (sensorType === 'temperature') {
        // Para temperatura, mapear 18-26°C a 0-100%
        percentage = ((value - 18) / (26 - 18)) * 100;
    } else if (sensorType === 'irrigation' || sensorType === 'light') {
        // Para estados binarios
        percentage = systemData[sensorType].status ? 100 : 0;
    } else {
        // Para porcentajes directos
        percentage = parseFloat(value);
    }

    percentage = Math.max(0, Math.min(100, percentage));

    const offset = circumference - (percentage / 100) * circumference;
    circle.style.strokeDashoffset = offset;
}

// Función para agregar gradiente al SVG
function addGradientToSVG(color) {
    const svg = document.querySelector('.circle-progress');

    // Eliminar gradiente previo si existe
    const existingDef = svg.querySelector('defs');
    if (existingDef) {
        existingDef.remove();
    }

    // Crear nuevo gradiente
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
    gradient.setAttribute('id', 'gradient');
    gradient.setAttribute('x1', '0%');
    gradient.setAttribute('y1', '0%');
    gradient.setAttribute('x2', '100%');
    gradient.setAttribute('y2', '100%');

    const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop1.setAttribute('offset', '0%');
    stop1.setAttribute('style', `stop-color:${color};stop-opacity:1`);

    const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop2.setAttribute('offset', '100%');
    stop2.setAttribute('style', `stop-color:${color};stop-opacity:0.6`);

    gradient.appendChild(stop1);
    gradient.appendChild(stop2);
    defs.appendChild(gradient);
    svg.insertBefore(defs, svg.firstChild);
}

// Función para actualizar los valores de las tarjetas
function updateCardValues() {
    // Actualizar valor del agua (entero)
    const waterValue = Math.round(systemData.water.value);
    document.getElementById('waterValue').textContent = waterValue;

    // Actualizar posición de las olas según el nivel
    updateWavePosition(waterValue);

    // Actualizar pH (entero)
    document.getElementById('phValue').textContent = Math.round(systemData.ph.value);

    // Actualizar irrigación
    document.getElementById('irrigationValue').textContent = systemData.irrigation.value;

    // Actualizar temperatura (entero)
    document.getElementById('tempValue').textContent = Math.round(systemData.temperature.value);

    // Actualizar nutrientes (entero)
    document.getElementById('nutrientValue').textContent = Math.round(systemData.nutrient.value);

    // Actualizar luz
    document.getElementById('lightValue').textContent = systemData.light.value;

    // Actualizar visualización del sistema resumen
    updateSystemOverview();
}

// Función para actualizar la visualización del sistema resumen
function updateSystemOverview() {
    // Actualizar nivel de agua (siempre entero)
    const waterValue = Math.round(systemData.water.value);
    const waterLevelText = document.getElementById('waterLevelText');

    if (waterLevelText) {
        waterLevelText.textContent = waterValue + '%';
    }

    // Actualizar nivel de pH (siempre entero)
    const phValueText = document.getElementById('phValueText');
    if (phValueText) {
        phValueText.textContent = Math.round(systemData.ph.value);
    }

    // Actualizar nivel de nutrientes (siempre entero)
    const nutrientValueText = document.getElementById('nutrientValueText');
    if (nutrientValueText) {
        nutrientValueText.textContent = Math.round(systemData.nutrient.value) + '%';
    }

    // Actualizar posición de las olas en el tanque del sistema
    updateTankVisuals(waterValue);
}

// Función para actualizar la visualización del tanque (nivel de agua y olas)
function updateTankVisuals(percentage) {
    // --- 1. Actualizar el nivel del rectángulo de agua ---
    const waterRect = document.getElementById('tankWaterLevel');
    if (waterRect) {
        const tankTopY = 795;    // y inicial del contenedor del tanque + stroke
        const tankBottomY = 1125; // y + altura - stroke
        const tankHeight = tankBottomY - tankTopY; // Altura total disponible para el agua

        const waterHeight = tankHeight * (percentage / 100);
        const waterY = tankBottomY - waterHeight;

        waterRect.setAttribute('y', waterY);
        waterRect.setAttribute('height', waterHeight);
    }

    // --- 2. Actualizar la posición de las olas ---
    const waterSurfaceY = 1125 - (330 * percentage / 100);
    const wave1 = document.querySelector('.system-wave1');
    const wave2 = document.querySelector('.system-wave2');
    const wave3 = document.querySelector('.system-wave3');

    if (wave1) wave1.setAttribute('cy', waterSurfaceY - 5);
    if (wave2) wave2.setAttribute('cy', waterSurfaceY);
    if (wave3) wave3.setAttribute('cy', waterSurfaceY + 5);
}

// Función para actualizar la posición de las olas según el nivel de agua
function updateWavePosition(percentage) {
    const waveContainer = document.querySelector('.wave-container');
    if (waveContainer) {
        // Invertir el porcentaje porque las olas suben desde abajo
        const bottomPosition = percentage;
        waveContainer.style.height = bottomPosition + '%';
    }
}

// Función para simular cambios en los datos
function simulateDataChanges() {
    // Nivel de agua disminuye gradualmente
    systemData.water.value -= Math.random() * 0.5;
    systemData.water.value = Math.max(0, Math.min(100, systemData.water.value));

    // pH varía ligeramente
    systemData.ph.value += (Math.random() - 0.5) * 0.1;
    systemData.ph.value = Math.max(5.0, Math.min(8.5, systemData.ph.value));

    // Temperatura varía ligeramente
    systemData.temperature.value += (Math.random() - 0.5) * 0.3;
    systemData.temperature.value = Math.max(15, Math.min(30, systemData.temperature.value));

    // Nutrientes disminuyen gradualmente
    systemData.nutrient.value -= Math.random() * 0.3;
    systemData.nutrient.value = Math.max(0, Math.min(100, systemData.nutrient.value));

    // Actualizar valores en las tarjetas
    updateCardValues();
}

// Función para cerrar modal al hacer clic fuera de él
function closeModalOnOutsideClick(event) {
    if (event.target.id === 'sensorModal') {
        closeSensorModal();
    }
}

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Actualizar valores iniciales
    updateCardValues();

    // Simular actualización de datos cada 5 segundos
    setInterval(simulateDataChanges, 5000);

    // Cerrar modal con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSensorModal();
        }
    });
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

// Función para obtener datos del servidor (para futuro uso con API)
async function fetchDataFromServer() {
    try {
        const response = await fetch('/api/system-data');
        const data = await response.json();
        // Actualizar systemData con los datos del servidor
        console.log('Datos del servidor:', data);
    } catch (error) {
        console.error('Error al obtener datos:', error);
    }
}

// ===== FUNCIONES DE CONTROL DE IRRIGACIÓN =====

// Nueva función para el interruptor rápido
function toggleIrrigationState(event) {
    // 1. Detener la propagación para no abrir el modal
    event.stopPropagation();

    // 2. Invertir el estado actual
    const newStatus = !systemData.irrigation.status;

    // 3. Llamar a la función principal que actualiza todo
    toggleIrrigation(newStatus);
}

// Función para activar/desactivar irrigación
function toggleIrrigation(activate) {
    systemData.irrigation.status = activate;
    systemData.irrigation.value = activate ? 'Activo' : 'Inactivo';

    // Actualizar tarjeta de irrigación
    document.getElementById('irrigationValue').textContent = systemData.irrigation.value;

    // Actualizar visualización en el resumen
    updateIrrigationVisualization(activate);

    // Enviar actualización al servidor
    updateServerIrrigation(activate);
}

// Función para actualizar la visualización de irrigación en el resumen
function updateIrrigationVisualization(isActive) {
    const irrigationColumn = document.getElementById('irrigationColumn');
    const centralPipe = document.getElementById('centralPipe');
    const pump = document.getElementById('pump');

    // Obtener todas las gotas de agua de todos los niveles
    const allDrops = document.querySelectorAll('.water-drops');

    if (isActive) {
        // Mostrar tubería de fondo, bomba y columna de agua animada
        if(centralPipe) centralPipe.style.display = 'block';
        if(pump) pump.style.display = 'block';
        if(irrigationColumn) irrigationColumn.style.display = 'block';

        // Mostrar gotas cayendo en todos los niveles
        allDrops.forEach(drops => {
            if (drops) drops.style.display = 'block';
        });

    } else {
        // Ocultar todo lo relacionado con la irrigación
        if(centralPipe) centralPipe.style.display = 'none';
        if(pump) pump.style.display = 'none';
        if(irrigationColumn) irrigationColumn.style.display = 'none';

        // Ocultar gotas cayendo en todos los niveles
        allDrops.forEach(drops => {
            if (drops) drops.style.display = 'none';
        });
    }
}

// Función para enviar actualización al servidor
async function updateServerIrrigation(status) {
    try {
        const response = await fetch('/api/update-system', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                irrigation: {
                    status: status,
                    timestamp: new Date().toISOString()
                }
            })
        });
        const data = await response.json();
        console.log('Respuesta del servidor:', data);
    } catch (error) {
        console.error('Error al actualizar irrigación:', error);
    }
}

// Función para programar irrigación
function scheduleIrrigation(schedule) {
    console.log('Programación de irrigación:', schedule);
    // Aquí se implementaría la lógica de programación
    // Por ahora solo lo registramos
}

// Función para actualizar la barra deslizante de potencia
function updatePowerSlider(value) {
    const powerValue = document.getElementById('powerValue');
    const powerFill = document.getElementById('powerFill');

    if (powerValue) {
        powerValue.textContent = Math.round(value) + '%';
    }

    if (powerFill) {
        powerFill.style.width = value + '%';
    }
}

// Función para guardar la configuración de irrigación
function saveIrrigationConfig() {
    const powerSlider = document.getElementById('powerSlider');
    const savingDuration = document.getElementById('savingDuration');
    const abundantDuration = document.getElementById('abundantDuration');

    const config = {
        savingPower: powerSlider ? Math.round(powerSlider.value) : 40,
        savingDuration: savingDuration ? parseInt(savingDuration.value) : 15,
        abundantDuration: abundantDuration ? parseInt(abundantDuration.value) : 5
    };

    // Actualizar systemData
    systemData.irrigation.savingPower = config.savingPower;
    systemData.irrigation.savingDuration = config.savingDuration;
    systemData.irrigation.abundantDuration = config.abundantDuration;

    // Enviar al servidor
    updateServerIrrigationConfig(config);

    // Mostrar mensaje de confirmación
    alert(`Configuración guardada:\n\n⚡ Potencia en modo ahorro: ${config.savingPower}%\n⏱️ Duración modo ahorro: ${config.savingDuration} min\n💧 Duración irrigación abundante: ${config.abundantDuration} min`);
}

// Función para enviar configuración al servidor
async function updateServerIrrigationConfig(config) {
    try {
        const response = await fetch('/api/update-irrigation-config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                config: config,
                timestamp: new Date().toISOString()
            })
        });
        const data = await response.json();
        console.log('Configuración guardada en servidor:', data);
    } catch (error) {
        console.error('Error al guardar configuración:', error);
    }
}

// Inicializar visualización de irrigación según estado inicial
document.addEventListener('DOMContentLoaded', () => {
    updateIrrigationVisualization(systemData.irrigation.status);
    updateCardValues();
});


// ===== NUEVA FUNCIONALIDAD: MENÚ DE PERFIL Y CONTADOR DE COSECHA =====

/**
 * Muestra u oculta el menú desplegable del perfil.
 */
function toggleProfileMenu() {
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

/**
 * Inicia el contador regresivo para la cosecha.
 */
function startHarvestCountdown() {
    // Fecha estimada de cosecha (puedes cambiarla o hacerla dinámica)
    const harvestDate = new Date('2025-12-20T18:00:00');
    
    const harvestDateElement = document.getElementById('harvestDate');
    if(harvestDateElement) {
        const formattedDate = harvestDate.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
        harvestDateElement.textContent = `Fecha: ${formattedDate}`;
    }

    const daysEl = document.getElementById('days');
    const hoursEl = document.getElementById('hours');
    const minutesEl = document.getElementById('minutes');
    const secondsEl = document.getElementById('seconds');

    if (!daysEl || !hoursEl || !minutesEl || !secondsEl) return;

    const interval = setInterval(() => {
        const now = new Date();
        const distance = harvestDate.getTime() - now.getTime();

        if (distance < 0) {
            clearInterval(interval);
            document.getElementById('harvestCountdown').innerHTML = "<div style='font-size: 1.2rem; font-weight: bold; color: #388e3c;'>¡Cosecha Lista!</div>";
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        daysEl.textContent = String(days).padStart(2, '0');
        hoursEl.textContent = String(hours).padStart(2, '0');
        minutesEl.textContent = String(minutes).padStart(2, '0');
        secondsEl.textContent = String(seconds).padStart(2, '0');
    }, 1000);
}

// Event Listeners adicionales
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar contador de cosecha
    startHarvestCountdown();

    // Cerrar el menú de perfil si se hace clic fuera de él
    window.onclick = function(event) {
        if (!event.target.matches('.profile-circle')) {
            const dropdowns = document.getElementsByClassName('dropdown-menu');
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
});

