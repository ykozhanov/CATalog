FROM python:3.13

WORKDIR /server

COPY backend/pyproject.toml backend/
COPY backend/uv.lock backend/

COPY db_lib/pyproject.toml db_lib/
COPY db_lib/uv.lock db_lib/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync --directory backend/ --active
RUN uv sync --directory db_lib/ --active

COPY backend/ backend/
COPY db_lib/ db_lib/

ENV FLASK_APP=backend/app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]