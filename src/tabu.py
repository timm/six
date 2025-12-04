def tabu(s, near, cost, snap, k=100, b=20):
  """
  snap: func(s)->s' (rounds/hashes state for equality check)
  """
  best, seen = s, []
  for _ in range(k):
    # Filter using 'snap' to check if essentially the same state
    # Note: we store 'snap(n)' in seen, not 'n'
    cands = sorted(near(s), key=cost)
    try:    s = next(n for n in cands if snap(n) not in seen)
    except: break 
    
    if cost(s) < cost(best): best = s
    seen = ([snap(s)] + seen)[:b] # Store quantized version
    print(round(best,2), end=" ")
  return best

# --- Usage Example (Continuous) ---
import random
cost = lambda x: x**2

# 1. Rounding makes infinite space finite (clumps neighbors together)
snap = lambda x: round(x, 1) 

# 2. Neighbors are random floats, but we treat close ones as identical
near = lambda x: [x + random.uniform(-0.5, 0.5) for _ in range(10)]

print(tabu(10.5, near, cost, snap))
