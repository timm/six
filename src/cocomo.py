#!/usr/bin/env python3 -B
import random, math, statistics
import binr 

# -----------------------------------------------------------------------------
# 1. KNOWLEDGE (Physics)
# -----------------------------------------------------------------------------
def definitions():
  "Variables and their optimization goals (+/-)."
  return [
    # Inputs 
    ("Prec", 1, 6), ("Flex", 1, 6), ("Arch", 1, 6), ("Team", 1, 6), ("Pmat", 1, 6),
    ("Acap", 1, 6), ("Aexp", 1, 6), ("Ltex", 1, 6), ("Pcap", 1, 6), ("Pcon", 1, 6),
    ("Plex", 1, 6), ("Sced", 1, 6), ("Site", 1, 6), ("Tool", 1, 6), ("Cplx", 1, 6),
    ("Data", 2, 5), ("Docu", 1, 6), ("Pvol", 2, 5), ("Rely", 1, 6), ("Ruse", 2, 6),
    ("Stor", 3, 6), ("Time", 3, 6), 
    ("LOC+", 2, 2000) # We want more features!
  ]

def risks():
  "Risk interactions. _=Low(0), 1=Med, 2=High, 4=Very High."
  _ = 0
  M = { 
    "ne":   [[_,_,_,1,2,_], [_,_,_,_,1,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_]],
    "ne46": [[_,_,_,1,2,4], [_,_,_,_,1,2], [_,_,_,_,_,1], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_]],
    "nw":   [[2,1,_,_,_,_], [1,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_]],
    "nw4":  [[4,2,1,_,_,_], [2,1,_,_,_,_], [1,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_]],
    "sw":   [[_,_,_,_,_,_], [_,_,_,_,_,_], [1,_,_,_,_,_], [2,1,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_]],
    "sw4":  [[_,_,_,_,_,_], [_,_,_,_,_,_], [1,_,_,_,_,_], [2,1,_,_,_,_], [4,2,1,_,_,_], [_,_,_,_,_,_]],
    "sw26": [[_,_,_,_,_,_], [_,_,_,_,_,_], [_,_,_,_,_,_], [1,_,_,_,_,_], [2,1,_,_,_,_], [_,_,_,_,_,_]], 
    "sw46": [[_,_,_,_,_,_], [_,_,_,_,_,_], [1,_,_,_,_,_], [2,1,_,_,_,_], [4,2,1,_,_,_], [_,_,_,_,_,_]] 
  }
  return {
    "Cplx": {"Acap": M["sw46"], "Pcap": M["sw46"], "Tool": M["sw46"]},
    "Ltex": {"Pcap": M["nw4"]},
    "Pmat": {"Acap": M["nw"],   "Pcap": M["sw46"]},
    "Pvol": {"Plex": M["sw"]},
    "Rely": {"Acap": M["sw4"],  "Pcap": M["sw4"],  "Pmat": M["sw4"]},
    "Ruse": {"Aexp": M["sw46"], "Ltex": M["sw46"]},
    "Sced": {"Cplx": M["ne46"], "Time": M["ne46"], "Pcap": M["nw4"], 
             "Aexp": M["nw4"],  "Acap": M["nw4"],  "Plex": M["nw4"], 
             "Ltex": M["nw"],   "Pmat": M["nw"],   "Rely": M["ne"], 
             "Pvol": M["ne"],   "Tool": M["nw"]},
    "Stor": {"Acap": M["sw46"], "Pcap": M["sw46"]},
    "Team": {"Aexp": M["nw"],   "Sced": M["nw"],   "Site": M["nw"]},
    "Time": {"Acap": M["sw46"], "Pcap": M["sw46"], "Tool": M["sw26"]},
    "Tool": {"Acap": M["nw"],   "Pcap": M["nw"],   "Pmat": M["nw"]}
  }

