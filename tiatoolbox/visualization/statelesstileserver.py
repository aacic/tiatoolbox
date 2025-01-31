import io
import threading
from pathlib import Path

from flask import Flask, Response, send_file

from tiatoolbox.tools.pyramid import ZoomifyGenerator
from tiatoolbox.wsicore import WSIReader


class StatelessTileServer(Flask):

    def __init__(self):
        super().__init__(__name__)
        self.reader = None
        self.reader_lock = threading.Lock()  # Lock for thread safety
        self.route(
            "/tileserver/layer/<layer>/<session_id>/zoomify/TileGroup<int:tile_group>/"
            "<int:z>-<int:x>-<int:y>@<int:res>x.jpg",
        )(
            self.zoomify,
        )

    def zoomify(
        self,
        layer: str,
        session_id: str,
        tile_group: int,  # skipcq: PYL-W0613  #noqa: ARG002
        z: int,
        x: int,
        y: int,
        res: int,
    ) -> Response:
        """Serve a Zoomify tile for a particular layer.

        Note that this should not be called directly, but will be called
        automatically by the Flask framework when a client requests a
        tile at the registered URL.

        Args:
            layer (str):
                The layer name.
            session_id (str):
                Session ID. Unique ID to disambiguate requests from different sessions.
            tile_group (int):
                The tile group. Currently unused.
            z (int):
                The zoom level.
            x (int):
                The x coordinate.
            y (int):
                The y coordinate.
            res (int):
                Resolution to save the tiles at.
                Helps to specify high resolution tiles. Valid options are 1 and 2.

        Returns:
            flask.Response:
                The tile image response.

        """
        try:
            reader = self.get_reader()
            zoomify = ZoomifyGenerator(reader, tile_size=256)
            tile_image = zoomify.get_tile(
                level=z,
                x=x,
                y=y,
                res=res,
                interpolation="optimise",
                transparent_value=None,
            )
        except IndexError:
            return Response("Tile not found", status=404)
        image_io = io.BytesIO()
        tile_image.save(image_io, format="webp")
        image_io.seek(0)
        return send_file(image_io, mimetype="image/webp")

    def get_reader(self) -> WSIReader:
        """Thread-safe lazy-load and cache the WSIReader instance."""
        if self.reader is None:
            with self.reader_lock:  # Ensure only one thread initializes it
                if self.reader is None:  # Double-checked locking
                    self.reader = WSIReader.open(
                        Path(
                            "/path/to/_fsspec.json")
                    )
        return self.reader
