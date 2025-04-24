from datetime import datetime, timedelta
from typing import List

import httpx
from geopy import distance  # type: ignore
from geopy.extra.rate_limiter import RateLimiter  # type: ignore
from geopy.geocoders import Nominatim  # type: ignore
from mcp.server.fastmcp import FastMCP

# Instantiate FastMCP server
mcp = FastMCP("MCP fturno", dependencies=["geopy", "httpx"])

geo_app = Nominatim(user_agent="mcp-fturno", timeout=30.0)
geocode = RateLimiter(geo_app.geocode, min_delay_seconds=1)


@mcp.tool()
async def get_nearby_duty_pharmacies(address: str) -> List[dict]:
    """
    Get ten closest pharmacies on duty today, sorted by distance to the given address.
    """
    headers = {"User-Agent": "mcp-fturno", "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php",
                headers=headers,
                timeout=30.0,
                follow_redirects=True,
            )
            response.raise_for_status()
            all_pharmacies: List[dict] = response.json()
        except Exception as e:
            return []

    # Filter pharmacies that are on duty today
    now = datetime.now()
    fecha_hoy = now.isoformat()[0:10]
    fecha_ayer = (now - timedelta(days=1)).isoformat()[0:10]
    all_pharmacies = list(
        filter(
            lambda f: f["fecha"] == fecha_hoy or f["fecha"] == fecha_ayer,
            all_pharmacies,
        )
    )

    # Sort pharmacies by distance to the given address
    location = geocode(address)
    all_pharmacies.sort(
        key=lambda pto: distance.distance(
            (pto["local_lat"], pto["local_lng"]),
            (location.latitude, location.longitude),
        ).km
    )

    # Return the ten closest pharmacies
    return [
        {
            "name": pharmacy["local_nombre"],
            "address": pharmacy["local_direccion"],
            "phone": pharmacy["local_telefono"],
            "schedule": pharmacy["funcionamiento_hora_apertura"]
            + " - "
            + pharmacy["funcionamiento_hora_cierre"],
            "zone": pharmacy["localidad_nombre"],
        }
        for pharmacy in all_pharmacies[:10]
    ]


if __name__ == "__main__":
    mcp.run()
