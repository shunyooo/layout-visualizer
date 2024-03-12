import os
from typing import Callable, Literal, Mapping

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
ColorMap = Callable[[str], Color] | Mapping[str, Color] | None
AvoidLabelTo = Literal["right", "bottom"]


# NOTE: Sub functions


def _draw_textbox(
    draw: PILImageDraw,
    text: str,
    xy: tuple[float, float],
    font: PILImageFont,
    bg_color: Color,
    font_color: Color,
    padding: tuple[float, float, float, float],
    avoid_bboxes: list[BBox],
    avoid_to: AvoidLabelTo,
) -> BBox:
    """Draw textbox with color background."""
    content_bbox = BBox.from_xywh(xy, get_textsize(text, font)).shift(
        x=padding[0], y=padding[1]
    )
    text_font_offset = get_font_offset(font, text)
    bg_bbox = content_bbox.pad(right=padding[2], bottom=padding[3])

    for avoid_bbox in avoid_bboxes:
        # shift bbox if duplicate position
        if bg_bbox.is_collision(avoid_bbox):
            if avoid_to == "right":
                _diff = avoid_bbox.x2 - bg_bbox.x1
                bg_bbox = bg_bbox.shift(x=_diff)
                content_bbox = content_bbox.shift(x=_diff)
            elif avoid_to == "bottom":
                _diff = avoid_bbox.y2 - bg_bbox.y1
                bg_bbox = bg_bbox.shift(y=_diff)
                content_bbox = content_bbox.shift(y=_diff)
            else:
                raise ValueError(f"Invalid avoid_position: {avoid_to}")

    draw.rectangle(bg_bbox.x1y1x2y2, fill=bg_color)
    draw.text(
        content_bbox.shift(y=-text_font_offset).x1y1,  # remove offset
        text,
        fill=font_color,
        font=font,
        spacing=0,
        align="left",
    )
    return bg_bbox


def _to_color_map_func(
    color_map: ColorMap,
) -> Callable[[str], Color]:
    """Convert color_map to function."""

    def default_func(label: str):
        return text_to_color(label, alpha=0.7)

    if isinstance(color_map, dict):
        return lambda label: color_map.get(label, default_func(label))
    elif callable(color_map):
        return color_map
    else:
        return default_func


def _draw_labeled_bbox(
    image: PILImage,
    label: str,
    bbox: BBox,
    bg_color: Color,
    font: PILImageFont,
    line_width: int,
    avoid_text_bboxes: list[BBox],
    avoid_to: AvoidLabelTo,
) -> tuple[BBox, BBox]:
    """Draw label text and bbox rectangle."""
    bbox_image = _Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(bbox_image)
    draw.rectangle(bbox.x1y1x2y2, outline=bg_color, width=line_width)
    text_bbox = _draw_textbox(
        draw,
        label,
        bbox.x1y1,
        font,
        bg_color,
        font_color="white",  # TODO: make it customizable
        padding=(line_width, line_width, line_width, line_width),
        avoid_bboxes=avoid_text_bboxes,
        avoid_to=avoid_to,
    )
    image.alpha_composite(bbox_image)
    return bbox, text_bbox


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
    avoid_label_to: AvoidLabelTo = "right",
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
    image = image.copy().convert("RGBA")
    avoid_text_bboxes = []
    bg_color_map = _to_color_map_func(bg_color_map)
    for label_bbox in label_bboxes:
        label, bbox = label_bbox
        _, text_bbox = _draw_labeled_bbox(
            image,
            label,
            BBox.from_x1y1x2y2(bbox),
            bg_color=bg_color_map(label),
            font=_load_font(font_size),
            line_width=line_width,
            avoid_text_bboxes=avoid_text_bboxes,
            avoid_to=avoid_label_to,
        )
        avoid_text_bboxes.append(text_bbox)
    return image
