import logging
from multiprocessing import Queue

from sanic.log import LOGGING_CONFIG_DEFAULTS, logger

from papierpiano.model import CutCommand, PrintQRCodeCommand, PrintTextCommand


def start_printer(print_queue: Queue):
    logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)  # type: ignore

    printer = None
    try:
        logger.info("Initializing printer")

        from escpos.printer import Usb

        printer = Usb(0x04B8, 0x0E28, profile="TM-T20II")

        logger.info("Printer initialized")

        while True:
            command = print_queue.get()

            match command:
                case CutCommand():
                    logger.info("Cutting")
                    printer.cut()

                case PrintTextCommand(text, cut):
                    logger.info(f"Printing: {text}")
                    printer.text(text)
                    if cut:
                        printer.cut()

                case PrintQRCodeCommand(content, size):
                    logger.info(f"Printing QRCode: {content}")
                    printer.set(align="center")
                    printer.qr(content, size=size, native=True)

                case _:
                    logger.error(f"Unknow command: {command}")

    except KeyboardInterrupt:
        logger.info("Stopping printer")

        if printer is not None:
            printer.close()
        print_queue.close()

        logger.info("Printer stopped")
