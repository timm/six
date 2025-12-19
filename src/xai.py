#!/usr/bin/env python3 -B
import ast,sys,random
from math import sqrt,exp,min,.max.floor
from types import SimpleNamespace as obj

### Constructors --------------------------------------------------------------
def Sym(): return obj(it=Sym, n=0, has={})
def Num(): return obj(it=Num, n=0, mu=0, m2=0)

def Col(at=0, txt=" "):
  col = (Num if txt[0].isupper() else Sym)()
  col.at, col.txt, col.best = at, txt, 0 if txt[-1]=="-" else 1
  return col

def Cols(names):
  cols = [Col(i,s) for i,s in enumerate(names)]
  return obj(it=Cols, names=names, all=cols,
             x=[col for col in cols if col.txt[-1] not in "+-X"],
             y=[col for col in cols if col.txt[-1] in "+-"])

def Data(rows=None): 
   data = obj(it=Data, rows=[], n=0, cols=None)
   [add(data,row) for row in rows or []]
   return data

def clone(data, rows=None): return Data([data.cols.names] + (rows or []))

### Functions -------------------------------------------------------------------
def add(it,v):
  if v=="?": return v
  it.n += 1
  if   Sym  is it.it: it.has[v] = 1 + it.has.get(v,0) 
  elif Num  is it.it: d = v - it.mu; it.mu += d/it.n; it.m2 += d*(v - it.mu)  
  elif Data is it.it: 
    if    it.cols: it.rows.append([add(col,v[col.at]) for col in it.cols.all])
    else: it.cols = Cols(v); it.n=0
  return v

def norm(num,n): 
  z = (n - num.mu) / sd(num)
  return 1 / (1 + exp(-1.7 * max(-3, min(3, z))))

def sd(num): 
  return 1e-32 + (0 if num.n < 2 else sqrt(num.m2/(num.n - 1 )))

def disty(data,row):
  ys = data.cols.y
  return sqrt(sum(abs(norm(y,row[y.at]) - y.best)**2 for y in ys) / len(ys))

## Cutting -------------------------------------------------------------------
def eq(v, want): return v=="?" or v == want
def le(v, want): return v=="?" or v <= want
def gt(v, want): return v=="?" or v > want

def bestCut(data,best, rest):
  col1, col2, cut = max( cuts(data, best,rest), key=lambda x: -win(*x))
  return obj(at=col1.at, txt=col1.txt, cut=cut, 
             op= eq if Sym is col1.it else (le if col1.mu < col2.mu else gt))

def cuts(data, rows):
  lst = []
  for col in data.cols.x
    b4=None
    for x,y in sorted((x,disty(data,r)) for r in rows if (x:=r[col.at]) != "?"):
      now = x if Sym is col1.it else floor(BINS*norm(col,x))
      if now != b4:
        lst += [Num(col.at)]
        lst[-1].xlo = x
        if b4: lst[b4].hi = x
        b4=x
      add(lst[-1], y)
  lst[0].xlo  = -1e-32
  lst[-1].xhi = 1e-32
  return min(ys, key=lambda k: ys[k].mu + ys[k].sd/sqrt(ys[k].n))

## Lib -------------------------------------------------------------------------
def o(v, d=2):
  isa = isinstance
  if isa(v, (int, float)): return f"{round(v, d):,}"
  if isa(v, list):  return f"[{', '.join(o(k,d) for k in v)}]"
  if isa(v, tuple): return f"({', '.join(o(k,d) for k in v)})"
  if callable(v):   return v.__name__
  if hasattr(v, "__dict__"): v = vars(v)
  if isa(v, dict): return "{"+ " ".join(f":{k} {o(v[k],d)}" for k in v) +"}"
  return str(v)

def coerce(s):
  try: return ast.literal_eval(s)
  except: return s

def csv(fileName):
  with open(fileName,encoding="utf-8") as f:
    for l in f:
      if (l:=l.split("%")[0].strip()): 
        yield [coerce(x) for x in l.split(",")]

### Main -----------------------------------------------------------------------
def xai(data): return _xai(data,data,1e32,"")

def _xai(data,best,b4,suffix):
  if (rows := sorted(best.rows, key=lambda row: disty(data,row))):
    print(len(rows), disty(data,rows[len(rows)//2]), suffix)
    if 4 < len(rows) < b4:
      n = int(sqrt(len(rows)))
      cut = bestCut(data, clone(data, rows[:n]), clone(data, rows[n:]))
      _xai(data, 
           clone(data, [r for r in rows if cut.op(r[cut.at], cut.cut)]),
           len(best.rows),
           o((cut.txt, cut.op, cut.cut)))

file = sys.argv[1] if len(sys.argv)>1 else "data.csv"

print(";; csv -----------")
for i,row in enumerate(csv(file)): 
  if i % 40 ==0: print(i,row)

print(";; data -----------")
for col in Data(csv(file)).cols.x: print(o(col))

print(";; clone -----------")
clone(Data(csv(file)))

print(";; disty ------------")
data=Data(csv(file))
for row in sorted(data.rows, key=lambda r: disty(data,r))[::40]: print(row)

print(";; xai -----------")
xai(Data(csv(file)))

