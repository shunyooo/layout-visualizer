import os

import pytest
from PIL import Image as _Image
from PIL import ImageChops, ImageStat
from PIL.Image import Image as PILImage

from layout_visualizer import draw_label_bboxes


@pytest.fixture
def image():
    return _Image.new("RGBA", (200, 200), color="white")


def _image(name: str) -> PILImage:
    return _Image.open(os.path.join("tests", "assets", "label_images", f"{name}.png"))


def _eq(image1: PILImage, image2: PILImage) -> bool:
    diff = ImageChops.difference(image1, image2)
    return sum(ImageStat.Stat(diff).sum) == 0


class TestDrawLabelBBoxes:
    def test_normal_empty(self, image: PILImage):
        label_bboxes = []
        result = draw_label_bboxes(image, label_bboxes)
        assert result == image

    def test_normal_multi_labels(self, image: PILImage):
        label_bboxes: list[tuple[str, tuple]] = [
            ("Label 1", (10, 10, 50, 50)),
            ("Label 2", (30, 30, 140, 100)),
        ]
        result = draw_label_bboxes(image, label_bboxes)
        assert _eq(result, _image("multi_labels"))

    def test_normal_multi_labels_avoid_right(self, image: PILImage):
        label_bboxes: list[tuple[str, tuple]] = [
            ("Label 1", (10, 10, 50, 50)),
            ("Label 2", (10, 10, 140, 100)),
        ]
        result = draw_label_bboxes(image, label_bboxes, avoid_label_to="right")
        assert _eq(result, _image("multi_labels_avoid_right"))

    def test_normal_multi_labels_avoid_bottom(self, image: PILImage):
        label_bboxes: list[tuple[str, tuple]] = [
            ("Label 1", (10, 10, 50, 50)),
            ("Label 2", (10, 10, 140, 100)),
        ]
        result = draw_label_bboxes(image, label_bboxes, avoid_label_to="bottom")
        assert _eq(result, _image("multi_labels_avoid_bottom"))

    def test_multi_labels_color_map_dict(self, image: PILImage):
        label_bboxes: list[tuple[str, tuple]] = [
            ("Label 1", (10, 10, 50, 50)),
            ("Label 2", (30, 30, 140, 100)),
        ]
        result = draw_label_bboxes(image, label_bboxes, bg_color_map={"Label 1": "red"})
        assert _eq(result, _image("multi_labels_color_map_dict"))

    def multi_labels_color_map_func(self, image: PILImage):
        label_bboxes: list[tuple[str, tuple]] = [
            ("Label 1", (10, 10, 50, 50)),
            ("Label 2", (30, 30, 140, 100)),
        ]
        color_func = lambda label: "red" if label == "Label 1" else "blue"  # noqa
        result = draw_label_bboxes(image, label_bboxes, bg_color_map=color_func)
        assert _eq(result, _image("multi_labels_color_map_func"))
