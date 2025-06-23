import os
from dataclasses import dataclass

from escpos.printer import Network
from sanic import HTTPResponse, Request, Sanic, file, json
from sanic_ext import openapi, validate

app = Sanic("papierpiano")
app.config.PRINTER_HOST = os.environ["PRINTER_HOST"]
app.config.PRINTER_PORT = os.environ["PRINTER_PORT"]


@app.before_server_start
async def attach_printer(app, _):
    app.ctx.printer = Network(
        app.config.PRINTER_HOST,
        app.config.PRINTER_PORT,
        profile="TM-T20II",
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
    printer = request.app.ctx.printer
    printer.cut()

    return json({"message": "Cutted"})


@app.post("/api/print")
@openapi.definition(body={"application/json": PrintBody})
@validate(json=PrintBody)
async def print_handler(request: Request, body: PrintBody) -> HTTPResponse:
    printer = request.app.ctx.printer
    printer.text(body.text)
    if body.cut:
        printer.cut()

    return json({"message": f"Printed {body.text}"})


@app.post("/api/qrcode")
@openapi.definition(body={"application/json": QRCodeBody})
@validate(json=QRCodeBody)
async def qrcode_handler(request: Request, body: QRCodeBody) -> HTTPResponse:
    printer = request.app.ctx.printer
    printer.set(align="center")
    printer.qr(body.content, size=body.size, native=True)

    return json({"message": "Printed QRCode"})


app.static("/assets", "./static/assets/")


@app.get("/")
async def spa_handler(_):
    return await file("./static/index.html")
