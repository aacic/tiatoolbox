"""Module to run TileServer for testing purpose."""

import logging

from flask_cors import CORS

from tiatoolbox.visualization import TileServer
from tiatoolbox.wsicore import WSIReader

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("aiohttp").setLevel(logging.DEBUG)
logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)

svs = "/path/to/fsspec.json"

reader = WSIReader.open(svs)

# Initialize and run the TileServer
tile_server = TileServer(
    title="Tiatoolbox TileServer",
    layers={},
)
CORS(tile_server, send_wildcard=True)


tile_server.run(host="127.0.0.1", port=5000)
