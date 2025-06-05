import logging

logging.basicConfig(
    filename="app/logger/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


logger = logging.getLogger(__name__)
