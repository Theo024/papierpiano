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


def get_printer():
    return Network(
        app.config.PRINTER_HOST,
        int(app.config.PRINTER_PORT),
        profile="TM-T20II",
    )


def wrap_text(text, max_width=48):
    if not text:
        return []

    paragraphs = text.split("\n")
    lines = []

    for paragraph in paragraphs:
        if not paragraph.strip():  # Empty line or whitespace only
            lines.append("")
            continue

        words = paragraph.split()
        current_line = ""

        for word in words:
            # If a single word is longer than max_width, break it
            if len(word) > max_width:
                # Add current line if it exists
                if current_line:
                    lines.append(current_line)
                    current_line = ""

                # Break the long word into chunks
                while len(word) > max_width:
                    lines.append(word[:max_width])
                    word = word[max_width:]

                # Set remaining part as current line
                current_line = word
            # Check if adding this word would exceed the limit
            elif current_line and len(current_line) + 1 + len(word) > max_width:
                # Start a new line
                lines.append(current_line)
                current_line = word
            else:
                # Add word to current line
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word

        # Add the last line if it's not empty
        if current_line:
            lines.append(current_line)

    return lines


@dataclass
class PrintBody:
    text: str
    cut: bool = True


@dataclass
class TodoBody:
    todos: list[str]


@dataclass
class QRCodeBody:
    content: str
    size: int = 16


@app.post("/api/cut")
async def cut_handler(request: Request) -> HTTPResponse:
    printer = get_printer()
    printer.cut()

    return json({"message": "Cutted"})


@app.post("/api/print")
@openapi.definition(body={"application/json": PrintBody})
@validate(json=PrintBody)
async def print_handler(request: Request, body: PrintBody) -> HTTPResponse:
    printer: Escpos = get_printer()
    printer.set_with_default(align="right")
    printer.textln(
        datetime.now(tz=ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
    )

    printer.set_with_default()

    printer.textln("─" * 48)
    printer.ln()

    for line in wrap_text(body.text):
        printer.textln(line)

    printer.ln()
    printer.textln("─" * 48)

    if body.cut:
        printer.cut()

    return json({"message": f"Printed {body.text}"})


@app.post("/api/todo")
@openapi.definition(body={"application/json": TodoBody})
@validate(json=TodoBody)
async def todo_handler(request: Request, body: TodoBody) -> HTTPResponse:
    printer: Escpos = get_printer()
    printer.set_with_default(align="right")
    printer.textln(
        datetime.now(tz=ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
    )

    printer.set_with_default()

    printer.textln("─" * 48)
    printer.ln()

    for idx, todo in enumerate(body.todos):
        if idx > 0:
            printer.ln()

        printer.set_with_default(double_width=True, bold=True)
        printer.text("[]")
        printer.set_with_default()
        printer.text(" ")

        for idx, line in enumerate(wrap_text(todo, max_width=21)):
            if idx > 0:
                printer.set_with_default(double_width=True, bold=True)
                printer.text("  ")
                printer.set_with_default()
                printer.text(" ")

            printer.set_with_default(double_width=True)
            printer.textln(line)

    printer.set_with_default()
    printer.ln()
    printer.textln("─" * 48)

    printer.cut()

    return json({"message": "Printed Todo"})


@app.post("/api/qrcode")
@openapi.definition(body={"application/json": QRCodeBody})
@validate(json=QRCodeBody)
async def qrcode_handler(request: Request, body: QRCodeBody) -> HTTPResponse:
    printer = get_printer()
    printer.set_with_default(align="center")
    printer.qr(body.content, size=body.size, native=True)
    printer.cut()
    printer.set_with_default()

    return json({"message": "Printed QRCode"})


@app.post("/api/image")
async def image_handler(request: Request) -> HTTPResponse:
    file = request.files.get("file")
    image = Image.open(BytesIO(file.body))
    image.thumbnail((576, image.height), Image.Resampling.LANCZOS)

    printer: Escpos = get_printer()
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
