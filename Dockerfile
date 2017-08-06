FROM hypriot/rpi-python

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    make \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python", "-u", "start.py"]
