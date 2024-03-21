from src.server import app
from src.app.config import logging_config
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)