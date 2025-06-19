import logging
from multiprocessing import Queue

from sanic.log import LOGGING_CONFIG_DEFAULTS, logger


def start_printer(print_queue: Queue):
    printer = None
    try:
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.info("Initializing printer")

        from escpos.printer import Usb

        printer = Usb(0x04B8, 0x0E28, profile="TM-T20II")

        logger.info("Printer initialized")

        while True:
            text = print_queue.get()
            logger.info(f"Printing: {text}")
            printer.text(text)

    except KeyboardInterrupt:
        logger.info("Stopping printer")
        if printer is not None:
            printer.close()
        print_queue.close()
        logger.info("Printer stopped")
