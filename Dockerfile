# We always start from an existing container
FROM python:3.10-alpine
#3.8.2

# Copy dependency lists into container
COPY requirements.txt .
COPY requirements-dev.txt .

RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip install -r requirements.txt; \
    pip install -r requirements-dev.txt; \
	apk del .build-deps;

# Copy our code into the container
COPY app.py .

# Copy the HTML page templates directory
COPY templates templates

# Copy the version number into the container
COPY VERSION.txt .

# Our code runs on port 5000, so allow access
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP app.py

# This is the command that is executed when the container starts
# Note we've added --host=0.0.0.0 as by default only local users would
# be able to access the application.
# CMD [ "flask", "run", "--host=0.0.0.0" ]
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "APP_DISPATCH"]