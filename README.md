# construplan-software-integracion-open-ai
Construplan es una aplicación fullstack en Django 5 que permite a usuarios registrar modelos de construcción, adjuntar planos/imágenes y procesarlos con IA. Integra la API de OpenAI para generar renders (gpt-image-1)  y fichas técnicas (gpt-4o-mini), con fallback local para no interrumpir el flujo. Incluye gestión de usuarios/roles, panel admin, histórico de modelos, descarga de PDF con la imagen generada y ficha técnica embebida, y carga de adjuntos bajo control (PNG/JPG o plano PDF/PNG hasta 20 MB).

Tecnologías:

Backend: Python 3.11/3.12, Django 5, CustomUser con validación de RUT, xhtml2pdf para informes.
IA: OpenAI (imágenes + chat completions), mock de respaldo.
Frontend: Bootstrap 5 + templates con herencia.
Almacenamiento: SQLite para desarrollo; archivos en media/ (adjuntos y resultados IA).
Utilidades: python-dotenv para .env, widget_tweaks para formularios.

