import base64
import json
import re
from html import unescape
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageChops, ImageDraw, ImageOps

folder = Path(__file__).resolve().parent / "images"

folder.mkdir(exist_ok=True)
url = "https://eggpicnic.com/create-your-own-flock-australia/"
page = urlopen(url).read().decode()
gallery = page.split("Our Complete Australian Birdlife Collection", 1)[1]
figures = re.findall(
    r'<figure class="wp-block-image[^"]*">(.*?)</figure>', gallery, re.S
)
source_pattern = r'(?:data-src|src)="([^"]+/wp-content/uploads/[^"]+)"'
for i, figure in enumerate(figures):
    source = unescape(re.findall(source_pattern, figure)[0])
    caption = re.findall(r"<figcaption[^>]*>(.*?)</figcaption>", figure, re.S)[0]
    name = unescape(re.sub(r"<[^>]+>", "", caption)).strip().replace("/", "-")
    with urlopen(source) as response, Image.open(response) as image:
        image = image.convert("RGB")
    # A common source canvas height preserves relative bird sizes after cropping.
    image = image.resize(
        (round(image.width * 600 / image.height), 600), Image.Resampling.LANCZOS
    )
    width, height = image.size
    background = Image.new("RGB", image.size, image.getpixel((0, 0)))
    red, green, blue = ImageChops.difference(image, background).split()
    difference = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    mask = difference.point(lambda value: 255 if value > 24 else 0)
    mask = ImageOps.expand(mask, 1, 0)
    # Remove edge-connected background while keeping enclosed pale plumage.
    ImageDraw.floodfill(mask, (0, 0), 128)
    alpha = mask.crop((1, 1, width + 1, height + 1)).point(
        lambda value: 0 if value == 128 else 255
    )
    image.putalpha(alpha)
    image.crop(alpha.getbbox()).save(folder / f"{name}.webp", quality=90, method=6)
    print(f"{i + 1}/{len(figures)} {name}", flush=True)

birds = []
for path in sorted(folder.glob("*.webp")):
    with Image.open(path) as image:
        bird = dict(name=path.stem, w=image.width, h=image.height, sourceH=600)
    data = base64.b64encode(path.read_bytes()).decode()
    birds.append(dict(bird, image=f"data:image/webp;base64,{data}"))

# Data URLs keep canvas PNG export working when the HTML is opened directly from disk.
(folder / "catalogue.js").write_text(
    "const birds=" + json.dumps(birds, separators=(",", ":")) + ";\n"
    "const images=birds.map(bird=>{const image=new Image();"
    "image.src=bird.image;return image});\n"
)
print(f"Exported {len(birds)} birds to {folder / 'catalogue.js'}")
