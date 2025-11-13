FROM python:3.14-slim-bookworm AS  builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.14-slim-bookworm AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libmariadb3 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY . .

RUN chmod +x ./entrypoint.sh

RUN --mount=type=secret,id=my-env-file,target=.env,required=true \
    python manage.py collectstatic --noinput --clear

RUN chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "forum_proj.wsgi:application"]