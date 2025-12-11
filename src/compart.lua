#!/usr/bin/env python3 -B
import random, math, statistics
import binr 

# -----------------------------------------------------------------------------
# 1. DATA: Projects & Policies
# -----------------------------------------------------------------------------

# Mappings from Image names to Internal names
MAP = {
    "resl": "Arch", "apex": "Aexp", "ksloc": "LOC+", 
    "prec": "Prec", "flex": "Flex", "team": "Team", "pmat": "Pmat", 
    "stor": "Stor", "ruse": "Ruse", "docu": "Docu", "acap": "Acap",
    "pcon": "Pcon", "ltex": "Ltex", "tool": "Tool", "sced": "Sced",
    "cplx": "Cplx", "data": "Data", "pvol": "Pvol", "rely": "Rely",
    "pcap": "Pcap", "plex": "Plex", "site": "Site", "time": "Time"
}

# 4 Projects from Figure 4
PROJECTS = {
    "OSP": {
        "ranges": {
            "prec": (1,2), "flex": (2,5), "resl": (1,3), "team": (2,3), 
            "pmat": (1,4), "stor": (3,5), "ruse": (2,4), "docu": (2,4),
            "acap": (2,3), "pcon": (2,3), "apex": (2,3), "ltex": (2,4),
            "tool": (2,3), "sced": (1,3), "cplx": (5,6), "ksloc": (75,125)
        },
        "fixed": {
            "data": 3, "pvol": 2, "rely": 5, "pcap": 3, "plex": 3, "site": 3,
            "time": 3 
        }
    },
    "OSP2": {
        "ranges": {
            "prec": (3,5), "pmat": (4,5), "docu": (3,4), "ltex": (2,5),
            "sced": (2,4), "ksloc": (75,125)
        },
        "fixed": {
            "flex": 3, "resl": 4, "team": 3, "time": 3, "stor": 3, "data": 4,
            "pvol": 3, "ruse": 4, "rely": 5, "acap": 4, "pcap": 3, "pcon": 3,
            "apex": 4, "plex": 4, "tool": 5, "cplx": 4, "site": 6
        }
    },
    "JPL_Flight": {
        "ranges": {
            "rely": (3,5), "data": (2,3), "cplx": (3,6), "time": (3,4),
            "stor": (3,4), "acap": (3,5), "apex": (2,5), "pcap": (3,5),
            "plex": (1,4), "ltex": (1,4), "pmat": (2,3), "ksloc": (7, 418)
        },
        "fixed": {
            "tool": 2, "sced": 3, "prec": 3, "flex": 3, "resl": 3, "team": 3, 
            "ruse": 3, "docu": 3, "pcon": 3, "site": 3, "pvol": 3
        }
    },
    "JPL_Ground": {
        "ranges": {
            "rely": (1,4), "data": (2,3), "cplx": (1,4), "time": (3,4),
            "stor": (3,4), "acap": (3,5), "apex": (2,5), "pcap": (3,5),
            "plex": (1,4), "ltex": (1,4), "pmat": (1,3), "ksloc": (11, 392)
        },
        "fixed": {
            "tool": 2, "sced": 3, "prec": 3, "flex": 3, "resl": 3, "team": 3, 
            "ruse": 3, "docu": 3, "pcon": 3, "site": 3, "pvol": 3
        }
    }
}

# 9 Standard Policies
POLICIES = [
    ("Pers", {"acap":5, "pcap":5, "pcon":5, "apex":5, "plex":5, "ltex":5}),
    ("Tools", {"time":3, "stor":3, "pvol":2, "tool":5, "site":6}),
    ("Prec", {"prec":5, "flex":5}),
    ("Arch", {"resl":5}),
    ("Sced", {"sced":5}),
    ("Proc", {"pmat":5}),
    ("Func", {"data":2, "LOC+": 0.5}), 
    ("Team", {"team":5}),
    ("Qual", {"rely":1, "docu":1, "time":3, "cplx":1})
]

