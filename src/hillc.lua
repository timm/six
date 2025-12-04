#!/usr/bin/env lua
-- vim: set ts=2 sw=2 et:
local d = require"data"
local fmt = string.format
local floor = math.floor

local function f(x) 
  return 1.61 + 2.1*x[1] + -3.5*x[2]^3 + 4*x[3]^3 - 5*x[4]^4 end

local function MODEL() 
  return d.DATA({d.NUM(100,1), d.NUM(20,5), d.NUM(10,4), d.NUM(3,2)}) end

local function climb(model0,    seen,model1,xs,y)
  seen, model1 = d.NUM(), d.clone(model0)
  for j=1,100 do 
    xs = d.sample(model0) 
    y = add(seen, f(xs))
    if (y - seen.mu)/seen.sd < -1 then d.add(model1, xs) end end 
 return model1,seen end 

-- ----------------------------------------------------------------------------
local eg={}

eg["--climb"] = function(s,      model,seen)
  math.randomseed(s or 42)
  model = MODEL()
  for j=1,10 do  
    model,seen = climb(model)
    print(fmt("%10.0f %10.0f",floor(seen.mu), floor(seen.sd))) end end

if arg[0]:find"hillc.lua" then
  for i,s in pairs(arg) do if eg[s] then eg[s](arg[i+1]) end end end
