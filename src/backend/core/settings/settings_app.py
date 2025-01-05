from src.backend.app import app
from src.backend.settings import BPS

for bp in BPS:
    app.register_blueprint(**bp)
