from dataclasses import dataclass
from multiprocessing import Queue

from sanic import HTTPResponse, Request, Sanic, file, json
from sanic_ext import openapi, validate

from papierpiano.model import CommandType, PrinterCommand
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
class PrintCommand:
    text: str


@app.post("/api/cut")
async def cut_handler(request: Request) -> HTTPResponse:
    request.app.shared_ctx.print_queue.put(PrinterCommand(CommandType.CUT))
    return json({"message": "Cutted"})


@app.post("/api/print")
@openapi.definition(body={"application/json": PrintCommand})
@validate(json=PrintCommand)
async def print_handler(request: Request, body: PrintCommand) -> HTTPResponse:
    request.app.shared_ctx.print_queue.put(PrinterCommand(CommandType.TEXT, body.text))
    return json({"message": f"Printed {body.text}"})


app.static("/assets", "./static/assets/")


@app.get("/")
async def spa_handler(request):
    return await file("./static/index.html")
