from PIL import Image

IMG_WIDTH = 512

class ImageWrapper:

  def __init__(self, img: Image.Image):
    img = img.convert("RGB")
    height = round(img.height * IMG_WIDTH / img.width)
    img = img.resize((IMG_WIDTH, height), Image.LANCZOS)
    img = img.convert("1")
    self.img = img

    self.placeholder = f"<image {IMG_WIDTH}*{height}>\n"

  def __len__(self):
    return len(self.placeholder)

  def __str__(self):
    return self.placeholder

  def print_to_printer(self, printer):
    printer.image(self.img, center=True)
