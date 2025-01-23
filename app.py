"""Module to run TileServer for testing purpose."""

import logging

from flask_cors import CORS

from tiatoolbox.visualization.tileserver import TileServer

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("aiohttp").setLevel(logging.DEBUG)
logging.getLogger("aiohttp.client").setLevel(logging.DEBUG)

# Initialize and run the TileServer
app = TileServer(
    title="Tiatoolbox TileServer",
    layers={},
)
CORS(app, send_wildcard=True)

# Gunicorn will look for 'app' in this script
if __name__ == "__main__":
    # Replace host="0.0.0.0"
    app.run(host="127.0.0.1", port=5000)
