# Hill-climbing and Random Search — an intro for grad students


Learning goals

- Understand the difference between pure random search and a simple hill-climbing / Cross-Entropy-style loop.
- See how hill-climbing can be implemented by repeatedly sampling, selecting elites, and refitting a sampler.
- Map each step to the primitives in src/data.lua (NUM, DATA, sample, add, clone).
- Be ready to implement a minimal CEM-style sampler and the hillc.lua examples.


## 1) High-level idea (one-paragraph)

We want to find inputs x that make an objective f(x) small (or large). 

Random search draws many candidates at random and remembers the best.

 Hill-climbing here uses a short loop: 
 
 - draw many candidates from a current proposal distribution...
 - ... keep the best few (the "elite" set), and fit the next proposal to those elites.
 -  repeating this concentrates the proposal where good solutions live. 
 
 (Aside that   simple loop is the Cross-Entropy Method (CEM) / estimation-of-distribution approach .)


## 2) Minimal CEM sampler (put this at the top of any lecture)
This tiny pseudocode shows the whole algorithm in plain steps. This code only handles the very simple case of a model with one variable.

```
μ := initial mean
σ2 := initial variance
repeat until convergence or max iterations:
  X := draw N samples from Normal(μ, σ2)
  score each x in X with f(x) = objective(x)
  elites := top Ne points from X by score
  μ := mean(elites)
  σ2 := variance(elites)  (use small floor if zero)
end
return μ  -- mean of final distribution (best guess)
```

One-line intuition: "sample many → keep best → refit → repeat."


 Small annotated example: one iteration (concrete numbers)

- Start μ = -6, σ2 = 100, N = 100, Ne = 10.
- Draw 100 samples from Normal(-6, 100).
- Evaluate f(x) for each sample (higher S better).
- Sort and keep top 10 samples.
- Compute μ_elite = mean(top 10), σ2_elite = var(top 10).
- Update μ := μ_elite, σ2 := σ2_elite (or smooth).
- Repeat.


## 3) hillc.lua: objective and model (short fragments)

Objective f(x) (toy polynomial). We minimize this.

```lua
local function f(x)
  return 1.61 + 2.1*x[1] + -3.5*x[2]^3 + 4*x[3]^3 - 5*x[4]^4
end
```

MODEL describes how to draw candidates. In data.lua a DATA is a vector of columns; NUM columns define Gaussians (mu, sd).

```lua
local function MODEL()
  return d.DATA({ d.NUM(100,1), d.NUM(20,5), d.NUM(10,4), d.NUM(3,2) })
end
```

Mapping: one-dimensional CEM = one d.NUM(mu, sd).


## 4) Random search (short explanation + code snippet)

What it does: sample repeatedly from the model and keep the best sample seen.

Code fragment:

```lua
for j=1,1000 do
  xs = d.sample(model0)
  y = add(seen, f(xs))
  if y < best then best,out = y, xs end
end
```

Plain English:
- d.sample(model0) proposes a vector xs.
- add(seen, f(xs)) updates an online mean/sd for observed y-values (for diagnostics).
- Keep the single best xs found.

When to use: simple baselines, highly parallelizable, works okay for low dimension or wide priors.


## 5) Hill-climbing implemented in hillc.lua (climb)

What it does: sample a batch, keep the promising ones (via a z-score rule), add those to a fresh model, return the new model.

Code fragment:

```lua
seen, model1 = d.NUM(), d.clone(model0)
for j=1,100 do
  xs = d.sample(model0)
  y = add(seen, f(xs))
  if (y - seen.mu) / seen.sd < -1 then d.add(model1, xs) end
end
return model1, seen
```

Step-by-step (student-friendly):
- seen = d.NUM(): an online tracker for mean and sd of objective values we see this batch.
- d.clone(model0): make a fresh DATA object with the same column types but empty stats.
- Sample many xs from model0. For each:
  - compute y = f(xs) and update seen.
  - if y is at least 1 sd below the running mean (a quick elite test), add xs to model1.
- After the loop, model1 contains only the "elite" samples; its NUM columns have mu/sd computed from the elites. Use model1 as the next proposal and repeat.

How this maps to CEM:
- Sampling = draw N from Normal(μ,σ2).
- Elite selection = z-score test (approx top ~16% if y is normal).
- Refit = d.add on a fresh clone builds the new mu/sd from elites.


## 6) Simple changes to make this robust (practical tips)

- Use a minimum variance floor: sd := max(sd, eps) so sampler doesn't collapse to a point too early.
- Use smoothing: mu := α*mu_elite + (1-α)*mu_old with α ∈ (0,1] to slow changes and reduce noise.
- Prefer explicit elite selection (collect batch → sort → take top Ne) rather than an online z-score if you want reproducible selection.
- Guard against seen.sd == 0 before dividing (skip selection until seen.n ≥ 2, or use eps).


## 10) Summary

Random search is a one-shot global sampler with memory of the best sample. Hill-climbing here is a simple CEM-style loop: sample a batch, keep elites, refit the sampler, repeat — a practical middle ground between blind search and heavy-weight global optimizers.

