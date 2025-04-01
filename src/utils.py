import cairosvg
import io
import requests
from PIL import Image


def svg_to_png(svg_code: str, size: tuple = (384, 384)) -> Image.Image:
    """
    Converts an SVG string to a PNG image using CairoSVG.

    If the SVG does not define a `viewBox`, it will add one using the provided size.

    The background color is set to #999999 and the image is padded 20px on each side.

    Parameters
    ----------
    svg_code : str
        The SVG string to convert.
    size : tuple[int, int], default=(384, 384)
        The desired size of the output PNG image (width, height).

    Returns
    -------
    PIL.Image.Image
        The generated PNG image.
    """

    BG_COLOR = "#999999"

    if "viewBox" not in svg_code:
        svg_code = svg_code.replace("<svg", f'<svg viewBox="0 0 {size[0]} {size[1]}"')

    png_data = cairosvg.svg2png(bytestring=svg_code.encode("utf-8"), background_color=BG_COLOR)
    img = Image.open(io.BytesIO(png_data)).convert("RGB")

    padded_img = Image.new("RGB", (img.width + 40, img.height + 40), BG_COLOR)
    padded_img.paste(img, (20, 20))

    return padded_img


def load_svg_from_url(url: str) -> Image.Image:
    """
    Load an SVG image from a URL and convert it to a PIL Image.

    Args:
        url: URL of the SVG image

    Returns:
        PIL Image object
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    svg_content = response.content.decode("utf-8")

    return svg_to_png(svg_content)
