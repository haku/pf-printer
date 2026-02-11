import re

class Dice:
  def __init__(self, count, sides):
    self.count = count
    self.sides = sides

  def __str__(self):
    if self.sides <= 1:
      return str(self.count)
    return f"{self.count}d{self.sides}"

  def mul(self, times):
    return Dice(times * self.count, self.sides)

  def append(self, b):
    if self.sides == b.sides:
      return [Dice(self.count + b.count, self.sides)]
    return [self, b]


def parse(dice):
  m = re.match(r"^([0-9]*)(?:d([0-9]+))?$", dice)
  if not m:
    raise Exception(f"invalid dice: {dice}")

  count = int(m.group(1)) if m.group(1) else 1
  sides = int(m.group(2)) if m.group(2) else 1
  return Dice(count, sides)
