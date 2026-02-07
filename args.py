import argparse

class Args:
  def __init__(self):
    self.parser = argparse.ArgumentParser()
    self.args = None

  def add_argument(self, *args, **kwargs):
    self.parser.add_argument(*args, **kwargs)

  def __getattr__(self, name):
    if not self.args:
      self.args = self.parser.parse_args()
    return self.args.__getattribute__(name)

  def get_required(self, name):
    val = self.__getattr__(name)
    if not val:
      self.need_arg(name)
    return val

  def need_arg(self, name):
    print(f"Missing arg: --{name}")
    sys.exit(1)

ARGS = Args()
