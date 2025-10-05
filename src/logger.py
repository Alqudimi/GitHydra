"""Logging system for GitHydra"""

import logging
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler

LOG_DIR = Path.home() / ".githydra" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logging():
    """Setup logging configuration"""
    log_file = LOG_DIR / f"githydra_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            RichHandler(rich_tracebacks=True, show_time=False, show_path=False)
        ]
    )

def get_logger(name: str):
    """Get logger instance"""
    return logging.getLogger(name)

def log_command(command: str, success: bool, message: str = ""):
    """Log command execution"""
    logger = get_logger("githydra.command")
    if success:
        logger.info(f"Command '{command}' executed successfully. {message}")
    else:
        logger.error(f"Command '{command}' failed. {message}")
