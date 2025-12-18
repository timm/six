import ast,sys,random
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

def sub(it, v):
  if v != "?":
    it.n -= 1
    if it.n > 0:
      d = v - it.mu
      it.mu -= d / it.n
      it.m2 -= d * (v - it.mu)
    else: it.mu, it.m2 = 0, 0
  return v

def prob(sym,v): return sym.has.get(v,0) / (sym.n + 1e-32)

def norm(num,n): 
  z = (n - num.mu) / (sd(num) + 1e-32)
  z = max(-3,min(3,z))
  return 1 / (1 + exp(-1.7 * z))

def sd(num): return 1e-32 + (0 if num.n < 2 else sqrt(num.m2/(num.n - 1 )))

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

def cuts(data, best, rest):
  for col1,col2 in zip(best.cols.x, rest.cols.x):
    if Sym is col1.it: 
      cut =  max(col1.has, key=lambda k: win(col1,col2,k)), eq
    else: 
      cut = numCuts(data,best.rows+rest.rows)
    if cut: yield col1,col2, cut

def numCuts(data,rows)
  lo, cut = 1e32, None
  lhs, rhs = Num(), adds(disty(data, r) for r in rows)
  for row in sorted(rows, key=lambda r: r[col.at]):
    y = disty(data, rows[i])
    add(lhs, sub(rhs, y))
    if lhs.n > 1 and rhs.n > 1:
      score = (lhs.n * sd(lhs) + rhs.n * sd(rhs)) / len(rows)
      if score < lo:
        lo, cut = score, obj(at=col.at, txt=col.txt, 
                            op=le if lhs.mu < rhs.mu else gt, 
                            cut=rows[i][col.at])
  return cut

def win(best:Col, rest:Col,v): 
  if Sym is best.it: 
    b,r = prob(best,v), prob(rest,v)
  else:
    b,r = norm(best,v), norm(rest,v)
    if best.mu > rest.mu: b,r = 1-b, 1-r
  return b*b/(r + 1e-32)

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

