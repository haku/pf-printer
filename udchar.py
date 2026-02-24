class Udchars:
  def __init__(self, placeholder: str, pcols: int, prows: int, pattern: str):
    self.placeholder = placeholder
    self.chars = self.split_chars(len(placeholder), pcols, prows, pattern)

  def print_placeholder(self, printer):
    printer.text(self.placeholder)

  def print_to_printer(self, printer, font: str, times: int = 1):
    for char in self.chars:
      char.print_char(printer=printer, font=font, times=times)

  @staticmethod
  def split_chars(char_count: int, pcols: int, prows: int, pattern: str):
    if char_count * pcols * prows != len(pattern):
      raise ValueError()

    row_length = len(pattern) / prows
    if not row_length.is_integer():
      raise ValueError(f"not int: {row_length}")

    row_length = int(row_length)
    pattern_rows = [pattern[i:i + row_length] for i in range(0, len(pattern), row_length)]

    ret = []
    for i in range(0, char_count):
      x = i * pcols
      char_ptn = ''.join([p[x:x + pcols] for p in pattern_rows])
      ret.append(Udchar(pcols, prows, char_ptn))
    return ret


class Udchar:
  def __init__(self, pcols: int, prows: int, pattern: str):
    self.pcols = pcols
    self.prows = prows
    self.char_bytes = self.mk_char(pcols, prows, pattern)

  def print_char(self, printer, font: str, times: int = 1):
    sub  = bytes(font, "ascii")

    self.prt(printer, [0x1b, b"&", 3, sub, sub])
    self.prt(printer, [self.pcols])
    self.prt(printer, self.char_bytes)
    self.prt(printer, [0x1b, b"%", 1])
    for x in range(0, times):
      self.prt(printer, sub)
    self.prt(printer, [0x1b, b"%", 0])

  @staticmethod
  def prt(printer, data: [bytes | list[int]]):
    output = []
    for b in data:
      if isinstance(b, int):
        output.append(bytes([b]))
      elif isinstance(b, bytes):
        output.append(b)
      else:
        raise ValueException()
    printer._raw(b"".join(output))

  @staticmethod
  def mk_char(pcols: int, prows: int, pattern: str) -> bytes:
    if pcols * prows != len(pattern):
      raise ValueError()

    s = [pattern[i:i + pcols] for i in range(0, len(pattern), pcols)]
    if len(s) != prows:
      raise ValueError(f"wrong number of rows: {len(s)}")

    output = b""
    for col in range(0, pcols):
      for row in range(0, 3):
        byte = ""
        for bit in range(0, 8):
          y = row * 8 + bit
          if y >= prows:
            byte += "0"
          else:
            byte += "0" if s[y][col] == " " else "1"
        output += bytes([int(byte, 2)])
    return output
