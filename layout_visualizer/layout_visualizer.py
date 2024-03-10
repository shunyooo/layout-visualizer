import os
from typing import Callable

from PIL import Image as _Image
from PIL import ImageDraw, ImageFont
from PIL.Image import Image as PILImage
from PIL.ImageDraw import ImageDraw as PILImageDraw
from PIL.ImageFont import FreeTypeFont as PILImageFont

from layout_visualizer.model.bbox import BBox
from layout_visualizer.utils.color import text_to_color
from layout_visualizer.utils.path import get_src_dir
from layout_visualizer.utils.pillow import get_font_offset, get_textsize

# NOTE: Constants

FONTS_DIR = "fonts"
FONT_FILE = "NotoSansJP-Medium.ttf"

# NOTE: Types

Color = tuple[int, int, int] | tuple[int, int, int, int] | str | int
ColorMap = Callable[[str], Color] | dict[str, Color] | None


# NOTE: Sub functions


def _draw_textbox(
    draw: PILImageDraw,
    text: str,
    xy: tuple[float, float],
    font: PILImageFont,
    bg_color: Color,
    font_color: Color,
    padding: tuple[float, float, float, float] = (0, 0, 0, 0),
) -> None:
    """Draw textbox with color background."""
    text_bbox = BBox.from_xywh(xy, get_textsize(text, font)).shift(
        x=padding[0], y=padding[1]
    )
    text_font_offset = get_font_offset(font, text)
    bg_bbox = text_bbox.pad(right=padding[2], bottom=padding[3])
    draw.rectangle(bg_bbox.x1y1x2y2, fill=bg_color)
    draw.text(
        text_bbox.shift(y=-text_font_offset).x1y1,  # remove offset
        text,
        fill=font_color,
        font=font,
        spacing=0,
        align="left",
    )


def _to_color_map_func(
    color_map: ColorMap,
) -> Callable[[str], Color]:
    """Convert color_map to function."""
    if isinstance(color_map, dict):
        return lambda label: color_map[label]
    elif callable(color_map):
        return color_map
    else:
        # Default color map
        return lambda label: text_to_color(label, alpha=0.7)


def _draw_labeled_bbox(
    image: PILImage,
    label: str,
    bbox: BBox,
    bg_color: Color,
    font: PILImageFont,
    line_width: int,
) -> None:
    """Draw label text and bbox rectangle."""
    bbox_image = _Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(bbox_image)
    draw.rectangle(bbox.x1y1x2y2, outline=bg_color, width=line_width)
    _draw_textbox(
        draw,
        label,
        bbox.x1y1,
        font,
        bg_color,
        font_color="white",  # TODO: make it customizable
        padding=(line_width, line_width, line_width, line_width),
    )
    image.alpha_composite(bbox_image)


def _load_font(font_size: int) -> PILImageFont:
    """Load font."""
    return ImageFont.truetype(
        os.path.join(get_src_dir(), FONTS_DIR, FONT_FILE), size=font_size
    )


# NOTE: Main function


def draw_label_bboxes(
    image: PILImage,
    label_bboxes: list[tuple[str, tuple[float, float, float, float]]],
    bg_color_map: ColorMap = None,
    font_size: int = 10,
    line_width: int = 2,
) -> PILImage:
    """Draw labeled bounding boxes on image.

    Args:
        image (PILImage):
                     Pillow image.
        label_bboxes (list[tuple[str, tuple[float, float, float, float]]]):
                     List of label and bbox(x_min, y_min, x_max, y_max).
        bg_color_map (ColorMap, optional):
                     Background Color Map. Defaults is generated from label hash.
        font_size (int, optional):
                     Font size for label text. Defaults to 10.
        line_width (int, optional):
                     Line width for bbox. Defaults to 2.

    Returns:
        PILImage: Image with labeled bounding boxes.
    """
    image = image.copy()
    for label_bbox in label_bboxes:
        label, bbox = label_bbox
        _draw_labeled_bbox(
            image,
            label,
            BBox.from_x1y1x2y2(bbox),
            bg_color=_to_color_map_func(bg_color_map)(label),
            font=_load_font(font_size),
            line_width=line_width,
        )
    return image
