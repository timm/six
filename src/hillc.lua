-- cr = crossover= how often we change an parameter. 0=never, 1=always
-- f  = scaling factor = how fasr we change a pararameter. 0 = none; 1=lots; 2=massive (rare)
-- np = population size
--
-- defaults (concise)
-- the.cr = 0.9    -- crossover CR (typical 0.7-0.95). larger -> more mixing
-- the.f  = 0.8    -- scaling F (typical 0.5-0.9). larger -> bigger steps
-- NP = math.max(20, 10 * D) -- population, heuristic 5-20×D, min 20

-- local tuning after a global search 
-- cr, f = 0.3,0.5
--
-- Tuning (short)
-- Exploration: increase F (0.8-0.95) and NP (10-20×D). cost: more evals.
-- Exploitation: lower F (0.3-0.6) and CR (0.2-0.6). finer, steadier search.
-- Adaptive: adjust F and CR online (recommended if unsure).

local the={cr=0.3, f=0.5}
the.np     = function(d) return math.max(20,10*d) end
the.budget = function(d) return 1000*the.d end

local rand=math.random

-- farthest(k, r1, rows) --> row ;; Find row faraway from `r1` in a random sample.
local function faraway(data, rows,    most,r1,r2,d,A,B)
  most = -1
  for _ = 1, 20 do
    r1,r2 = rows[rand(#rows)//1], rows[rand(#rows)//1]
    d = distx(data, r1, r2)
    if d > most then most, A,B =  d,r1,r2 end end
  return A,B,most end

local function climb(data,rows,     rest,best,c,half)
  rows = rows or data.rows
  if #rows < the.np  then return rows end
  rest,best,c = faraway(data, rows)
  if disty(data, rest) < disty(data, best) then rest,best = best,rest end
  half = {}
  for _, row in pairs(rows) do
    if distx(data, row, best) < c/2 then half[#half+1]=row end end
  return climb(data,half) end

local function any(a) return rand(#a)//1 end

local function _mutate(out,keep,x,y,z)
  for k=1,#x do
  out[k] = x[k]
    if k ~= keep and rand() < the.cr then
      local ok, tmp = pcall(function() return x[k] * the.f*(y[k] - z[k]) end)
      out[k] = ok and tmp or (rand() < 0.5 and y[k] or z[k]) end end
  return out end

local function mutates(a,n,    out)
  out = {}
  for k=1,n do out[k] = _mutate({}, any(a), a[any(a)], a[any(a)], a[any(a)]) end
  return out end

--mutates(climb())
