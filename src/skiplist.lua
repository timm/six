local os = require("os")

-- =============================================================================
-- 1. TRIE (Optimized)
-- =============================================================================
local ids, n_id = {}, 1
local K, SCALE = 0.618033988749895, 4294967296
local function TREE() return { branch = true } end
local root = TREE()
local function trie_reset() root = TREE() end

local function get_hash(k,    id)
  id = ids[k]; if not id then id=n_id; ids[k]=id; n_id=n_id+1 end
  return math.floor( ((id * K) % 1) * SCALE ) end

local function tree_get(key,    h, curr, depth, kid)
  h, curr, depth = get_hash(key), root, 31
  while curr do
    kid = curr[(h >> depth) & 1]
    if not kid then return end
    if kid.branch then curr, depth = kid, depth - 1
    else return kid.key == key and kid.val or nil end end end

local function tree_put(key, val,
                        h,curr,depth,side,kid,old,nb,sn,so,b)
  h, curr, depth = get_hash(key), root, 31
  while true do
    side = (h >> depth) & 1
    kid = curr[side]
    if not kid then curr[side] = {key=key, val=val, h=h}; return end
    if kid.branch then curr, depth = kid, depth - 1
    else -- Fork collision
      if kid.key == key then kid.val = val; return end
      old, nb = kid, TREE()
      curr[side], curr, depth = nb, nb, depth - 1
      while true do
        sn, so = (h >> depth) & 1, (old.h >> depth) & 1
        if sn ~= so then
          curr[sn] = {key=key, val=val, h=h}; curr[so] = old; return end
        b = TREE(); curr[sn] = b; curr, depth = b, depth - 1 end end end end

-- =============================================================================
-- 2. SKIP LIST (Optimized)
-- =============================================================================
local max_level, p = 16, 0.5
local function NODE(lvl, k, v) return {key=k, val=v, fwd={}} end
local head = NODE(max_level)
local function sl_reset() head = NODE(max_level) end

local function random_level(    lvl)
  lvl = 1
  while math.random() < p and lvl < max_level do lvl = lvl + 1 end
  return lvl end

local function sl_get(key,      curr, i, next_node)
  curr = head
  for i = max_level, 1, -1 do
    while true do
      next_node = curr.fwd[i]
      if not next_node or next_node.key >= key then break end
      curr = next_node end end
  curr = curr.fwd[1]
  if curr and curr.key == key then return curr.val end end

local function sl_put(key, val,     curr, update, i, next_node, lvl, new_node)
  curr, update = head, {}
  for i = max_level, 1, -1 do
    while true do
      next_node = curr.fwd[i]
      if not next_node or next_node.key >= key then break end
      curr = next_node end
    update[i] = curr end
  curr = curr.fwd[1]
  if curr and curr.key == key then curr.val = val; return end

  lvl = random_level()
  new_node = NODE(lvl, key, val)
  for i = 1, lvl do
    new_node.fwd[i] = update[i].fwd[i]
    update[i].fwd[i] = new_node end end

-- =============================================================================
-- 3. SANITY CHECKS (Verify Logic)
-- =============================================================================
local function check(cond, msg) 
  if not cond then error("FAIL: " .. msg) end end

local function test_logic(name, put_fn, get_fn, reset_fn)
  reset_fn()
  print("Verifying Logic: " .. name)
  
  -- 1. Basic Insert
  put_fn("a", 10); put_fn("b", 20)
  check(get_fn("a") == 10, "Get A")
  check(get_fn("b") == 20, "Get B")
  
  -- 2. Missing Key
  check(get_fn("z") == nil, "Get Missing")
  
  -- 3. Update (Overwrite)
  put_fn("a", 999)
  check(get_fn("a") == 999, "Update A")
  
  -- 4. Collision / Order (Strings close to each other)
  put_fn("abc", 1); put_fn("abd", 2)
  check(get_fn("abc") == 1, "Collision 1")
  check(get_fn("abd") == 2, "Collision 2")
  
  print("  > logic valid.")
end

test_logic("TRIE", tree_put, tree_get, trie_reset)
test_logic("SKIPLIST", sl_put, sl_get, sl_reset)

-- =============================================================================
-- 4. THE RACE (Benchmark + Data Integrity)
-- =============================================================================
local N = 10^6 -- 100k items
local keys = {}
math.randomseed(os.time())

print("\nGenerating " .. N .. " keys...")
for i=1,N do keys[i] = "k_" .. i end

print("--- STARTING BENCHMARK (With Validation) ---")

-- TRIE RUN
trie_reset()
local t1 = os.clock()
for i=1,N do tree_put(keys[i], i) end
for i=1,N do 
  if tree_get(keys[i]) ~= i then error("Trie Data Corrupt: " .. keys[i]) end 
end
local t2 = os.clock()
print(string.format("Trie Time:      %.4fs", t2 - t1))

-- SKIP LIST RUN
sl_reset()
local t3 = os.clock()
for i=1,N do sl_put(keys[i], i) end
for i=1,N do 
  if sl_get(keys[i]) ~= i then error("SkipList Data Corrupt: " .. keys[i]) end 
end
local t4 = os.clock()
print(string.format("Skip List Time: %.4fs", t4 - t3))

-- RESULT
local speedup = (t4 - t3) / (t2 - t1)
print(string.format("Winner: Trie is %.2fx faster", speedup))
