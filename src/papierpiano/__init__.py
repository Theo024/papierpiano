import os
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from zoneinfo import ZoneInfo

from escpos.escpos import Escpos
from escpos.printer import Network
from PIL import Image
from sanic import HTTPResponse, Request, Sanic, file, json
from sanic_ext import openapi, validate

app = Sanic("papierpiano")
app.config.PRINTER_HOST = os.environ["PRINTER_HOST"]
app.config.PRINTER_PORT = os.environ["PRINTER_PORT"]


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
    size: int = 16


@app.post("/api/cut")
async def cut_handler(request: Request) -> HTTPResponse:
    printer = request.app.ctx.printer
    printer.cut()

    return json({"message": "Cutted"})


@app.post("/api/print")
@openapi.definition(body={"application/json": PrintBody})
@validate(json=PrintBody)
async def print_handler(request: Request, body: PrintBody) -> HTTPResponse:
    printer: Escpos = request.app.ctx.printer
    printer.set_with_default(align="right")
    printer.textln(
        datetime.now(tz=ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
    )

    printer.textln("─" * 48)
    printer.ln()

    printer.set_with_default(bold=True, double_width=True)
    printer.textln(body.text)

    printer.set_with_default()
    printer.ln()
    printer.textln("─" * 48)

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
    printer.cut()
    printer.set_with_default()

    return json({"message": "Printed QRCode"})


@app.post("/api/image")
async def image_handler(request: Request) -> HTTPResponse:
    file = request.files.get("file")
    image = Image.open(BytesIO(file.body))
    image.thumbnail((576, image.height), Image.Resampling.LANCZOS)

    printer: Escpos = request.app.ctx.printer
    printer.image(image, impl="graphics", center=True)
    printer.ln()

    printer.set_with_default(align="right")
    printer.textln(datetime.now(tz=ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M"))

    caption = request.form.get("caption", "")
    if caption.strip() != "":
        printer.set_with_default(bold=True)
        printer.textln(caption)

    printer.cut()

    return json({"message": "Printed Image"})


app.static("/assets", "./static/assets/")


@app.get("/")
async def spa_handler(_):
    return await file("./static/index.html")
