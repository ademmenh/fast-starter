import uvicorn
import logging
from pathlib import Path
from src.app import create_app
from src.config.domain.interface import IConfig
from src.config.infrastructure.adapter import ConfigAdapter
from src.shared.infrastructure.logger import GZipTimedRotatingFileHandler, JsonFormatter

config: IConfig = ConfigAdapter()

# Logging (Console + File for development)
LOGS_DIR = Path(__file__).resolve().parents[1] / config.logs_dirname
LOGS_DIR.mkdir(parents=True, exist_ok=True)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.handlers.clear()

# Console handler
console = logging.StreamHandler()
console.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
root.addHandler(console)

# File handler
file_handler = GZipTimedRotatingFileHandler(
    filename=LOGS_DIR / "app.log",
    when="midnight",
    interval=1,
    backupCount=config.retention_days,
    encoding="utf-8",
    utc=True,
)
file_handler.setFormatter(JsonFormatter())
file_handler.suffix = "%Y-%m-%d"
root.addHandler(file_handler)

# Route uvicorn logs through our handlers
for uvicorn_logger in ("uvicorn", "uvicorn.access", "uvicorn.error"):
    lg = logging.getLogger(uvicorn_logger)
    lg.handlers = []
    lg.propagate = True

app = create_app(config=config, show_docs=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.port)
