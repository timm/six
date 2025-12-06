#!/usr/bin/env python3 -B
# vim: ts=2:sw=2:sts=2:et
"""
binr.py : build rules via stochastic incremental XAI
(c) 2025, Tim Menzies, timm@ieee.org, mit-license.org

Options:
 -h             Show help.
 -b  bins=7     Number of bins for discretization (int).
 -B  Budget=30  Max rows to eval (int).
 -e  era=10     Number of rows in an era (int)
 -p  p=2        Distance coefficient
 -r  repeats=20 Number of experimental repeats (int).
 -s  seed=42    Random number seed (int).
 -f  file=../data/auto93.csv File to load (str).
"""
from types import SimpleNamespace as o
from math import floor,sqrt,cos,log,exp,pi
from typing import Any,Iterable
import fileinput,random,sys,re
rand = random.random

the = o(bins=7, Budget=30, era=10, p=2, repeats=20, seed=42,
        file="../data/auto93.csv")

QTY  = float | int
ATOM = QTY | str 
ROW  = list[ATOM]
ROWS = list[ROW]
NUM,SYM,COLS = o,o,o      # redefined below
COL  = NUM | SYM          # redefined below
DATA = tuple[ROWS, COLS]  # redefined below

# ------------------------------------------------------------------------------
def SYM() -> SYM: 
  return o(it=SYM, n=0, has={}, bins={})

def NUM() -> NUM: 
  return o(it=NUM, n=0, mu=0, sd=0, m2=0, bins={})

def COL(at=0, of=" ") -> COL: 
  it = (NUM if of[0].isupper() else SYM)()
  it.at = at
  it.of = of
  it.best = str(of)[-1]!="-" 
  return it

def COLS(names: list[str]) -> COLS:
  t = [COL(at=i, of=s) for i,s in enumerate(names)]
  return o(it=COLS, names=names, 
           all = t,
           x   = [c for c in t if c.of[-1] not in "+-X"],
           y   = [c for c in t if c.of[-1] != "X" and c.of[-1] in "+-"])

def DATA(rows: ROWS = None) -> DATA:      
  return adds(rows, o(it=DATA, n=0, rows=[], cols=None))

# ------------------------------------------------------------------------------
def add(i: o, v: ATOM | ROW) -> ATOM | ROW: 
  if v=="?": return v
  i.n += 1
  if   SYM is i.it: i.has[v] = 1 + i.has.get(v,0)
  elif NUM is i.it:
    v = float(v)
    d = v - i.mu
    i.mu += d/i.n
    i.m2 += d*(v - i.mu)
    i.sd  = 0 if i.n < 2 else sqrt(i.m2/(i.n - 1))
  elif DATA is i.it:
    if i.cols: 
      i.rows += [[add(c,v[c.at]) for c in i.cols.all]] 
    else: i.cols = COLS(v)
  return v

def adds(src: str | Iterable = None, it: o | None = None ) -> o:
  it = it or NUM()
  if str(src)[-4:]==".csv":
    with open(src, encoding="utf-8") as f:
      for line in f:
        if line: add(it, [s.strip() for s in line.split(",")])
  else: [add(it,row) for row in (src or [])]
  return it

# ------------------------------------------------------------------------------
def norm(num: NUM, v: ATOM) -> float:
  return 1 / (1 + exp(-1.702 * (v - num.mu)/(num.sd + 1e-32))) 

def bin(col: COL, v: ATOM) -> int | ATOM:
  return floor( the.bins * norm(col,v) ) if v!="?" and NUM is col.it else v 

def dist(src: Iterable) -> float:
  d,n=0,0
  for d1 in src: 
    n += 1
    d += d1 ** the.p
  return (d/n) ** (1/the.p)

def disty(data: DATA, row: ROW) -> float:
  return dist(abs(norm(col, row[col.at]) - col.best) for col in data.cols.y)

def distx(data: DATA, row1: ROW, row2: ROW) -> float:
  return dist(_aha(col, row1[col.at], row2[col.at]) for col in data.cols.x)

def _aha(col: COL, a: ATOM, b: ATOM) -> float:
  if a==b=="?": return 1
  if SYM is col.it : return a != b
  a,b = norm(col,a), norm(col,b)
  a = a if a != "?" else (0 if b>0.5 else 1)
  b = b if b != "?" else (0 if a>0.5 else 1)
  return abs(a - b)

# ------------------------------------------------------------------------------
def scoreGet(data,row):
  return sum(x.bins[b].mu for x in data.cols.x 
                          if (b := bin(x,row[x.at])) in x.bins) 

def scorePut(data,row,score):
  for x in data.cols.x:
    if (b := bin(x, row[x.at])) != "?":
      x.bins[b] = x.bins.get(b) or NUM(x.at, b)
      add(x.bins[b], score)

def score(data, eps=0):
  best_score, best_row = 1e32, None
  random.shuffle(data.rows)
  seen, rows, model = set(), data.rows, DATA([data.cols.names])
  for j, row in enumerate(rows):
    if len(seen) >= the.Budget: break
    add(model, row) 
    scorePut(model, row, disty(model, rows))
    seen.add(id(row))
    if j % the.era == 0:
      candidate = min(rows[j+1 : j+20], key=lambda r: scoreGet(model, r))
      seen.add(id(candidate))
      if (score := disty(model, candidate)) < best_score - eps:
        best_score, best_row = score, candidate
    return best_row

# ------------------------------------------------------------------------------
def test_h(_) -> None: 
  print(__doc__)

def test__the(_) -> None: 
  print(the)

def test_s(n: str) -> None: 
  the.seed = float(n); random.seed(the.seed)

def test__sym(_) -> None:  
  print(adds("aaaabbc",SYM()))

def test__num(_) -> None:
  def box_muller(mu,sd):
    return mu + sd * sqrt(-2 * log(rand())) * cos(2 * pi * rand()) 
  print(adds(box_muller(10,2) for _ in range(100)))

def test__data(f) -> None:
  data = DATA(the.file)
  print(data.cols.x[-1])
  print(len(data.rows))

def test__disty(_):
  ys, data = NUM(), DATA(the.file)
  Y=lambda row: floor(100*disty(data,row))
  for r in sorted(data.rows,key=Y)[::20]:
    print(Y(r),r)

def test__distx(_):
  xs, data = NUM(), DATA(the.file)
  X=lambda row1: floor(100*distx(data,row1, data.rows[0]))
  for r in sorted(data.rows,key=X)[::20]:
    print(X(r),r)
  
_tests= {k:fun for k,fun in vars().items() if "test__" in k}

def test__all(_):
  for k,fun in _tests.items(): print("\n----- "+k); fun(_)

# ------------------------------------------------------------------------------
if __name__ == "__main__":
  for n, s in enumerate(sys.argv):
    if fn := vars().get(f"test{s.replace('-', '_')}"): 
      fn(sys.argv[n+1] if n < len(sys.argv)-1 else None)
