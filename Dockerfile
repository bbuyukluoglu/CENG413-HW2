# HW-2 Dockerfile (HW-1 quality checklist still applied).
# 1. Pinned, small base image   -> reproducible, smaller, fewer CVEs
# 2. Dependencies before code   -> build cache works
# 3. Non-root user              -> limits damage if compromised
# 4. No data directory any more -> the app is stateless, state is in PostgreSQL
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create an unprivileged user and switch to it.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
