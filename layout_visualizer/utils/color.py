import colorsys
import hashlib
import unicodedata


def text_to_color(text: str, alpha: float = 1.0) -> str:
    text = unicodedata.normalize("NFKC", text)
    hash_object = hashlib.md5(text.encode())
    hash_number = int(hash_object.hexdigest(), 16)
    r, g, b = colorsys.hsv_to_rgb((hash_number % 360) / 360.0, 1, 0.75)
    color_code = "#{:02x}{:02x}{:02x}{:02x}".format(
        int(r * 255), int(g * 255), int(b * 255), int(alpha * 255)
    )
    return color_code
