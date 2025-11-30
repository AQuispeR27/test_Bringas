# 🔫 Sistema de Detección de Armas con YOLOv11

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/Flutter-3.0+-02569B.svg)](https://flutter.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-yellow.svg)](https://docs.ultralytics.com/)

Sistema completo de detección de armas en tiempo real usando **YOLOv11** con aplicación móvil (Flutter) y backend (FastAPI) con sistema de alertas automáticas (Push Notifications + SMS).

---

## 🎯 Características

### ✨ Funcionalidades Principales

- 🎥 **Detección en Tiempo Real**: Procesamiento de video en vivo desde cámara móvil
- 📱 **Aplicación Móvil**: App nativa para Android/iOS con Flutter
- ⚡ **Backend Potente**: FastAPI + YOLOv11 con soporte GPU
- 🚨 **Alertas Automáticas**:
  - Notificaciones Push (Firebase Cloud Messaging)
  - SMS (Twilio)
  - Email (opcional)
- 🌐 **WebSocket Streaming**: Comunicación en tiempo real optimizada
- 📊 **Estadísticas**: Panel de métricas y detecciones históricas
- 🎨 **Interfaz Intuitiva**: UI moderna con Material Design

### 🔧 Tecnologías Utilizadas

**Backend:**
- Python 3.8+
- FastAPI
- YOLOv11 (Ultralytics)
- PyTorch + CUDA
- WebSockets
- Twilio (SMS)
- Firebase Admin SDK

**Mobile:**
- Flutter 3.0+
- Dart
- Camera Plugin
- Firebase Messaging
- Provider (State Management)

**Infraestructura:**
- WebSocket para streaming
- REST API
- Firebase Cloud Messaging
- CUDA para aceleración GPU

---

## 📂 Estructura del Proyecto

```
YOLO_Seguridad/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── main.py            # API principal
│   │   ├── utils/
│   │   │   ├── alert_manager.py      # Gestor de alertas
│   │   │   └── detection_logger.py   # Logger de detecciones
│   ├── requirements.txt       # Dependencias Python
│   ├── .env.example          # Variables de entorno
│   └── run_server.sh         # Script de inicio
│
├── mobile_app/                # Aplicación Flutter
│   ├── lib/
│   │   ├── main.dart         # Entry point
│   │   ├── screens/          # Pantallas
│   │   │   ├── home_screen.dart
│   │   │   └── settings_screen.dart
│   │   ├── services/         # Servicios
│   │   │   ├── detection_service.dart
│   │   │   └── notification_service.dart
│   │   ├── models/           # Modelos de datos
│   │   ├── widgets/          # Widgets reutilizables
│   │   └── utils/            # Utilidades
│   └── pubspec.yaml          # Dependencias Flutter
│
├── runs/                      # Resultados del entrenamiento YOLO
│   └── detect/train/weights/
│       └── best.pt           # Modelo entrenado
│
├── Prueba2.ipynb             # Notebook de entrenamiento
├── MOBILE_APP_GUIDE.md       # Guía completa de instalación
└── README.md                 # Este archivo
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Para Backend:**
  - Python 3.8+
  - GPU NVIDIA con CUDA (recomendado)
  - 8GB RAM mínimo

- **Para Mobile:**
  - Flutter SDK 3.0+
  - Android Studio / Xcode
  - Dispositivo físico o emulador

### Instalación Backend

```bash
# 1. Clonar repositorio
git clone https://github.com/AQuispeR27/test_Bringas.git
cd test_Bringas/backend

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus credenciales

# 5. Iniciar servidor
./run_server.sh
```

### Instalación Mobile

```bash
# 1. Navegar a carpeta móvil
cd mobile_app

# 2. Instalar dependencias
flutter pub get

# 3. Configurar Firebase
flutterfire configure

# 4. Editar URL del servidor en lib/utils/app_config.dart
# Cambiar IP a la de tu servidor

# 5. Ejecutar app
flutter run
```

**📖 Para guía completa y detallada, ver: [MOBILE_APP_GUIDE.md](MOBILE_APP_GUIDE.md)**

---

## 📊 Uso

### 1. Entrenar el Modelo (si no tienes best.pt)

```bash
# Abrir Jupyter Notebook
jupyter notebook Prueba2.ipynb

# Ejecutar todas las celdas
# El modelo entrenado se guardará en runs/detect/train/weights/best.pt
```

### 2. Iniciar Backend

```bash
cd backend
./run_server.sh
```

El servidor estará disponible en:
- API: `http://TU_IP:8000`
- Documentación interactiva: `http://TU_IP:8000/docs`
- WebSocket: `ws://TU_IP:8000/ws/stream`

### 3. Usar Aplicación Móvil

1. Abrir app en tu dispositivo
2. Ir a **Configuración**
3. Configurar URL del backend (`http://TU_IP:8000`)
4. Configurar alertas (Push/SMS)
5. Guardar y volver a pantalla principal
6. Click en **INICIAR** para comenzar detección

---

## 🔔 Configuración de Alertas

### SMS (Twilio)

1. Crear cuenta en [Twilio](https://www.twilio.com/)
2. Obtener credenciales:
   - Account SID
   - Auth Token
   - Número de teléfono Twilio
3. Agregar a `backend/.env`:
```bash
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Push Notifications (Firebase)

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Agregar apps Android/iOS
3. Descargar `google-services.json` (Android) y `GoogleService-Info.plist` (iOS)
4. Descargar Service Account Key desde Firebase Settings
5. Guardar como `backend/firebase-credentials.json`
6. Configurar en `backend/.env`:
```bash
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

---

## 📡 API Endpoints

### REST API

```bash
# Health Check
GET /

# Detectar armas en imagen
POST /detect/image
Body: FormData { file: imagen.jpg }

# Detectar en frame de video
POST /detect/frame
Body: { "frame": "base64_image", "alert_config": {...} }

# Obtener estadísticas
GET /stats/detections
```

### WebSocket

```javascript
// Conectar
const ws = new WebSocket('ws://TU_IP:8000/ws/stream');

// Enviar frame
ws.send(JSON.stringify({
  frame: "base64_encoded_image",
  alert_config: { ... }
}));

// Recibir detección
ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  // result.detected, result.detections, ...
};
```

---

## 📈 Rendimiento

### Velocidades Típicas

- **GPU (RTX 4070)**: ~60 FPS
- **CPU (i7)**: ~10-15 FPS
- **Móvil (procesando 1/3 frames)**: ~10 FPS efectivos

### Optimizaciones

**Para más velocidad:**
- Reducir resolución de entrada
- Usar modelo nano (`yolo11n.pt`)
- Aumentar `frameSkip` en app móvil

**Para más precisión:**
- Usar modelo large (`yolo11l.pt`)
- Aumentar resolución a 1280
- Entrenar con más epochs

---

## 🎯 Casos de Uso

- 🏫 **Seguridad Escolar**: Detección temprana de amenazas
- 🏢 **Edificios Corporativos**: Monitoreo de accesos
- 🏦 **Bancos**: Prevención de robos
- 🛂 **Aeropuertos**: Control de seguridad
- 🏘️ **Residencial**: Vigilancia inteligente

---

## 🔒 Consideraciones de Seguridad

⚠️ **Importante:**
- Este sistema es una **herramienta de asistencia**, no un reemplazo de seguridad profesional
- Puede tener falsos positivos/negativos
- Usar en conjunto con personal capacitado
- Cumplir con leyes locales de privacidad y videovigilancia

---

## 🛠️ Troubleshooting

Ver la [Guía Completa](MOBILE_APP_GUIDE.md#parte-5-troubleshooting) para soluciones a problemas comunes.

**Problemas frecuentes:**
- No conecta al servidor → Verificar IP y firewall
- Modelo no encontrado → Entrenar primero con el notebook
- Notificaciones no llegan → Verificar credenciales Firebase/Twilio

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abrir Pull Request

---

## 📝 Roadmap

- [ ] Dashboard web para gestión centralizada
- [ ] Soporte para múltiples cámaras IP
- [ ] Integración con sistemas CCTV
- [ ] Re-entrenamiento automático
- [ ] Detección de objetos adicionales
- [ ] Grabación automática de incidentes
- [ ] API para integración con alarmas

---

## 📄 Licencia

Este proyecto es de código abierto. Usar bajo responsabilidad propia.

---

## 👨‍💻 Autor

**AQuispeR27**

- GitHub: [@AQuispeR27](https://github.com/AQuispeR27)

---

## 🙏 Agradecimientos

- [Ultralytics](https://github.com/ultralytics/ultralytics) por YOLOv11
- [Roboflow](https://roboflow.com/) por el dataset
- [Flutter](https://flutter.dev/) y [FastAPI](https://fastapi.tiangolo.com/)

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar [MOBILE_APP_GUIDE.md](MOBILE_APP_GUIDE.md)
2. Crear un [Issue](https://github.com/AQuispeR27/test_Bringas/issues)

---

**⭐ Si este proyecto te resulta útil, por favor dale una estrella en GitHub!**
