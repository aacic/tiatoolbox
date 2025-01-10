from flask_cors import CORS

from tiatoolbox.visualization.tileserver import TileServer

# Initialize and run the TileServer
app = TileServer(
    title="Tiatoolbox TileServer",
    layers={},
)
CORS(app, send_wildcard=True)

# Gunicorn will look for 'app' in this script
if __name__ == "__main__":
    # Only for development; use gunicorn for production
    app.run(host="0.0.0.0", port=5000)