# -----------------------------------------------------------------------------
# 2. PHYSICS
# -----------------------------------------------------------------------------
def get_base_definitions():
    return [
        ("Prec", "*", 1, 6), ("Flex", "*", 1, 6), ("Arch", "*", 1, 6),
        ("Team", "*", 1, 6), ("Pmat", "*", 1, 6),
        ("Acap", "-", 1, 6), ("Aexp", "-", 1, 6), ("Ltex", "-", 1, 6),
        ("Pcap", "-", 1, 6), ("Pcon", "-", 1, 6), ("Plex", "-", 1, 6),
        ("Sced", "-", 1, 6), ("Site", "-", 1, 6), ("Tool", "-", 1, 6),
        ("Cplx", "+", 1, 6), ("Data", "+", 2, 5), ("Docu", "+", 1, 6),
        ("Pvol", "+", 2, 5), ("Rely", "+", 1, 6), ("Ruse", "+", 2, 6),
        ("Stor", "+", 3, 6), ("Time", "+", 3, 6),
        ("LOC+", "=", 2, 2000)
    ]

def make_project_definitions(proj_name):
    base = get_base_definitions()
    p_data = PROJECTS[proj_name]
    new_defs = []
    for name, role, def_lo, def_hi in base:
        key = next((k for k,v in MAP.items() if v == name), None)
        lo, hi = def_lo, def_hi
        
        # Apply Ranges
        if key in p_data["ranges"]:
            r = p_data["ranges"][key]
            lo, hi = r[0], r[1]
        # Apply Fixed Values
        if key in p_data["fixed"]:
            val = p_data["fixed"][key]
            lo, hi = val, val
            
        new_defs.append((name, role, lo, hi))
    return new_defs

def risks():
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

def assess(row, defs, risk_table=None, baseline=None, epsilon=0.5):
  risk_table = risk_table or risks()
  
  # 1. Repair: Inputs must be rounded to epsilon
  clean = []
  for val, (_, _, lo, hi) in zip(row, defs):
    val = max(lo, min(hi, val))
    val = round(val / epsilon) * epsilon
    clean.append(val)
  
  vals = {name: v for (name,_,_,_), v in zip(defs, clean)}
  
  # 3. Calculate Effort
  scale_sum, em_prod = 0.0, 1.0
  for val, (_, role, _, _) in zip(clean, defs):
    if role == '*': 
      scale_sum += (val - 6) * random.uniform(-1.58, -1.014)
    elif role == '+': 
      em_prod *= (1 + (val - 3) * random.uniform(0.073, 0.21))
    elif role == '-': 
      em_prod *= (1 + (val - 3) * random.uniform(-0.187, -0.078))

  a = random.uniform(2.3, 9.18)
  b = 0.91 + 0.01 * scale_sum
  effort = a * (vals["LOC+"] ** b) * em_prod

  # 4. Calculate Risk
  risk = 0
  for dr, interacts in risk_table.items():
    for inter, mat in interacts.items():
        idx1 = int(round(vals[dr])) - 1
        idx2 = int(round(vals[inter])) - 1
        if 0 <= idx1 < len(mat) and 0 <= idx2 < len(mat[0]):
            risk += mat[idx1][idx2]

  # 5. Calculate Change (Distance from Baseline Mean)
  dist = 0
  if baseline:
    for i, (val, (_, _, lo, hi)) in enumerate(zip(clean, defs)):
      denom = (hi - lo) if hi != lo else 1
      dist += ((val - baseline[i]) ** 2) / (denom**2)
    change = math.sqrt(dist)
  else:
    change = 0 

  return clean + [risk, change, effort]

def apply_policy(baseline_row, defs, policy_dict, risk_table, baseline_mean, epsilon):
    """
    Applies a standard policy to the Baseline Mean vector.
    """
    new_row = list(baseline_row)
    name_to_idx = {name: i for i, (name,_,_,_) in enumerate(defs)}
    
    for key, val in policy_dict.items():
        if key == "LOC+": 
             idx = name_to_idx["LOC+"]
             new_row[idx] *= val 
        else:
             target = MAP.get(key, key)
             if target in name_to_idx:
                 new_row[name_to_idx[target]] = val
                 
    return assess(new_row, defs, risk_table, baseline=baseline_mean, epsilon=epsilon)

