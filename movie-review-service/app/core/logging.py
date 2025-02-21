import logging
from app.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create logger
    logger = logging.getLogger('movie_reviews')
    
    # Add file handler
    fh = logging.FileHandler('app.log')
    fh.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(fh)
    
    return logger

logger = setup_logging() 