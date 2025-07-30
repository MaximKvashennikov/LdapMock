import logging

def setup_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:     %(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler("mock.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)
