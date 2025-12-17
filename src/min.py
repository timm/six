import ast,math,sys
from math import sqrt,exp
from types import SimpleNamespace as obj

### Constructors --------------------------------------------------------------
def Sym(s=" "): return obj(it=Sym, n=0, txt=s, has={})
def Num(s=" "): return obj(it=Num, n=0, txt=s, mu=0, m2=0, best=str(s)[-1]!="-")

def _col(s): return (Num if s[0].isupper() else Sym)(s)

def Cols(names):
  return obj(it=Cols, names=names,
             all = (cols := [_col(s) for s in names]),
             x   = [col for col in cols if col.txt[-1] not in "+-X"],
             y   = [col for col in cols if col.txt[-1] in "+-"])

def Data(): return obj(it=Data, rows=[], n=0, cols=None

### Functions -------------------------------------------------------------------
def add(i,v):
  if v=="?": return v
  i.n += 1
  match i.it:
    case Sym: i.has[v] = 1 + i.has.get(v,0)
    case Num: d = v - i.mu; i.mu += d/i.n; i.m2 += d*(v - i.mu)
    case Data:
      if i.cols: [add(col,v[n]) for n,col in enumerate(i.cols.all)]
      else: i.cols = Cols(v)

def where2cut(col1,col1):
  if col1.it is Sym: 
    return max(col1.has, key=lambda k: win(col1,col2,k))
  s1,s2 = sd(col1),sd(col2)
  return (col1.mu/s1 + col2.mu/s2)/(1/s1 + 1/s2 + 1e-32)
  
def win(best:Col, rest:Col,v): # n frosplitNum(best,mrest)
  if best.it is Sym:
    return best.get(k,0) / (best.n + 1e-32) - rest.get(k,0) / (rest.n + 1e-32)
  c1,c2 = cdf(best,v), cdf(rest,v)
  return c1-c2 if best.mu<rest.mu else (1-c1)-(1-c2)

### Lib -----------------------------------------------------------------------
def o(x):
  if type(x) is obj: return x.it.__name__+o(x.__dict__)
  if type(x) is float: return str(int(x)) if x == int(x) else f"{x:,.2f}"
  if type(x) is list: return "["+', '.join(o(y) for y in x)+"]"
  if type(x) is dict: return "{"+' '.join(f":{k} {o(x[k])}" for k in x)+"}"
  return str(x)

def coerce(s):
  try: return ast.literal_eval(s)
  except: return s

def csv(fileName):
  with open(fileName,encoding="utf-8") as f:
    for l in f:
      if (l:=l.split("%")[0].strip()): yield [coerce(x) for x in l.split(",")]

it  = csv(sys.argv[1] if len(sys.argv)>1 else "data.csv")
hdr = next(it)
y   = hdr.index("class")
xs  = [i for i in range(len(hdr)) if i!=y]

def Col(name):
  return Num() if name[0].isupper() else Sym()

best = {i:Col(hdr[i]) for i in xs}
rest = {i:Col(hdr[i]) for i in xs}

for r in it:
  tgt = best if r[y]=="best" else rest
  for i in xs:
    x=r[i]
    if x=="?": continue
    col=tgt[i]
    (addNum(col,float(x)) if col.isNum else addSym(col,x))

out=[]
for i in xs:
  b,r = best[i],rest[i]
  out += ([(deltaNum(b,r),hdr[i],b.lo,b.hi)]
          if b.isNum else
          [(deltaSym(b,r,k),hdr[i],k) for k in b.has])

print(*sorted(out,reverse=True),sep="\n")

