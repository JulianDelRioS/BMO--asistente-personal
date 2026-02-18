BMO AI – Asistente Virtual Multimodal en Python

BMO AI es un asistente de escritorio desarrollado en Python que integra procesamiento de lenguaje natural, visión computacional y control multimedia en tiempo real.

El sistema combina modelos LLM, reconocimiento de voz, síntesis de voz y APIs externas bajo una arquitectura modular orientada a eventos.

🚀 Stack Tecnológico

Lenguaje: Python 3.x

LLM: Google Gemini (texto + visión multimodal)

UI: Pygame

Speech-to-Text: Google Web Speech API

Text-to-Speech: gTTS + pygame.mixer

Integración Musical: Spotify Web API (OAuth2 con Spotipy)

Visión Artificial: OpenCV

🧠 Características Técnicas Destacadas
1️⃣ Integración Multimodal en Tiempo Real

Procesamiento de voz → interpretación con LLM → ejecución de acciones.

Análisis de imágenes capturadas por webcam mediante modelos multimodales.

Conversaciones contextuales con memoria a corto plazo.

2️⃣ Control Inteligente de Spotify (OAuth2)

Manejo completo de reproducción.

Búsqueda difusa de playlists.

Resolución de ambigüedad mediante diálogo interactivo.

Auto-lanzamiento de Spotify si la aplicación no está abierta.

3️⃣ Sistema de Gestión de Estados

Arquitectura basada en estados (Listening, DJ Mode, Sleep, etc.).

Persistencia del contexto ante interrupciones.

Algoritmo anti-ruido con sistema de strikes para evitar activaciones falsas.

4️⃣ Diseño Modular

Separación de responsabilidades (voz, UI, lógica, integración externa).

Fácil extensión para nuevas capacidades.

Manejo de APIs externas y autenticación segura.

🎯 Objetivo del Proyecto

Explorar la integración práctica de modelos LLM y visión artificial en aplicaciones de escritorio interactivas, priorizando experiencia de usuario, robustez y arquitectura escalable.
