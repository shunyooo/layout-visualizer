from PIL import Image as _Image
from PIL import ImageDraw
from PIL.ImageFont import FreeTypeFont as PILImageFont


def get_font_offset(font: PILImageFont, text: str) -> float:
    image = _Image.new("RGB", (0, 0), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    return draw.textbbox((0, 0), text, font=font, spacing=0)[1]


def get_textsize(
    text: str, font: PILImageFont, spacing: int = 0
) -> tuple[float, float]:
    image = _Image.new("RGB", (0, 0), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=font, spacing=spacing)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
