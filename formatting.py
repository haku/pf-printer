def com(*arr):
  return space(*arr, sep=', ')

def space(*arr, sep=" "):
  return sep.join([str(a) for a in arr if a])

def prefix(val, pre):
  if not val:
    return ''
  return f"{pre} {val}"

def suffix(val, suf):
  if not val:
    return ''
  return f"{val} {suf}"
