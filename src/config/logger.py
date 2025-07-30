import logging
from pathlib import Path


log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "mock.log"

def setup_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:     %(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)
