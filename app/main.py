import logging
import time
from create_models import create_models
logger = logging.getLogger(__name__)

def main():
    create_models()
    while True:
        logger.info("It works!")
        time.sleep(2)

if __name__ == "__main__":
    main()