# SPDX-FileCopyrightText: 2025-present Luis Saavedra <luis94855510@gmail.com>
#
# SPDX-License-Identifier: MIT
"""MCP duty pharma."""

import logging
from datetime import datetime, timedelta

import httpx
import pytz  # type: ignore
from geopy import distance  # type: ignore
from geopy.extra.rate_limiter import RateLimiter  # type: ignore
from geopy.geocoders import Nominatim  # type: ignore
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)

# Instantiate FastMCP server
mcp = FastMCP("MCP Duty Pharma", dependencies=["geopy", "httpx"])

geo_app = Nominatim(user_agent="mcp-duty-pharma", timeout=30.0)
geocode = RateLimiter(geo_app.geocode, min_delay_seconds=1)


@mcp.tool()
async def get_nearby_duty_pharmacies(address: str) -> list[dict]:
    """Get nearby pharmacies on duty today.

    - sorted by distance to the given address.
    - only ten closest pharmacies are returned.
    - only pharmacies on duty today are returned.

    """
    headers = {"User-Agent": "MCP Duty Pharma", "Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php",
                headers=headers,
                timeout=30.0,
                follow_redirects=True,
            )
            response.raise_for_status()
            all_pharmacies: list[dict] = response.json()
        except httpx.HTTPStatusError:
            return []

    # Filter pharmacies that are on duty today
    now = datetime.now(tz=pytz.timezone("America/Santiago"))
    fecha_hoy = now.isoformat()[0:10]
    fecha_ayer = (now - timedelta(hours=12)).isoformat()[0:10]
    all_pharmacies = list(
        filter(
            lambda f: f["fecha"] == fecha_hoy or f["fecha"] == fecha_ayer,
            all_pharmacies,
        ),
    )

    # Sort pharmacies by distance to the given address
    location = geocode(address)
    valid_pharmacies = []
    for pharmacy in all_pharmacies:
        try:
            lat = float(pharmacy["local_lat"].strip(","))
            lng = float(pharmacy["local_lng"].strip(","))
            valid_pharmacies.append(pharmacy)
            logging.debug(f"Processed lat/lng: {lat}, {lng}")
        except ValueError as e:
            logging.error(
                f"Error processing lat/lng for pharmacy {pharmacy}: {e}"
            )

    valid_pharmacies.sort(
        key=lambda pto: distance.distance(
            (
                float(pto["local_lat"].strip(",")),
                float(pto["local_lng"].strip(",")),
            ),
            (location.latitude, location.longitude),
        ).km,
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
        for pharmacy in valid_pharmacies[:10]
    ]


if __name__ == "__main__":
    mcp.run()
