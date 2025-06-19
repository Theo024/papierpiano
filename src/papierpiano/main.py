from dataclasses import dataclass
from multiprocessing import Queue

from sanic import HTTPResponse, Request, Sanic, file, json
from sanic_ext import openapi, validate

from papierpiano.model import CutCommand, PrintQRCodeCommand, PrintTextCommand
from papierpiano.printer import start_printer

app = Sanic("papierpiano")


@app.main_process_start
async def main_process_start(app):
    app.shared_ctx.print_queue = Queue()


@app.main_process_ready
async def main_process_ready(app: Sanic, _):
    app.manager.manage(
        "Printer",
        start_printer,
        {"print_queue": app.shared_ctx.print_queue},
        transient=True,
    )


@dataclass
class PrintBody:
    text: str
    cut: bool = True


@dataclass
class QRCodeBody:
    content: str
    size: int = 3


@app.post("/api/cut")
async def cut_handler(request: Request) -> HTTPResponse:
    request.app.shared_ctx.print_queue.put(CutCommand())
    return json({"message": "Cutted"})


@app.post("/api/print")
@openapi.definition(body={"application/json": PrintBody})
@validate(json=PrintBody)
async def print_handler(request: Request, body: PrintBody) -> HTTPResponse:
    request.app.shared_ctx.print_queue.put(PrintTextCommand(body.text, body.cut))
    return json({"message": f"Printed {body.text}"})


@app.post("/api/qrcode")
@openapi.definition(body={"application/json": QRCodeBody})
@validate(json=QRCodeBody)
async def qrcode_handler(request: Request, body: QRCodeBody) -> HTTPResponse:
    request.app.shared_ctx.print_queue.put(PrintQRCodeCommand(body.content, body.size))
    return json({"message": "Printed QRCode"})


app.static("/assets", "./static/assets/")


@app.get("/")
async def spa_handler(_):
    return await file("./static/index.html")
