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
from math import floor,sqrt,cos,log,exp,pi
from typing import Any,Iterable
import fileinput,random,sys,re
rand = random.random

class o(dict):
  __getattr__, __setattr__ = dict.__getitem__, dict.__setitem__
  def __repr__(i): return show(i)

the = o(bins=7, Budget=30, era=10, p=2, repeats=20, seed=42,
        file="../data/auto93.csv")

Qty  = float | int
Atom = Qty | str | bool
Row  = list[Atom]
Rows = list[Row]
# Num,Sym,Cols = o,o,o      # defined below
# Col  = Num | Sym          # defined below
# Data = tuple[Rows, Cols]  # defined below

# ------------------------------------------------------------------------------
def Sym() -> o: 
  return o(it=Sym, n=0, has={}, bins={})

def Num() -> o:
  return o(it=Num, n=0, mu=0, sd=0, m2=0, bins={})

def Col(at=0, of=" ") -> o:
  it = (Num if of[0].isupper() else Sym)()
  it.at = at
  it.of = of
  it.best = str(of)[-1]!="-" 
  return it

def Cols(names:list[str]) -> o:
  cols = [Col(at=i, of=s) for i,s in enumerate(names)]
  return o(it=Cols, names=names, 
           all = cols,
           x   = [col for col in cols if str(col.of)[-1] not in "+-X"],
           y   = [col for col in cols if str(col.of)[-1] in "+-"])

def Data(rows = None) -> o:
  return adds(rows, o(it=Data, n=0, rows=[], cols=None))

# ------------------------------------------------------------------------------
def add(i: o, # o = Num | Sym | Data, 
        v: Any,
        inc = 1) -> Any: # returns v
  if v=="?": return v
  i.n += inc
  if   i.it is Sym: i.has[v] = inc + i.has.get(v,0)
  elif i.it is Num:
    v = float(v)
    if inc < 0 and i.n < 2:
      i.n = i.mu = i.sd = i.m2 = 0
    else:
      d     = v - i.mu
      i.mu += inc * d / i.n
      i.m2 += inc * d * (v - i.mu)
      i.sd  = 0 if i.n < 2 else sqrt(max(0,i.m2)/(i.n - 1))
  elif i.it is Data:
    if i.cols: 
      row = [add(c, v[c.at], inc) for c in i.cols.all] 
      i.rows.append(row) if inc > 0 else i.rows.remove(row)
    else: i.cols = Cols(v)
  return v

def sub(i,v): return add(i,v,-1)

def adds(src:Iterable = None, it=None ) -> o: # returns it
  it = it or Num()
  if str(src)[-4:]==".csv":
    with open(src, encoding="utf-8") as f:
      for line in f:
        if line: add(it, [s.strip() for s in line.split(",")])
  else: [add(it,row) for row in (src or [])]
  return it

# ------------------------------------------------------------------------------
def norm(num:Num, v:Qty) -> float:
  return 1 / (1 + exp(-1.702 * (v - num.mu)/(num.sd + 1e-32))) 

def bin(col:Col, v:Atom) -> int | Atom:
  return floor( the.bins * norm(col,v) ) if v!="?" and col.it is Num else v 

def dist(src:Iterable) -> float:
  d,n = 0,0
  for d1 in src: 
    n += 1
    d += d1 ** the.p
  return (d/n) ** (1/the.p)

def disty(data:Data, row:Row) -> float:
  return dist(abs(norm(col, row[col.at]) - col.best) for col in data.cols.y)

def distx(data:Data, row1:Row, row2:Row) -> float:
  return dist(_aha(col, row1[col.at], row2[col.at]) for col in data.cols.x)

def _aha(col:Col, a:Atom, b:Atom) -> float:
  if a==b=="?": return 1
  if col.it is Sym : return a != b
  a,b = norm(col,a), norm(col,b)
  a = a if a != "?" else (0 if b>0.5 else 1)
  b = b if b != "?" else (0 if a>0.5 else 1)
  return abs(a - b)

# ------------------------------------------------------------------------------
def scoreGet(data:Data, row:Row) -> Row:
  return sum(x.bins[b].mu for x in data.cols.x 
                          if (b := bin(x,row[x.at])) in x.bins) 

def scorePut(data:Data, row:Row, score:Qty):
  for x in data.cols.x:
    if (b := bin(x, row[x.at])) != "?":
      x.bins[b] = x.bins.get(b) or Num(x.at, b)
      add(x.bins[b], score)

def score(data:Data, eps=0):
  best_score, best_row = 1e32, None
  random.shuffle(data.rows)
  seen, rows, model = set(), data.rows, Data([data.cols.names])
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
def show(x):
  t = type(x)
  if t is o:          return "{"+' '.join(f":{k} {show(x[k])}" for k in x)+"}"
  if t is float:      return str(int(x)) if x == int(x) else f"{x:.3f}"
  if t is type(show): return x.__name__ + '()'
  return str(x)

# ------------------------------------------------------------------------------
def test_h(_) -> None: 
  print(__doc__)

def test__the(_) -> None: 
  print(the)

def test_s(n: str) -> None: 
  the.seed = float(n); random.seed(the.seed)

def test__sym(_) -> None:  
  print(adds("aaaabbc",Sym()))

def test__num(_) -> None:
  def box_muller(mu,sd):
    return mu + sd * sqrt(-2 * log(rand())) * cos(2 * pi * rand()) 
  print(adds(box_muller(10,2) for _ in range(10^4)))

def test__data(f) -> None:
  data = Data(the.file)
  print(data.cols.x[-1])
  print(len(data.rows),data.rows[1])

def test__disty(_):
  ys, data = Num(), Data(the.file)
  Y=lambda row: floor(100*disty(data,row))
  for r in sorted(data.rows,key=Y)[::20]:
    print(Y(r),r)

def test__distx(_):
  xs, data = Num(), Data(the.file)
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
      random.seed(the.seed)
      fn(sys.argv[n+1] if n < len(sys.argv)-1 else None)
