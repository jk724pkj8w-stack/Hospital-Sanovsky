# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).


# Hospital Sanosvky - Sistema de Gestión Médica

Una plataforma integral web para la gestión de servicios hospitalarios, que facilita el control de pacientes, especialistas y la programación de citas médicas. Construida con una arquitectura moderna que separa el cliente interactivo de una API robusta y escalable.

## Características Principales

- **Gestión de Citas:** Creación, asignación y seguimiento de citas entre pacientes y especialistas mediante validación estricta de datos.
- **Expedientes Clínicos:** Registro y consulta del historial médico vinculado a cada perfil.
- **Autenticación Segura:** Acceso protegido a las rutas del panel principal (Dashboard) verificando el estado de la sesión del usuario.
- **API RESTful:** Backend estructurado para garantizar la consistencia en la base de datos y la creación dinámica de entidades vinculadas.

## Stack Tecnológico

**Frontend:**
- **Framework:** Vue.js 3 (Composition API)
- **Construcción y Herramientas:** Vite, npm
- **Enrutamiento:** Vue Router
- **Autenticación:** Firebase Auth
- **Estilos:** Bootstrap, FontAwesome

**Backend:**
- **Framework:** FastAPI (Python)
- **Validación de Datos:** Pydantic
- **Base de Datos:** Google Cloud Firestore (NoSQL)

##  Configuración y Despliegue

El proyecto está dividido en dos entornos que deben configurarse y ejecutarse para el desarrollo local.

### 1. Configuración del Backend (FastAPI)

1. Navegar al directorio del backend.
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
3. Instalar las dependencias principales:
    pip install fastapi uvicorn google-cloud-firestore pydantic python-dotenv
4. Configurar las variables de entorno creando un archivo .env en la raíz del backend con:
    GOOGLE_APPLICATION_CREDENTIALS="ruta/a/tus/credenciales/firebase-adminsdk.json"
    API_KEY="tu_secreto_aqui"
5. Iniciar el servidor de desarrollo:
    uvicorn main:app --reload

### 2. Configuración del Frontend (Vue.js + Vite)
1. Navegar al directorio del frontend.
2. Instalar las dependencias de Node: 
    npm install
3. Configurar las variables de entorno creando un archivo .env en la raíz del frontend para proteger las credenciales de inicialización:
    VITE_FIREBASE_API_KEY="tu_api_key"
    VITE_FIREBASE_AUTH_DOMAIN="hospital-sanosvky-19c12.firebaseapp.com"
    VITE_FIREBASE_PROJECT_ID="hospital-sanosvky-19c12"
    VITE_FIREBASE_STORAGE_BUCKET="hospital-sanosvky-19c12.firebasestorage.app"
    VITE_FIREBASE_MESSAGING_SENDER_ID="106705125175"
    VITE_FIREBASE_APP_ID="1:106705125175:web:383cebaaebce16002924b2"
4. Iniciar el servidor de Vite:
    npm run dev


