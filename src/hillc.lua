-- farthest(k, r1, rows) --> row ;; Find row faraway from `r1` in a random sample.
local function faraway(data, rows,    most,r1,r2,d,A,B)
  most = -1
  for _ = 1, 20 do 
    r1,r2 = rows[rand(#rows)//1], rows[rand(#rows)//1]
    d = distx(data, r1, r2)
    if d > most then most, A,B =  d,r1,r2 end end
  return A,B,most end 

local function _climb1(data,stop,rows,     A,B,c,t)
  if #rows < stop  then return rows end 
  A,B,c = faraway(data, rows)
  if disty(data, A) < disty(data, B) then A,B = B,A end
  t = {}
  for _, row in pairs(rows) do 
    if distx(data, row, B) < c/2 then t[#t+1]=row end end
  return _climb(data,stop, t) end

-- climb(data, rows) --> row ;; Recursively zoom into the best region.
local function climb(data,stop,rows)
  return _climb(data,stop or 10, rows or data.rows) end

local function any(a) return rand(#a)//1 end

local function _mutate(out,keep,x,y,z)
  for k=1,#x do 
    out[k] = x[k]
    if k ~= keep and rand() < the.cf then 
      local ok, tmp = pcall(function() return x[k] * the.f*(y[k] - z[k]) end)
      out[k] = ok and tmp or (rand() < 0.5 and y[k] or z[k]) end end
  return out end

local function mutates(a,n,    out)
  out = {}; 
  for k=1,n do out[k] = _mutate({}, any(a), a[any(a)], a[any(a)], a[any(a)]) end 
  return out end
