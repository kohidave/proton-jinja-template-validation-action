FROM python:3.10-slim
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app Jinja2
RUN pip install --target=/app pyyaml

ENV PYTHONPATH /app
CMD [ "python", "/app/main.py" ]
