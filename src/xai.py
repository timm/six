import ast,math,sys,random
from math import sqrt,exp
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

def Data(rows=None): return adds(rows, obj(it=Data, rows=[], n=0, cols=None))

def clone(data, rows=None): return Data([data.cols.names] + (rows or []))

### Functions -------------------------------------------------------------------
def adds(src, it=None):
  it = it or Num(); [add(it, x) for x in src]; return it

def add(it,v):
  if v=="?": return v
  it.n += 1
  if   Sym  is it.it: it.has[v] = 1 + it.has.get(v,0) 
  elif Num  is it.it: d = v - it.mu; it.mu += d/it.n; it.m2 += d*(v - it.mu)  
  elif Data is it.it: 
    if    it.cols: it.rows.append([add(col,v[col.at]) for col in it.cols.all])
    else: it.cols = Cols(v); it.n=0
  return v

def bestCut(best,rest):
  cuts= [(c1,c2,cut(c1,c2)) for c1,c2 in zip(best.cols.x, rest.cols.x)]
  c1,c2,where = max(cuts, key=lambda x: -win(*x))
  return obj(at=c1.at, txt=c1.txt, cut=where, 
             op= eq if Sym is c1.it else (le if c1.mu < c2.mu else gt))

def eq(v, want): return v=="?" or v == want
def le(v, want): return v=="?" or v <= want
def gt(v, want): return v=="?" or v > want

def cut(col1,col2):
  if Sym is col1.it: 
    return max(col1.has, key=lambda k: win(col1,col2,k))
  w1, w2 = 1/sd(col1), 1/sd(col2)
  return (w1 * col1.mu + w2 * col2.mu) /(w1 + w2 + 1e-32)

def win(best:Col, rest:Col,v): 
  if Sym is best.it:
    b,r = best.has.get(v,0)/(best.n + 1e-32), rest.has.get(v,0)/(rest.n + 1e-32)
  else:
    b,r = norm(best,v), norm(rest,v)
    if best.mu > rest.mu: b,r= 1-b, 1-r
  return b*b/(r + 1e-32)

def norm(num,n): return 1 / (1 + exp(-1.7 * (n - num.mu)/(sd(num) + 1e-32))) 

def sd(num):     return 1e-32 + (0 if num.n < 2 else sqrt(num.m2/(num.n - 1 )))

def disty(data,row):
  ys = data.cols.y
  return sqrt(sum(abs(norm(y,row[y.at]) - y.best)**2 for y in ys) / len(ys))

## Lib -------------------------------------------------------------------------
def o(v, d=2):
  isa = isinstance
  if isa(v, float): return str(round(v, d))
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
def xai(data, suffix=""):
  rows = sorted(data.rows, key=lambda row: disty(data,row))
  n = len(rows)//2
  print(o(disty(data,rows[n])), suffix)
  if len(rows) > 4: 
    go = bestCut(clone(data, rows[:n]), clone(data,rows[n:]))
    xai(clone(data, [row for row in rows if go.op(row[go.at], go.cut)]),
        o((go.txt,go.op, go.cut)))

fileName = sys.argv[1] if len(sys.argv)>1 else "data.csv"

print(";; csv -----------")
for i,row in enumerate(csv(fileName)): 
  if i % 30 ==0: print(i,row)
print(";; data -----------")
for col in Data(csv(fileName)).cols.x: print(o(col))
print(";; clone -----------")
clone(Data(csv(fileName)))
print(";; xai -----------")
xai(Data(csv(fileName)))

