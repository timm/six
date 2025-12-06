#!/usr/bin/env python3 -B
# vim: ts=2:sw=2:sts=2:et
from binr import the, o, Data, Num, adds

# -- Helpers -------------------------------------------------------------------
def clone(data, rows): return Data([data.cols.names] + rows)
def score(rows, y):    return adds([r[y.at] for r in rows]).sd

def cuts(c, lo, hi, rows):
  if c.it is not Num: return set(r[c.at] for r in rows if r[c.at]!="?")
  s1, s2 = lo.cols.all[c.at].sd + 1E-32, hi.cols.all[c.at].sd + 1E-32
  mu1, mu2 = lo.cols.all[c.at].mu, hi.cols.all[c.at].mu
  return [(mu1/s1 + mu2/s2) / (1/s1 + 1/s2)]

# -- Main ----------------------------------------------------------------------
def grow(data, lvl=0):
  rows, y = data.rows, data.cols.y[0]
  if len(rows) < the.era or lvl >= the.bins or y.sd < 1e-32:
    return o(mu=y.mu, n=len(rows))

  rows.sort(key=lambda r: r[y.at])
  mid, best = len(rows)//2, o(score=1e32)
  lo, hi = clone(data, rows[:mid]), clone(data, rows[mid:])

  for c in data.cols.x:
    for v in cuts(c, lo, hi, rows):
      yes, no = [], []
      for r in rows:
        if r[c.at] != "?":
          match = r[c.at] < v if c.it is Num else r[c.at] == v
          (yes if match else no).append(r)

      if len(yes) >= the.era and len(no) >= the.era:
        s = (len(yes)*score(yes, y) + len(no)*score(no, y)) / len(rows)
        if s < best.score: best = o(score=s, col=c, val=v, yes=yes, no=no)

  return o(mu=y.mu, n=len(rows)) if best.score > 1e30 else \
         o(mu=y.mu, n=len(rows), col=best.col, val=best.val, 
           left=grow(clone(data, best.yes), lvl+1),
           right=grow(clone(data, best.no), lvl+1))

def show(t, lvl=0):
  if "left" not in t: return print(f"{t.mu:.2f} ({t.n})")
  op, val = ("<", f"{t.val:.2f}") if t.col.it is Num else ("==", t.val)
  print(f"{t.col.of} {op} {val}")
  print(f"{'| '*(lvl+1)}yes: ", end=""); show(t.left, lvl+1)
  print(f"{'| '*(lvl+1)}no:  ", end=""); show(t.right, lvl+1)

if __name__=="__main__": show(grow(Data(the.file)))
