FROM python:3.12-slim-bookworm


LABEL org.opencontainers.image.source="https://github.com/stjude/proteinpaint" \
    org.opencontainers.image.version="latest"

ARG PORT=5000
ENV PORT=$PORT

#get linux packages
RUN apt-get -y update && apt-get -y install --no-install-recommends \
    libopenjp2-7-dev libopenjp2-tools \
    openslide-tools \
    libgl1 \
    build-essential \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

RUN python3 -m venv /opt/venv && \
    pip install --upgrade pip && \
    pip --no-cache-dir install  gunicorn \
    ## clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /home/root/tileserver

COPY app.py /home/root/tileserver

COPY ./gunicorn_config.py /home/root/tileserver

COPY ./requirements /home/root/tileserver/requirements

COPY ./docs /home/root/tileserver/docs

COPY ./tiatoolbox /home/root/tileserver/tiatoolbox

RUN pip install -r /home/root/tileserver/requirements/requirements_dev.txt

EXPOSE $PORT

# Run gunicorn when the container launches
CMD ["gunicorn", "--config", "/home/root/tileserver/gunicorn_config.py", "app:app"]