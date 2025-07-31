"""Hello world application module for testing GitHub workflows."""

import logging
import logging.config
import signal
import sys
import threading
import types
from pathlib import Path
from typing import Optional

import yaml

shutdown_event = threading.Event()


def signal_handler(signum: int, frame: Optional[types.FrameType]) -> None:
    """Handle shutdown signals gracefully.

    Args:
        signum: Signal number received
        frame: Current stack frame (can be None)
    """
    logger = logging.getLogger(__name__)
    try:
        signal_name = signal.Signals(signum).name
    except (AttributeError, ValueError):
        signal_name = str(signum)
    logger.info(f"Received {signal_name} signal, shutting down gracefully...")
    shutdown_event.set()


def setup_signal_handlers() -> None:
    """Setup signal handlers for graceful shutdown across different OS platforms."""
    logger = logging.getLogger(__name__)

    try:
        signal.signal(signal.SIGINT, signal_handler)
        logger.debug("Registered SIGINT handler")
    except (AttributeError, OSError) as e:
        logger.warning(f"Could not register SIGINT handler: {e}")

    try:
        signal.signal(signal.SIGTERM, signal_handler)
        logger.debug("Registered SIGTERM handler")
    except (AttributeError, OSError) as e:
        logger.debug(f"SIGTERM not available on this platform: {e}")

    if sys.platform == "win32":
        try:
            signal.signal(signal.SIGBREAK, signal_handler)
            logger.debug("Registered SIGBREAK handler for Windows")
        except (AttributeError, OSError) as e:
            logger.debug(f"Could not register SIGBREAK handler: {e}")


def setup_logging() -> None:
    """Setup logging configuration from YAML file.

    Loads the logging configuration from config/logging_config.yaml
    and applies it to the root logger.
    """
    logging_configuration_path = getattr(
        sys, "_MEIPASS", Path(__file__).parent.parent / "config" / "logging_config.yaml"
    )
    if "_MEI" in str(logging_configuration_path):
        logging_configuration_path = (
            Path(logging_configuration_path) / "config" / "logging_config.yaml"
        )

    try:
        with open(logging_configuration_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            logging.config.dictConfig(config)
    except FileNotFoundError:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)-4s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        logging.error(f"Logging config file not found at {logging_configuration_path}")
    except Exception as e:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)-4s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )
        logging.error(f"Error loading logging config: {e}")


def log_hello_world() -> None:
    """Log a simple Hello World message.

    This function demonstrates basic logging functionality
    for testing GitHub workflow configurations.
    """
    logger = logging.getLogger(__name__)
    logger.info("Hello World")
    logger.info("Hello User!")


def run_continuous_logging() -> None:
    """Run continuous logging every 5 seconds until shutdown signal received."""
    logger = logging.getLogger(__name__)
    logger.info("Starting continuous logging (every 5 seconds)...")
    logger.info("Press Ctrl+C to stop")

    try:
        while not shutdown_event.is_set():
            log_hello_world()

            if shutdown_event.wait(timeout=5.0):
                break

    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, shutting down gracefully...")
        shutdown_event.set()

    logger.info("Logging stopped")


def main() -> None:
    """Main entry point for the hello world application."""
    setup_logging()
    setup_signal_handlers()
    run_continuous_logging()


if __name__ == "__main__":
    main()
