import logging
import time

logger = logging.getLogger(__name__)

def main():
    while True:
        logger.info("It works!")
        time.sleep(2)

if __name__ == "__main__":
    main()