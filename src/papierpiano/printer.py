import logging
from multiprocessing import Queue

from sanic.log import LOGGING_CONFIG_DEFAULTS, logger

from papierpiano.model import CommandType, PrinterCommand


def start_printer(print_queue: Queue):
    logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)  # type: ignore

    printer = None
    try:
        logger.info("Initializing printer")

        from escpos.printer import Usb

        printer = Usb(0x04B8, 0x0E28, profile="TM-T20II")

        logger.info("Printer initialized")

        while True:
            command: PrinterCommand = print_queue.get()
            if command.type == CommandType.CUT:
                logger.info("Cutting")
                printer.cut()
            elif command.type == CommandType.TEXT and command.text is not None:
                logger.info(f"Printing: {command.text}")
                printer.text(command.text)
            else:
                logger.error(f"Unknow command: {command}")
    except KeyboardInterrupt:
        logger.info("Stopping printer")

        if printer is not None:
            printer.close()
        print_queue.close()

        logger.info("Printer stopped")
