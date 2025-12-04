#!/usr/bin/env lua
-- vim: set ts=2 sw=2 et:
local abs,min,max,floor = math.abs,math.min,math.max,math.floor
local pi,cos,log,rand = math.pi,math.cos,math.log,math.random
local fmt = string.format

-- ----------------------------------------------------------------------------
-- TRI(lo=0, mid=0.5, hi=1) --> TRI
local function TRI(lo,mid,hi)
  return {it=TRI,n=0, lo=lo or 0, mid=mid or 0.5, hi=hi or 1} end

-- NUM(mu=0, sd=0) --> NUM
local function NUM(mu,sd) 
  return {it=NUM, n=0, mu=mu or 0, m2=0, sd=sd or 0} end

-- SYM(has={}) -- SYM 
local function SYM(has,    n)
  n=0; for _,n1 in pairs(has or {}) do n = n + n1 end
  return {it=SYM, n=n, has=has or {} } end

-- COL = NUM | SYM | TRI
-- DATA(t : list[ COL ]) --> DATA
local function DATA(t) 
  return {it=DATA, cols=t; n=0} end

-- DATA(data: DATA) --> DATA
local function clone(data,    t)
  t={}; for j,col in pairs(data.cols) do t[j]=col.it() end; return DATA(t) end

-- ----------------------------------------------------------------------------
-- val = number | string | "?" 
-- add(i:COL, v: val | list[val]) --> v
local function add(i, v)
  if v == "?" then return v end
  i.n = i.n + 1
  if i.it == NUM then
    local d = v - i.mu
    i.mu = i.mu + d / i.n
    i.m2 = i.m2 + d * (v - i.mu)
    i.sd = (i.n < 2 or i.m2 < 0) and 0 or (i.m2 / (i.n - 1))^0.5

  elseif i.it == SYM then
    i.has[v] = (i.has[v] or 0) + 1 

  elseif i.it == DATA then
    for j,col in pairs(i.cols) do add(col,v[j]) end end
  return v end

-- sample(i:COL) --> val | list[val]
local function sample(i)
  if i.it==TRI then
    local u, v, p = rand(), rand(), (i.mid - i.lo) / (i.hi - i.lo)
    return i.lo + (i.hi - i.lo) * (min(u, v) + p * abs(u - v))

  elseif i.it==NUM then
    return i.sd==0 and i.mu or i.mu+i.sd*(-2*log(rand()))^0.5 * cos(2*pi*rand())

  elseif i.it==SYM then
    local most,mode,r = -1, nil, rand() * i.n
    for x, count in pairs(i.has) do
      r = r - count
      if r <= 0 then return x end 
      if count > most then mode,most = x,count end end
    return mode 

  else 
    local u={}; for k,v in pairs(i.cols) do u[k]=sample(v)end; return u end end 

-- ----------------------------------------------------------------------------
local function cat(t) print("{".. table.concat(t,", ") .."}") end

local function tens(t,  n,      f) 
  n,f = #t//20,floor
  return {f(t[n]), f(t[5*n]), f(t[10*n]), f(t[15*n]), f(t[19*n])} end

local function samples(i,  n,   u)
  u={}; for j=1,(n or 10^4) do u[j] = sample(i) end; table.sort(u); return u end

-- ----------------------------------------------------------------------------
local eg = {}
eg["--tri"]  = function(_) cat(tens(samples(TRI(10,20,60)))) end
eg["--num"]  = function(_) cat(tens(samples(NUM(30,5)))) end
eg["--sym"]  = function(_) cat(samples(SYM({cat=4,dog=2,mouse=1}),10)) end
eg["--data"] = function(s)
  math.randomseed(tonumber(s or 42))
  model = DATA({NUM(6,2), TRI(2,4,8), NUM(0,1), NUM(1,100), SYM{dog=2,cat=1}})
  for i=1,10 do cat(sample(model)) end end

if arg[0]:find"data.lua" then
  for i,s in pairs(arg) do if eg[s] then eg[s](arg[i+1]) end end end

return {NUM=NUM, SYM=SYM, TRI=TRI, DATA=DATA, 
        clone=clone, add=add, sample=sample}
