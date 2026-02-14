import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import time

def autenticar():
    """Conecta con Spotify pidiendo permisos para controlar la música."""
    # Agregamos 'user-read-playback-state' para poder encontrar tu dispositivo
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=config.SPOTIPY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state user-read-currently-playing"
    ))

def obtener_dispositivo_activo(sp):
    """Busca dónde está sonando la música para enviarle la orden."""
    dispositivos = sp.devices()
    for d in dispositivos['devices']:
        if d['is_active']:
            return d['id']
    
    # Si no hay ninguno "activo", devolvemos el primero de la lista (probablemente tu PC)
    if dispositivos['devices']:
        return dispositivos['devices'][0]['id']
    return None

def reproducir_cancion(busqueda):
    """Busca una canción y le da play automáticamente."""
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        
        resultados = sp.search(q=busqueda, limit=1, type='track')
        
        if resultados['tracks']['items']:
            uri_cancion = resultados['tracks']['items'][0]['uri']
            nombre = resultados['tracks']['items'][0]['name']
            artista = resultados['tracks']['items'][0]['artists'][0]['name']
            
            # Forzamos el play en el dispositivo detectado
            sp.start_playback(device_id=device_id, uris=[uri_cancion])
            return f"Reproduciendo {nombre} de {artista}."
        else:
            return "No encontré esa canción."
            
    except Exception as e:
        print(f"❌ Error Spotify: {e}")
        return "Asegúrate de tener Spotify abierto. No pude conectar."
    
def pausar_musica():
    """Pausa la música que se está reproduciendo actualmente."""
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        sp.pause_playback(device_id=device_id)
        return "Música pausada."
    except Exception as e:
        print(f"❌ Error pausando: {e}")
        return "No pude pausar, parece que no hay nada sonando."

def siguiente_cancion():
    """Salta a la siguiente canción en la lista de Spotify."""
    try:
        sp = autenticar()
        device_id = obtener_dispositivo_activo(sp)
        
        if device_id:
            sp.next_track(device_id=device_id)
            return "¡Cambio de ritmo! Poniendo la siguiente."
        else:
            return "No encuentro tu Spotify activo para cambiar la canción."
            
    except Exception as e:
        print(f"❌ Error cambiando canción: {e}")
        return "No pude cambiar de canción."