# -----------------------------------------------------------------------------
# 2. EVALUATION (The "Oracle")
# -----------------------------------------------------------------------------
def assess(row, defs=None, risk_table=None):
  "Enforce Integer constraints, Calculate Effort, Risk, Change."
  defs, risk_table = defs or definitions(), risk_table or risks()
  
  # 1. Repair: Inputs must be Integers (clamped to bounds)
  clean = []
  for val, (_, lo, hi) in zip(row, defs):
    clean.append(int(max(lo, min(hi, val + 0.5))))
  
  # 2. Map to names
  vals = {name: v for (name,_,_), v in zip(defs, clean)}
  
  # 3. Calculate Effort
  sf = 0.0 + sum([-1.58 * (vals[k]-6) for k in ["Prec","Flex","Arch","Team","Pmat"]])
  em = 1.0 
  for k in vals: 
    if k not in ["LOC+", "Prec","Flex","Arch","Team","Pmat"]:
      mult = -0.1 if k[0] in ['A','P'] else 0.1
      # Multiply by (1 + impact) to adjust from base effort
      em *= (1 + (vals[k]-3) * mult)
  a, b = 2.94, 0.91 
  effort = a * (vals["LOC+"] ** (b + 0.01 * sf)) * em

  # 4. Calculate Risk
  risk = 0
  for dr, interacts in risk_table.items():
    for inter, mat in interacts.items():
        idx1, idx2 = vals[dr]-1, vals[inter]-1
        if 0 <= idx1 < len(mat) and 0 <= idx2 < len(mat[0]):
            risk += mat[idx1][idx2]

  # 5. Calculate Change (Dist from "Average" start point of 3)
  dist = 0
  for val, (_, lo, hi) in zip(clean, defs):
    dist += ((val - 3) ** 2) / ((hi - lo)**2)
  change = math.sqrt(dist)

  # Return: [Inputs..., Risk-, Change-, Effort-]
  return clean + [risk, change, effort]

# -----------------------------------------------------------------------------
# 3. INTERFACE
# -----------------------------------------------------------------------------
def DATA(n=100):
  "Generate N random rows."
  defs = definitions()
  # Headers tell binr what to optimize: Risk-, Change-, Effort-
  header = [n for n,_,_ in defs] + ["Risk-", "Change-", "Effort-"]
  
  rows = []
  for _ in range(n):
    guess = [random.uniform(lo, hi) for _, lo, hi in defs]
    rows.append(assess(guess, defs))
    
  return [header] + rows

def stats(data, cols=None):
  "Report mu/sd for specific columns (Calculating from rows to avoid 'has' error)."
  if not cols:
    cols = ["LOC+", "Risk-", "Change-", "Effort-"]
  
  print(f"{'Metric':<10} {'Mean':>10} {'StdDev':>10}")
  print("-" * 32)
  
  # Find column objects by name (FIXED: c.of instead of c.txt)
  target_map = {c.of: c for c in data.cols.all}
  
  for name in cols:
    if name in target_map:
      col = target_map[name]
      # Robust calculation from rows
      vals = [r[col.at] for r in data.rows]
      if not vals: continue
      mu = statistics.mean(vals)
      sd = statistics.stdev(vals) if len(vals) > 1 else 0
      print(f"{name:<10} {mu:10.2f} {sd:10.2f}")

# -----------------------------------------------------------------------------
# 4. OPTIMIZER (Simple Hillclimber)
# -----------------------------------------------------------------------------
def go__climb(m=100, r=20):
  print(f"\n----- HILLCLIMBING (Pop={m}, Gens={r}) -----")
  defs = definitions()
  
  # 1. Initialize
  raw_data = DATA(m)
  data = binr.Data(raw_data)
  
  print("\n>>> INITIAL POPULATION")
  stats(data)

  # 2. Optimize
  for gen in range(r):
    # Sort by distance to heaven
    data.rows.sort(key=lambda r: binr.disty(data, r))
    
    # Keep elites
    best = data.rows[:30]
    
    # Generate new candidates via mixing elites
    guesses = binr.mixtures(binr.clone(data, best), m)
    
    # Assess candidates (repair bounds, apply physics)
    new_rows = [assess(row[:len(defs)], defs) for row in guesses]
    
    # Replace population
    data = binr.Data([raw_data[0]] + new_rows)

  # 3. Final Report
  print("\n>>> FINAL RECOMMENDATION")
  stats(data)

if __name__ == "__main__":
  go__climb()
