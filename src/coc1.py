#!/usr/bin/env python3 -B
import random, math
from binr import obj

PROJs, RXs = obj(), obj()

def q(lo=1, hi=None, ako="*") -> q: 
  return obj(it=q, lo=lo ,hi=hi or lo, ako=ako)

def with(q1:q,q2:None) -> q:
  if q2:
    return v(lo=max(q1.lo,q2.lo), hi=min(q1.hi,q2.hi), ako=q1.ako or q2.ako)
  return q1

def defaults():
  s,n,p = "*-+"
  return obj(
    kloc= q(2,2000,"ksloc"),
    locf= q(1),
    prec= q(1,6,s), flex= q(1,6,s), arch= q(1,6,s), 
    team= q(1,6,s), pmat= q(1,6,s), 

    acap= q(1,6,n), aexp= q(1,6,n), ltex= q(1,6,n), pcap= q(1,6,n),
    pcon= q(1,6,n), plex= q(1,6,n), sced= q(1,6,n), site= q(1,6,n), 
    tool= q(1,6,n), cplx= q(1,6,p), data= q(2,5,p), docu= q(1,6,p),

    pvol= q(2,5,p), rely= q(1,6,p), ruse= q(2,6,p), stor= q(3,6,p), 
    time= q(3,6,p))

PROJs.OSP= obj(
  ksloc= q(75,125),
  prec= q(1,2), flex= q(2,5), resl= q(1,3), team= q(2,3), 
  pmat= q(1,4), stor= q(3,5), ruse= q(2,4), docu= q(2,4),
  acap= q(2,3), pcon= q(2,3), apex= q(2,3), ltex= q(2,4),
  tool= q(2,3), sced= q(1,3), cplx= q(5,6), 
  data= q(3),   pvol= q(2),   rely= q(5),   pcap= q(3), 
  plex= q(3),   site= q(3),   time= q(3)s),   

PROJs.OSP2= obj(
  ksloc= q(75,125),
  prec= q(3,5), pmat= q(4,5), docu= q(3,4), ltex= q(2,5), sced= q(2,4), 
  flex= q(3),   resl= q(4),   team= q(3),   time= q(3),   stor= q(3), 
  data= q(4),   pvol= q(3),   ruse= q(4),   rely= q(5),   acap= q(4), 
  pcap= q(3),   pcon= q(2),   apex= q(4),   plex= q(4),   tool= q(5),   
  cplx= q(4),   site= q(6))

PROJs.JPLflight= obj(
  ksloc= q(7,418),
  rely= q(3,5), data= q(2,3), cplx= q(3,6), time= q(3,4),
  stor= q(3,4), acap= q(3,5), apex= q(2,5), pcap= q(3,5),
  plex= q(1,4), ltex= q(1,4), pmat= q(2,3), tool= q(2),   
  sced= q(3),   prec= q(3),   flex= q(3),   resl= q(3), team= q(3), 
  ruse= q(3),   docu= q(3),   pcon= q(3),   site= q(3), pvol= q(3))

PROJs.JPLground= obj(
  ksloc= q(11, 392),
  rely= q(1,4), data= q(2,3), cplx= q(1,4), time= q(3,4),
  stor= q(3,4), acap= q(3,5), apex= q(2,5), pcap= q(3,5),
  plex= q(1,4), ltex= q(1,4), pmat= q(1,3), tool= q(2),  sced= q(3),   
  prec= q(3),   flex= q(3),   resl= q(3),   team= q(3),  ruse= q(3),   
  docu= q(3),   pcon= q(3),   site= q(3),   pvol= q(3))

