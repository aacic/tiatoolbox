"""Module to run TileServer for testing purpose."""

from flask_cors import CORS

from tiatoolbox.visualization import TileServer

# Initialize and run the TileServer
tile_server = TileServer(
    title="Tiatoolbox TileServer",
    layers={},
)
CORS(tile_server, send_wildcard=True)


tile_server.run(host="127.0.0.1", port=5000)
