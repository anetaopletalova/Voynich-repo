FROM python:3.8-slim

ENV PYTHONUNBUFFERED True

## Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install Packages
RUN pip install -r requirements.txt

# Set an environment variable for the port for 8080
ENV PORT 8080
ENV DATABASE_URL postgresql+psycopg2://postgres:postgres@voynich-344713%3Aeurope-central2%3Avoynichdb:5432/voynichdb

# Run gunicorn bound to the 8080 port.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app