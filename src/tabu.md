
# Tabu Search: Optimization with Memory

**Tabu Search** is a metaheuristic that guides a local heuristic search procedure to explore the solution space beyond local optimality.

**The Problem:** Standard Hill Climbing is "amnesiac"—it simply grabs the best neighbor. It gets stuck in local optima or cycles endlessly between two good points.

**The Solution:** Add **Memory**. By keeping a list of recently visited states (the "Tabu List"), we force the algorithm to explore new directions, even if they are temporarily worse.

### 1. The Function Signature

We design `tabu` as a pure functional component. It doesn't know about the physics of your problem; it only knows how to navigate it.

  * **`s`**: The current starting state (solution).
  * **`near`**: A function `f(s) -> [s1, s2...]` that generates neighbors.
  * **`cost`**: A function `f(s) -> number` (lower is better).
  * **`snap`**: A function to discretize states (essential for continuous data).
  * **`k, b`**: Budget (iterations) and Buffer size (memory depth).

<!-- end list -->

```python
def tabu(s, near, cost, snap, k=100, b=20):
  """
  Run Tabu search.
  s: start state, near: func(s)->[s], cost: func(s)->num, 
  snap: func(s)->hashable, k: max iters, b: memory buffer size
  """
  best, seen = s, []
```

### 2\. Candidate Generation & Evaluation

In every iteration (`k`), we look at the neighborhood. We sort all neighbors by their cost (energy) immediately. This is a **Greedy** approach—we want the best move possible.

```python
  for _ in range(k):
    # Generate neighbors and sort them by cost (lowest first)
    cands = sorted(near(s), key=cost)
```

### 3\. The Tabu Filter

This is the core heuristic. We iterate through our sorted candidates and pick the first one that is **not** in our short-term memory (`seen`).

  * **Heuristic:** If we have been here recently, don't go back.
  * **The `snap` Strategy:** In continuous spaces (floats), `10.00001` \!= `10.00002`. Without snapping (rounding), the tabu list never finds a match. We compare the *snapped* versions to force the algorithm to recognize "similar" areas.

<!-- end list -->

```python
    # Select best neighbor whose 'snapped' version is not in history
    try:    
      s = next(n for n in cands if snap(n) not in seen)
    except StopIteration: 
      break # No valid moves left (all neighbors are Tabu)
```

### 4\. Updating Best & Memory

Once we move to `s`:

1.  Check if it's the global best (Aspiration).
2.  Add it to the `seen` list.
3.  Truncate `seen` to size `b`. This sliding window allows old "forbidden" moves to eventually become valid again, preventing the search from running out of options permanently.

<!-- end list -->

```python
    # Update Best Solution found so far
    if cost(s) < cost(best): 
      best = s
      
    # Update Memory (FIFO queue)
    # We store the 'snapped' ID, not the raw state
    seen = ([snap(s)] + seen)[:b]
    
  return best
```

-----

### 5\. Putting it Together: A Concrete Example

Here is how you use the engine to solve a continuous optimization problem (finding the bottom of a parabola).

**The Setup:**
We define our domain physics (`cost`, `neighbors`) and our resolution strategy (`snap`).

```python
import random

# 1. The Cost Function (Target: minimize x^2)
cost = lambda x: x**2

# 2. The Neighbors (Explore -0.5 to +0.5 around current x)
#    Note: These are raw floats.
near = lambda x: [x + random.uniform(-0.5, 0.5) for _ in range(10)]

# 3. The Snap Strategy (Crucial for Continuous Data)
#    We treat everything within 0.1 as the "same" location.
snap = lambda x: round(x, 1) 

# 4. Run it
#    Start at x=10.5. It should find its way to ~0.
final_pos = tabu(10.5, near, cost, snap, k=100, b=5)

print(f"Started at 10.5, ended at {final_pos:.5f} (Cost: {cost(final_pos):.5f})")
```

### Summary of Heuristics Used

1.  **Discretization (`snap`):** Continuous optimization requires overlaying a grid on the search space to make "memory" effective.
2.  **Short-Term Memory (`seen`):** Prevents immediate cycling and forces exploration of the neighborhood.
3.  **Greedy Local Search:** Always prefer the best non-tabu neighbor to exploit gradients.
4.  **Separation of Concerns:** The `tabu` function contains no domain logic; it relies on injected functions (`near`, `cost`) for details.
