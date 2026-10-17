# ─────────────────────────────────────────────────────────────────────────────
#  Dockerfile — Django URL Shortener
#
#  Build:   docker build -t url-shortener .
#  Run:     docker run -p 8000:8000 url-shortener
#  Open:    http://localhost:8000
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Base image ───────────────────────────────────────────────────────
FROM python:3.12-slim

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Prevents Python from buffering stdout/stderr (logs appear instantly)
ENV PYTHONUNBUFFERED=1

# ── Working directory inside the container ────────────────────────────────────
WORKDIR /app

# ── Install dependencies ──────────────────────────────────────────────────────
#  Copy only requirements first so Docker can cache this layer.
#  The layer is only rebuilt when requirements.txt changes.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy the entire project into the container ────────────────────────────────
#  (manage.py lives at the root of URLShortener/, so we copy that folder)
COPY URLShortener/ .

# ── Expose the port Django will listen on ────────────────────────────────────
EXPOSE 8000

# ── Entrypoint: migrate then start the dev server ────────────────────────────
#  We run migrations automatically every time the container starts so the
#  SQLite database is always up-to-date.
#
#  NOTE: Django's built-in runserver is fine for development / demos.
#        For production, swap it with gunicorn:
#          CMD ["gunicorn", "URLShortener.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:8000"]
