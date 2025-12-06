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
 -p  p=2        Distance coeffecient
 -r  repeats=20 Number of experimental repeats (int).
 -s  seed=42    Random number seed (int). 
 -f  file=../data/auto93.csv File to load (str).
"""
from types import SimpleNamespace as o
from math import pi,exp,log,cos,sqrt,floor
import fileinput,random,sys,re
rand = random.random

the = o(bins=7, Budget=30, era=10, p=2, repeats=20, seed=42,
        file="..data/auto93.csv")

# -----------------------------------------------------------------------------
def DATA(rows=[]):     
  return adds(rows, o(it=DATA, n=0, rows={}, cols=None))

def COL(at=0, of=" "): 
  it = (NUM if of[0].isupper() else SYM)()
  it.at = at
  it.of = of
  it.goal = 0 if str(of)[-1]=="-" else 1
  return it

def SYM(): 
  return o(it=SYM, n=0, has={})

def NUM(): 
  return o(it=NUM, n=0, mu=0, sd=0, m2=0)

def COLS(names):
  t = [COL(at=i, of=s) for i,s in enumerate(names)]
  return o(it=COLS, names=names, 
           all = t,
           x   = [c for col in t if c.of[-1] not in "+-X"],
           y   = [c for col in t if c.of[-1] != "X" and c.of in "+-"])

# -----------------------------------------------------------------------------
def add(i,v): 
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
    if i.data.cols: 
      i.rows += [[add(c,v[c.at]) for c in i.data.cols.all]] 
    else: i.data.cols = COLS(v)
  return v

def adds(src=[], it=None):
  it = it or NUM()
  if type(src)==str and src[-4:]==".csv":
    with open(src, encoding="utf-8") as f:
      for line in f:
        if line: add(it, [s.strip() for s in line.split(",")])
  else: [add(it,row) for row in iter(src)]
  return it

# -----------------------------------------------------------------------------
def norm(num,v):
  return 1 / (1 + exp(-1.702 * (v - num.mu)/(num.sd + 1e-32))) 

def bin(col,v):
  return floor( the.bins * norm(col,v) ) if v!="?" and NUM is col.it else v 

def dist(src):
  d,n=0,0
  for d1 in src: n,d = n+1,d1**the.p
  return (d/n) ** (1/the.p)

def disty(data, row):
  return dist(abs(norm(col, row[col.at]) - col.best) for col in data.cols.y)

# -----------------------------------------------------------------------------
def test_h(_): print(__doc__)

def test__the(_): print(the)

def test_s(n): the.seed = float(n); random.seed(the.seed)

def test__sym(_):  print(adds("aaaabbc",SYM()))

def test__nums(_):
  def box_muller(mu,sd):
    return mu + sd * sqrt(-2 * log(rand())) * cos(2 * pi * rand()) 
  print(adds(box_muller(10,2) for _ in range(100)))

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  for n, s in enumerate(sys.argv):
    if fn := vars().get(f"test{s.replace('-', '_')}"): 
      fn(sys.argv[n+1] if n < len(sys.argv)-1 else None)
