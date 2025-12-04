local rand, floor, sqrt = math.random, math.floor, math.sqrt
local the = {cr=0.8, f=0.5, np=20}

-- 1. MODEL & HELPERS
local function any(a) return rand(#a) end

local function series(b, x,    s)
  s=b[1]; for i=1,#x do s=s+b[i+1]*(x[i]^i) end; return s end

local function get_err(b, data,    sse, p, r)
  sse=0; for i=1,#data do r=data[i]
    p = series(b, r.x); sse=sse+(p-r.y)^2 end; return sse end

-- FIXED DISTANCE FUNCTION
local function dist(r1, r2,    d, n1, n2) 
  d=0
  for i=1,#r1.b do 
    n1, n2 = r1.b[i], r2.b[i]
    if type(n1)=="number" and type(n2)=="number" then
      d = d + (n1 - n2)^2
    else
      -- If symbols: Distance is 0 if equal, 1 if different
      d = d + (n1 == n2 and 0 or 1)
    end
  end 
  return sqrt(d) 
end

-- 2. MUTATION (Protected)
local function _mutate(out,keep,x,y,z,    k,ok,tmp)
  for k=1,#x do
    out[k] = x[k] 
    if k ~= keep and rand() < the.cr then
       -- Try Math. If fails (strings), fallback to crossover logic
       ok, tmp = pcall(function() return x[k] + the.f*(y[k] - z[k]) end)
       out[k] = ok and tmp or (rand()<0.5 and y[k] or z[k]) end end
  return out end

local function mutates(pop, n, data,    out, k, new_b)
  out = {}
  for k=1,n do 
    new_b = _mutate({}, rand(#pop[1].b), 
                    pop[any(pop)].b, pop[any(pop)].b, pop[any(pop)].b)
    -- Error calc also needs protection in case "SYM" gets passed to series()
    local ok, err = pcall(function() return get_err(new_b, data) end)
    out[k] = {b=new_b, err=(ok and err or 999999)} 
  end
  return out end

-- 3. CLIMB (Selector)
local function faraway(pop,    best, rest, max_d, d, c1, c2)
  max_d = -1
  for _=1,20 do
    c1, c2 = pop[any(pop)], pop[any(pop)]
    d = dist(c1, c2)
    if d > max_d then max_d, best, rest = d, c1, c2 end end
  return best, rest, max_d end

local function climb(pop, np,    best, rest, c, keep)
  if #pop <= np then return pop end
  best, rest, c = faraway(pop)
  if best.err > rest.err then best, rest = rest, best end
  keep = {}; for _,r in pairs(pop) do 
    if dist(r, best) < c then keep[#keep+1]=r end end
  return climb(keep, np) end

-- 4. MAIN
local D, N_DATA, GEN = 3, 20, 50
local true_b, training, pop = {}, {}, {}
math.randomseed(1234)

-- Setup True B (Numbers) & Data
for i=1,D+1 do true_b[i]=rand(1,8) end
for i=1,N_DATA do 
  local x={}; for j=1,D do x[j]=rand() end
  training[i] = {x=x, y=series(true_b, x)} end

-- Init Pop (With "SYM" to test robustness)
for i=1, 100 do 
  local b={}
  for j=1,D+1 do 
    if rand() < 0.1 then b[j] = "SYM" else b[j] = rand()*10 end 
  end
  pop[i] = {b=b, err=0}
  local ok, e = pcall(function() return get_err(b, training) end)
  pop[i].err = ok and e or 999999
end

print("Generations:")
for g=1,GEN do
  local survivors = climb(pop, the.np)
  pop = mutates(survivors, 100, training)
  for _,s in pairs(survivors) do pop[#pop+1]=s end -- Elitism
  
  table.sort(pop, function(a,b) return a.err < b.err end)
  if g%10==0 then print(string.format("Gen %d Best Err: %.5f", g, pop[1].err)) end
end

print("\nFinal Coeffs (Best):")
for k,v in ipairs(pop[1].b) do print(k-1, v) end
