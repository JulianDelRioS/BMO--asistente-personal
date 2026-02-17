import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import os
import time

def autenticar():
    """Conecta con Spotify pidiendo permisos para controlar la música y LEER PLAYLISTS."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=config.SPOTIPY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative"
    ))

def obtener_dispositivo_activo(sp):
    """Busca un dispositivo. Si no hay ninguno, intenta abrir Spotify en Windows."""
    try:
        # Intento 1: Buscar dispositivos ya disponibles
        dispositivos = sp.devices()
        
        # A. Si hay uno sonando ahora mismo, usalo
        for d in dispositivos['devices']:
            if d['is_active']:
                return d['id']
        
        # B. Si hay dispositivos en lista (pero en pausa), usa el primero (tu PC)
        if dispositivos['devices']:
            return dispositivos['devices'][0]['id']
            
        # C. 🚨 EMERGENCIA: Lista vacía. Abrimos Spotify.
        print("⚠️ No veo Spotify abierto. Iniciando aplicación...")
        os.system("start spotify")  # Comando para Windows
        
        print("⏳ Esperando 8 segundos a que Spotify cargue...")
        time.sleep(8) # Damos tiempo a que el programa arranque
        
        # Intento 2: Buscar de nuevo tras abrirlo
        dispositivos = sp.devices()
        if dispositivos['devices']:
             return dispositivos['devices'][0]['id']
             
    except Exception as e:
        print(f"❌ Error buscando dispositivos: {e}")
        
    return None

def reproducir_cancion(busqueda):
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        
        if not device_id:
            return "No pude encontrar tu Spotify. Ábrelo manualmente por favor."

        resultados = sp.search(q=busqueda, limit=1, type='track')
        if resultados['tracks']['items']:
            uri = resultados['tracks']['items'][0]['uri']
            nombre = resultados['tracks']['items'][0]['name']
            artista = resultados['tracks']['items'][0]['artists'][0]['name']
            
            # Forzamos el play en el dispositivo detectado
            sp.start_playback(device_id=device_id, uris=[uri])
            return f"Reproduciendo {nombre} de {artista}."
        else:
            return "No encontré esa canción."
    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error al conectar con Spotify."

# ⬇️ NUEVA FUNCIÓN VITAL PARA EL MODO INTERACTIVO
def listar_mis_playlists(limite=6):
    """Devuelve una lista de texto con los nombres de tus primeras playlists."""
    try:
        sp = autenticar()
        mis_playlists = sp.current_user_playlists(limit=limite)
        
        nombres = []
        for pl in mis_playlists['items']:
            nombres.append(pl['name'])
            
        return nombres
    except Exception as e:
        print(f"❌ Error listando playlists: {e}")
        return []

def reproducir_playlist(nombre_playlist):
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        
        if not device_id:
            return "No detecto Spotify abierto."

        print(f"📂 Buscando playlist: '{nombre_playlist}'...") 
        
        # Función auxiliar para limpiar texto (quita espacios dobles y mayúsculas)
        def limpiar(texto):
            return " ".join(str(texto).lower().split())

        busqueda_limpia = limpiar(nombre_playlist)
        
        # Obtenemos tus playlists
        mis_playlists = sp.current_user_playlists(limit=50)
        
        # 1. Búsqueda Local (Flexible)
        for playlist in mis_playlists['items']:
            nombre_real = playlist['name']
            nombre_real_limpio = limpiar(nombre_real)
            
            # Comparamos las versiones limpias
            # Esto hace que "mi playlist  2025" sea igual a "mi playlist 2025"
            if busqueda_limpia in nombre_real_limpio:
                sp.start_playback(device_id=device_id, context_uri=playlist['uri'])
                return f"Reproduciendo: {nombre_real}."
        
        # 2. PLAN B: Búsqueda Global
        print("⚠️ No la encontré en tu biblioteca local. Buscando en todo Spotify...")
        resultados = sp.search(q=nombre_playlist, type='playlist', limit=1)
        
        if resultados['playlists']['items']:
            playlist_encontrada = resultados['playlists']['items'][0]
            sp.start_playback(device_id=device_id, context_uri=playlist_encontrada['uri'])
            return f"Encontré esta lista pública: {playlist_encontrada['name']}."

        return f"No encontré ninguna playlist que coincida con '{nombre_playlist}'."
            
    except Exception as e:
        print(f"❌ Error Playlist: {e}")
        return "Error al buscar la playlist."

def pausar_musica():
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        if device_id:
            sp.pause_playback(device_id=device_id)
            return "Música pausada."
    except:
        pass
    return "No pude pausar."

def siguiente_cancion():
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        if device_id:
            sp.next_track(device_id=device_id)
            return "Siguiente canción."
    except:
        pass
    return "No pude cambiar."