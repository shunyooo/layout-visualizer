# layout-visualizer

[![PyPI version](https://badge.fury.io/py/layout-visualizer.svg)](https://badge.fury.io/py/notion-tqdm) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

Easily draw layout BBoxes



## Features

- Easily draw labeled BBoxes
  - Draw labels without overlap
- Low dependency
  - Only depends on `Pillow` and `Pydantic`



## Installation

```bash
pip install layout-visualizer
```



## Getting started

See [example notebook](./example.ipynb) for more details

```python
from layout_visualizer import draw_label_bboxes

image = ...  # Load PIL Image
label_bboxes = [
    ("Background Color", (0, 0, 1080, 1080)),
    ("BG Color", (0, 0, 1080, 1080)),
    ("Shadow", (0, 0, 1080, 1080)),
    ("Object 1", (138, 426, 942, 870)),
]
draw_label_bboxes(image, label_bboxes, font_size=20, line_width=5)
```

<img src="https://github.com/shunyooo/layout-visualizer/assets/17490886/6d79b894-405b-48fe-9661-5c672b2b5690" height=512/>

(Using psd from <a href="https://jp.freepik.com/free-psd/ramadan-mubarak-islamic-greetings-social-media-post-template_126726406.htm#&position=25&from_view=popular&uuid=7b635cda-4b7e-49a3-ba99-bc9537795d6f">Author: xvector</a> / Dictionary: Freepik)

