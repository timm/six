local rand, sqrt, min = math.random, math.sqrt, math.min
local CR, F = 0.8, 0.5 
local D, N, G, NP = 3, 10000, 5, 60 -- G=Generations, NP=Survivors

-- 1. MODEL & HELPERS
local function series(b, x,    s)
  s=b[1]; for i=1,#x do s=s+b[i+1]*(x[i]^i) end; return s end

local function distx(r1, r2,    d)
  d=0; for i=1,#r1.x do d=d+(r1.x[i]-r2.x[i])^2 end; return sqrt(d) end

local function disty(r) return -r.y end -- Minimize negative Y (Find Peaks)

-- 2. CLUSTER / FILTER (Hill Climbing)
local function faraway(rows,    best, rest, max_d, d, r1, r2)
  max_d = -1
  for _=1,20 do
    r1, r2 = rows[rand(#rows)], rows[rand(#rows)]
    d = distx(r1, r2)
    if d > max_d then max_d, best, rest = d, r1, r2 end end
  return best, rest, max_d end

local function climb(rows, np,    best, rest, c, keep, r)
  if #rows <= np then return rows end
  best, rest, c = faraway(rows)
  if disty(best) > disty(rest) then best, rest = rest, best end
  keep = {}; for _,r in pairs(rows) do 
    if distx(r, best) < c then keep[#keep+1]=r end end
  return climb(keep, np) end

-- 3. EXPAND (Mutation / DE)
local function mutate(pop, dim, b,    a, x, y, z, new_x, j)
  x, y, z = pop[rand(#pop)], pop[rand(#pop)], pop[rand(#pop)]
  new_x = {}
  for j=1,dim do
    if rand() < CR then
      new_x[j] = x.x[j] + F * (y.x[j] - z.x[j]) -- DE/rand/1
      -- Clamp to 0..2 to prevent explosion in power series
      if new_x[j] < 0 then new_x[j]=0 end; if new_x[j] > 2 then new_x[j]=2 end
    else new_x[j] = x.x[j] end end
  return {x=new_x, y=series(b, new_x)} end

local function evolve(survivors, N, dim, b,    pop, k)
  pop = {}; k=1
  -- Elitism: Keep survivors
  for _,r in pairs(survivors) do pop[k]=r; k=k+1 end
  -- Fill rest with mutants
  while k <= N do pop[k]=mutate(survivors, dim, b); k=k+1 end
  return pop end

-- 4. LEARN (SGD)
local function learn(rows, dim, lr, epochs,    b, r, err, j, grad)
  b={}; for i=1,dim+1 do b[i]=rand() end
  for _=1,epochs do
    r = rows[rand(#rows)]
    err = series(b, r.x) - r.y
    b[1] = b[1] - lr * err
    for j=1,dim do 
       grad = r.x[j]^j; if grad > 1e4 then grad=1e4 end
       b[j+1] = b[j+1] - lr * err * grad end end
  return b end

-- MAIN
local true_b, pop = {}, {}
math.randomseed(12345)

-- Setup True B and Initial Random Pop
print("True B: "); for i=1,D+1 do true_b[i]=rand(1,5); io.write(true_b[i].." ") end
print("\n\nGenerations ("..G.."):")

for i=1,N do 
  local x={}; for j=1,D do x[j]=rand()*2 end
  pop[i] = {x=x, y=series(true_b, x)} end

-- Run Generations
for g=1,G do
  local best = climb(pop, NP)
  -- Print stats of best survivor in this generation
  pop = evolve(best, N, D, true_b) 
  print(string.format("Gen %d | Best Y: %.4f | Survivors: %d | %d", g, best[1].y, #best,#pop))
end

-- Learn from final survivors
local est_b = learn(climb(pop, NP), D, 0.0001, 10000)

print("\nComparison:")
print(string.format("%-10s %-10s %-10s", "Coeff", "True", "Est"))
for i=1,D+1 do 
  print(string.format("b[%d]       %-10.4f %-10.4f", i-1, true_b[i], est_b[i])) end
