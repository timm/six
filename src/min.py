import ast,math,sys
from math import sqrt,exp
from types import SimpleNamespace as obj

### Constructors --------------------------------------------------------------
def Sym(s=" "): return obj(it=Sym, n=0, txt=s, has={})
def Num(s=" "): return obj(it=Num, n=0, txt=s, mu=0, m2=0, best=str(s)[-1]!="-")

def Col(s): return (Num if s[0].isupper() else Sym)(s)

def Cols(names):
  return obj(names = names, 
             all = (cols := [Col(s) for s in names]),
             x   = [col for col in cols if col.txt[-1] not in "+-X"],
             y   = [col for col in cols if col.txt[-1] in "+-"])

def Data(): return obj(it=Data, rows=[], n=0, cols=[])

### Methods -------------------------------------------------------------------
def add(x,v):
  if n=="?": return n
  x.n += 1
  if x.it==Num:
    d = v - x.mu; x.mu += d/x.n; x.m2 += d*(v - x.mu)
  elif x.it==Sym:
    x.has[v] = 1 + x.has.get(v,0)
  else x.it==Data
    [add(col,v[i]) for i,col in enumerate(x.cols.all)]

def splitNum(num1,num2):
  s1,s2 = sd(num1),sd(num2)
  return (num1.mu/s1 + num2.mu/s2)/(1/s1 + 1/s2 + 1e-9)

def splitSym(sym1,sym2):
  delta = lambda k: sym1.has[k]/sym1.n - sym2.get(k,0)/sym2.n
  return max(sym1.has, key=delta)
  
def deltaNum(best,rest):
  n = splitNum(best,rest)
  return (cdf(best,n)-cdf(rest,n)
          if best.mu<rest.mu else
          (1-cdfNum(best,n))-(1-cdfNum(rest,n)))

def deltaSym(best,rest,k):
  return best.has.get(k,0)/(best.n+1e-9) - rest.has.get(k,0)/(rest.n+1e-9)

### Lib -----------------------------------------------------------------------
def o(x,pre=""):s?
  if hasattr(x,"__dict__"): return o(x.__dict__, x.__name__ or "")
  if type(x) is float: return str(int(x)) if x == int(x) else f"{x:,.2f}"
  if type(x) is list: return pre+"["+', '.join(o(y) for y in x)+"]"
  if type(x) is dict: return pre+"{"+' '.join(f":{k} {o(x[k])}" for k in x)+"}"
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

