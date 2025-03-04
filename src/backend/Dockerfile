FROM python:3.12.9

WORKDIR /server

COPY backend/pyproject.toml src/backend/
COPY backend/uv.lock src/backend/

COPY db_lib/pyproject.toml src/db_lib/
COPY db_lib/uv.lock src/db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv pip install src/backend/ --system
RUN uv pip install src/db_lib/ --system

COPY backend src/backend/
COPY db_lib src/db_lib/

ENV FLASK_APP=/server/src/backend/app.py
ENV PYTHONPATH=/server/

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]