import logging
from datetime import datetime
import sys


def setup_logging():
    """
    Configure logging for the application.
    """
    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create a handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Configure specific loggers
    logging.getLogger('src').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)  # Reduce SQLAlchemy noise


def log_task_operation(operation: str, user_id: str, task_id: str = None, success: bool = True):
    """
    Log task operations for audit trail.
    """
    logger = logging.getLogger('src.services.task_service')

    if success:
        if task_id:
            logger.info(f"Task {operation}: user_id={user_id}, task_id={task_id}")
        else:
            logger.info(f"Task {operation}: user_id={user_id}")
    else:
        if task_id:
            logger.warning(f"Task {operation} failed: user_id={user_id}, task_id={task_id}")
        else:
            logger.warning(f"Task {operation} failed: user_id={user_id}")


# Initialize logging when module is imported
setup_logging()