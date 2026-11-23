from geopy.geocoders import Nominatim
from typing import Tuple, Optional
import time

geolocator = Nominatim(user_agent="pat_turismo_app")


def obtener_coordenadas_exactas(
    nombre: str,
    direccion: Optional[str],
    ciudad: str
) -> Tuple[Optional[float], Optional[float]]:

    """
    Busca las coordenadas de la forma más precisa posible.
    """

    consultas = []

    # 1. Nombre + Dirección + Ciudad
    if direccion:
        consultas.append(
            f"{nombre}, {direccion},  Colombia"
        )

    # 2. Dirección + Ciudad
    if direccion:
        consultas.append(
            f"{direccion}, Colombia"
        )

    # 3. Nombre + Ciudad
    consultas.append(
        f"{nombre},  Colombia"
    )

    # 4. Solo Dirección
    if direccion:
        consultas.append(
            f"{direccion}, Colombia"
        )

    # 5. Solo Nombre
    consultas.append(
        f"{nombre}, Colombia"
    )

    try:

        for consulta in consultas:

            location = geolocator.geocode(
                consulta,
                addressdetails=True
            )

            if location:

                return (
                    round(location.latitude, 8),
                    round(location.longitude, 8)
                )

            # OpenStreetMap recomienda no hacer consultas muy seguidas
            time.sleep(1)

        return None, None

    except Exception as e:

        print(
            f"Error obteniendo coordenadas: {e}"
        )

        return None, None

def buscar_lugar(texto: str) -> Optional[dict]:
    """
    Busca un lugar escrito por el usuario (dirección o sitio de referencia)
    y devuelve sus coordenadas. Solo busca dentro de Colombia.
    """
    try:
        location = geolocator.geocode(
            texto,
            addressdetails=True,
            country_codes="co",
            language="es",
            timeout=10
        )
    except Exception as e:
        print(f"Error buscando lugar: {e}")
        return None

    if not location:
        return None

    address = location.raw.get("address", {})

    ciudad = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
    )

    barrio = (
        address.get("neighbourhood")
        or address.get("suburb")
    )

    return {
        "latitud": round(location.latitude, 8),
        "longitud": round(location.longitude, 8),
        "nombre_mapa": location.address,
        "ciudad": ciudad,
        "barrio": barrio
    }
