BMO AI es un asistente virtual de escritorio interactivo. Construido en Python, BMO combina la potencia de Google Gemini para conversaciones naturales, Spotify para control musical avanzado y Pygame para una interfaz visual expresiva y reactiva.

A diferencia de los asistentes genéricos, BMO tiene personalidad, "ojos" para ver el mundo real y un "oído selectivo" inteligente para no interrumpir la música.

🛠️ Tecnologías Utilizadas (Tech Stack)
El núcleo de BMO está construido modularmente utilizando las siguientes tecnologías:

Lenguaje: Python 3.x 🐍

Cerebro (LLM): Google Gemini 1.5 Pro/Flash API (Generación de texto y visión).

Interfaz Visual (UI): Pygame (Renderizado de caras y estados: Happy, Listening, Music, Sleep, etc.).

Voz (TTS/STT):

Input: SpeechRecognition (Google Web Speech API).

Output: gTTS (Google Text-to-Speech) + pygame.mixer.

Música (DJ Mode): Spotipy (Spotify Web API) con autenticación OAuth2.

Visión: OpenCV (Captura de imágenes) + Análisis multimodal con Gemini.

✨ Funcionalidades Actuales
🧠 1. Inteligencia Conversacional & Personalidad
Conversaciones fluidas y contextuales gracias a Gemini.

Personalidad definida ("System Prompt").

Memoria a Corto Plazo: Recuerda el contexto de la charla inmediata.

🎧 2. DJ BMO (Integración Profunda con Spotify)
Control Total: Reproducir, Pausar, Siguiente canción.

Búsqueda Inteligente de Playlists:

Modo Directo: "Pon mi playlist Rock" (Busca coincidencia exacta o difusa).

Modo Interactivo: Si dices "Pon mi playlist", BMO lista tus listas y te pregunta cuál quieres.

Normalización: Ignora errores de espacios o mayúsculas ("Mi  Playlist" == "mi playlist").

Auto-Arranque: Si Spotify está cerrado en el PC, BMO lo abre automáticamente antes de ejecutar la orden.

Búsqueda Global: Si no encuentra la canción/lista en tu biblioteca, busca en el catálogo global de Spotify.

👁️ 3. Visión Computarizada
Comando: "BMO, mira esto" o "¿Qué ves?".

BMO toma una foto con la webcam, la envía a Gemini Vision y describe lo que ve o responde preguntas sobre la imagen.

🛡️ 4. Robustez y Gestión de Estado
Sistema de "Strikes" (Anti-Ruido): Si BMO detecta ruido 4 veces seguidas sin identificar voz (ej. música alta), desactiva su micrófono temporalmente (10s) para no interrumpir.

Persistencia de Estado: Si interrumpes el modo música con ruido, BMO recuerda que era DJ y vuelve a ponerse los auriculares.

Modo Sueño: Se "duerme"  tras inactividad.