# -----------------------------------------------------------------------------
# 3. INTERFACE
# -----------------------------------------------------------------------------
def get_stats(data):
  stats = {}
  for col in data.cols.all:
      vals = [r[col.at] for r in data.rows]
      if not vals: stats[col.of] = (0,0)
      else: stats[col.of] = (statistics.mean(vals), statistics.stdev(vals) if len(vals)>1 else 0)
  return stats

def analyze_project(proj_name, m=100, r=20, epsilon=0.5):
    print(f"\n{'='*60}")
    print(f" PROJECT: {proj_name}")
    print(f"{'='*60}")
    
    defs = make_project_definitions(proj_name)
    risk_table = risks()
    
    # 1. INITIALIZE & BASELINE
    raw_inputs = []
    for _ in range(m):
        # Use random.uniform for initial generation to allow diverse starting points
        raw_inputs.append([random.uniform(lo, hi) for _, _, lo, hi in defs])
        
    baseline_means = []
    for k in range(len(defs)):
        col_vals = [row[k] for row in raw_inputs]
        baseline_means.append(statistics.mean(col_vals))
        
    # Gen 0 Data
    rows = [assess(inp, defs, risk_table, baseline=baseline_means, epsilon=epsilon) for inp in raw_inputs]
    header = [n for n,_,_,_ in defs] + ["Risk-", "Change-", "Effort-"]
    data = binr.Data([header] + rows)
    initial_stats = get_stats(data)
    
    # 2. OPTIMIZE (Learned Policy)
    for gen in range(r):
        data.rows.sort(key=lambda r: binr.disty(data, r))
        best = data.rows[:30]
        guesses = binr.mixtures(binr.clone(data, best), m)
        new_rows = [assess(row[:len(defs)], defs, risk_table, baseline=baseline_means, epsilon=epsilon) for row in guesses]
        data = binr.Data([header] + new_rows)
        
    learned_stats = get_stats(data)
    
    # 3. EVALUATE STANDARD POLICIES
    policy_results = []
    for pname, pdict in POLICIES:
        res = apply_policy(baseline_means, defs, pdict, risk_table, baseline_means, epsilon)
        policy_results.append(res)
        
    # 4. REPORT MATRIX
    p_headers = [p[0] for p in POLICIES]
    
    print(f"{'Metric':<10} {'Base':>8} {'Lrn':>8} {'Sd':>6} " + " ".join([f"{ph:>6}" for ph in p_headers]))
    print("-" * (10 + 8 + 8 + 6 + 7*9))
    
    metrics = [d[0] for d in defs] + ["Risk-", "Change-", "Effort-"]
    
    for i, name in enumerate(metrics):
        base_val = initial_stats[name][0]
        lrn_val  = learned_stats[name][0]
        lrn_sd   = learned_stats[name][1]
        
        # Display logic: Round Inputs to Epsilon
        if i < len(defs): 
            base_disp = round(base_val/epsilon)*epsilon
            lrn_disp  = round(lrn_val/epsilon)*epsilon
        else:
            base_disp = base_val
            lrn_disp  = lrn_val
            
        if name == "Change-":
            base_disp = 0.00
            
        base_str = f"{base_disp:8.2f}"
        
        # Use = for Lrn if no change
        if abs(lrn_disp - base_disp) < 1e-9:
            lrn_str = f"{'=':>8}"
        else:
            lrn_str = f"{lrn_disp:8.2f}"
            
        row_str = f"{name:<10} {base_str} {lrn_str} {lrn_sd:6.2f} "
        
        # Policies
        for p_idx, res in enumerate(policy_results):
            val = res[i]
            val_disp = val
            if i < len(defs): val_disp = round(val/epsilon)*epsilon
            
            # Use = for Policy if no change
            if abs(val_disp - base_disp) < 1e-9:
                pol_str = f"{'=':>6}"
            else:
                pol_str = f"{val_disp:6.2f}"
                
            row_str += f"{pol_str} "
            
        print(row_str)

if __name__ == "__main__":
    for p in PROJECTS:
        analyze_project(p, m=100, r=20, epsilon=0.5)
