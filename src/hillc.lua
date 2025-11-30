-- farthest(i, r1, rows) --> row ;; Find row faraway from `r1` in a random sample.
local function faraway(data, rows,    most,r1,r2,d,A,B)
  most = -1
  for _ = 1, 20 do 
    r1,r2 = rows[rand(#rows)//1], rows[rand(#rows)//1]
    d = distx(data, r1, r2)
    if d > most then most, A,B =  d,r1,r2 end end
  return A,B,most end 

local function _climb1(data,stop,rows,     A,B,c,t)
  if #rows < stop  then return rows[1] end 
  A,B,c = faraway(data, rows)
  if disty(data, A) < disty(data, B) then A,B = B,A end
  t = {}; for _, row in pairs(rows) do 
            if distx(data, row, B) < c/2 then t[#t+1]=row end end
  return _climb(data,stop, t) end

-- climb(data, rows) --> row ;; Recursively zoom into the best region.
local function climb(data,stop,rows)
  return _climb(data,stop or 4. rows or data.rows)

--  just add a mutator in the region generated


