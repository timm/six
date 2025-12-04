--
--
-- local function _mutate(out,keep,x,y,z)
--   for k=1,#x do
--   out[k] = x[k]
--     if k ~= keep and rand() < the.cr then
--       local ok, tmp = pcall(function() return x[k] * the.f*(y[k] - z[k]) end)
--       out[k] = ok and tmp or (rand() < 0.5 and y[k] or z[k]) end end
--   return out end
--
-- local function mutates(a,n,    out)
--   out = {}
--   for k=1,n do out[k] = _mutate({}, any(a), a[any(a)], a[any(a)], a[any(a)]) end
--   return out end


