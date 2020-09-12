FROM fnndsc/ubuntu-python3

RUN mkdir -p /app
COPY requirements.txt /app
COPY main.py /app

WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]
