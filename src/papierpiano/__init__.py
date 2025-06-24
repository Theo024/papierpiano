import os
from dataclasses import dataclass
from io import BytesIO

from escpos.escpos import Escpos
from escpos.printer import Network
from PIL import Image
from sanic import HTTPResponse, Request, Sanic, file, json
from sanic_ext import openapi, validate

app = Sanic("papierpiano")
app.config.PRINTER_HOST = os.environ["PRINTER_HOST"]
app.config.PRINTER_PORT = os.environ["PRINTER_PORT"]


def compact_char_table(printer, start=4, header=False):
    """Output a compact character table for the current encoding"""
    chars = [" "] * 256
    for i in range(256):
        if i > 32 and i != 127:
            chars[i] = chr(i)
        else:
            chars[i] = " "

    if header:
        printer.set(bold=True)
        printer.text("  0123456789ABCDEF0123456789ABCDEF\n")
        printer.set(bold=False)

    for y in range(start, 8):
        printer.set(bold=True)
        printer.text(f"{y * 2:X} ")
        printer.set(bold=False)
        line = "".join(chars[y * 32 : (y + 1) * 32])
        printer.text(line + "\n")


@app.before_server_start
async def attach_printer(app, _):
    app.ctx.printer = Network(
        app.config.PRINTER_HOST,
        int(app.config.PRINTER_PORT),
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


@app.post("/api/image")
async def image_handler(request: Request) -> HTTPResponse:
    file = request.files.get("file")
    image = Image.open(BytesIO(file.body))
    image.thumbnail((576, image.height), Image.Resampling.LANCZOS)

    printer: Escpos = request.app.ctx.printer
    printer.image(image, impl="graphics", center=True)

    return json({"message": "Printed Image"})


app.static("/assets", "./static/assets/")


@app.get("/")
async def spa_handler(_):
    return await file("./static/index.html")