RXs= obj(
    pers=  obj(acap= q(5), pcap= q(5), pcon= q(5), 
               apex= q(5), plex= q(5), ltex= q(5)),
    tools= obj(time= q(3), stor= q(3), pvol= q(2), tool= q(5), site= q(6)),
    prec=  obj(prec= q(5), flex= q(5)),
    arch=  obj(resl= q(5)),
    sced=  obj(sced= q(5)),
    proc=  obj(pmat= q(5)),
    func=  obj(data= q(2), locf=q(0.5)),
    team=  obj(team= q(5)),
    qual=  obj(rely= q(1), docu= q(1), time= q(3), cplx= q(1)))

def rules():
  _ = 0; return obj(
           ne=   [[_,_,_,1,2,_], 
                  [_,_,_,_,1,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_]],
           ne46= [[_,_,_,1,2,4], 
                  [_,_,_,_,1,2], 
                  [_,_,_,_,_,1], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_]],
           nw=   [[2,1,_,_,_,_], 
                  [1,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_]],
           nw4=  [[4,2,1,_,_,_], 
                  [2,1,_,_,_,_], 
                  [1,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_]],
           sw=   [[_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [1,_,_,_,_,_], 
                  [2,1,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_]],
           sw4=  [[_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [1,_,_,_,_,_], 
                  [2,1,_,_,_,_], 
                  [4,2,1,_,_,_],
                  [_,_,_,_,_,_]],
           sw26= [[_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [1,_,_,_,_,_],
                  [2,1,_,_,_,_], 
                  [_,_,_,_,_,_]], 
           sw46= [[_,_,_,_,_,_], 
                  [_,_,_,_,_,_], 
                  [1,_,_,_,_,_], 
                  [2,1,_,_,_,_], 
                  [4,2,1,_,_,_], 
                  [_,_,_,_,_,_]]) 

def _risks():
  out, shapes = {},rules()
  tmp = obj(
    sw46=  [("cplx", "acap"), ("cplx", "pcap"), ("cplx", "tool"), 
            ("pmat", "pcap"), ("ruse", "aexp"), ("ruse", "ltex"),
            ("stor", "acap"), ("stor", "pcap"), 
            ("time", "acap"), ("time", "pcap")],
    nw=    [("pmat", "acap"), ("sced", "ltex"), 
            ("sced", "pmat"), ("sced", "tool"),
            ("team", "aexp"), ("team", "sced"), ("team", "site"),
            ("tool", "acap"), ("tool", "pcap"), ("tool", "pmat")],
    nw4=   [("ltex", "pcap"), ("sced", "pcap"), ("sced", "aexp"), 
            ("sced", "acap"), ("sced", "plex")],
    sw4=   [("rely", "acap"), ("rely", "pcap"), ("rely", "pmat")],
    ne46=  [("sced", "cplx"), ("sced", "time")],
    ne=    [("sced", "rely"), ("sced", "pvol")],
    sw=    [("pvol", "plex")],
    sw26=  [("time", "tool")] )
  for k, pairs in tmp.items():
    for i, j in pairs:
      out[(i,j)] = shapes[k]
  return out

def complete(d, default=defaults()):
  for qs in d.values():
    for k,q1 in qs: assert k in default
    for k,q0 in default.items():
      qs[k] = with(default[k], qs.get(k))
  return d

complete(PROJs)
complete(RXs)

def f(project, risks=_risks()):
  u = random.uniform
  x = obj( **{k:random.randint(q.lo, q.hi) for k,q in project.items()})
  sf, em = 0.0, 1.0
  for k,q in project.items():
    if   q.ako == '*': sf += (     x[k] - 6) * u(-1.58, -1.014)
    elif q.ako == '+': em *= (1 + (x[k] - 3) * u(0.073, 0.21))
    elif q.ako == '-': em *= (1 + (x[k] - 3) * u(-0.187, -0.078))
  a = u(2.2, 9.18)
  b = (1.09 +  (0.88-1.09)/(9.18-2.2) * (a - 2.2)) + u(-0.1, 0.1)
  effort = a * em * (x.kloc * x.locf)**(b + 0.01*sf)
  risks = sum(risks[(x[k1],x[k2])] for k1,k2 in risks)
