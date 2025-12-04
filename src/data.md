# Quick overview (expanded): data.lua — full theory mapped to code

 

1) Lua language essentials: syntax, locals vs globals, functions as
   first-class values, tables as arrays/records, pairs/ipairs
   iteration, and module return patterns.

- Explanation:
  - The file uses `local` bindings for functions/values and packs
    constructors into tables that act as typed records. Functions
    are stored in tables (e.g. `eg`) and returned from the module.

- Code (top-of-file local bindings and module return):

  ```lua
  local abs,min,max,floor = math.abs,math.min,math.max,math.floor
  local pi,cos,log,rand = math.pi,math.cos,math.log,math.random

  ...

  return {NUM=NUM, SYM=SYM, TRI=TRI, DATA=DATA,
          clone=clone, add=add, sample=sample}
  ```

- Notes:
  - `pairs` is used for generic iteration over tables; `ipairs`
    is not explicitly used but is the array-style iterator.


2) Table manipulation and copying: shallow vs deep clone semantics
   and iterative construction of table-based records.

- Explanation:
  - `clone` creates a new DATA object by iterating the `cols`
    table and calling each column constructor (`col.it()`).
  - This is a shallow "type-only" clone (it recreates column
    descriptors, not current state values).

- Code (`clone` and `DATA`):

  ```lua
  local function DATA(t) return {it=DATA, cols=t; n=0} end

  local function clone(data,    t)
    t={}; for j,col in pairs(data.cols) do t[j]=col.it() end
    return DATA(t)
  end
  ```

- Notes:
  - To deep-clone current state you would copy numeric fields
    (`n, mu, m2, sd`) and `has` tables; beware of function-valued
    tags (the `it` field) which should remain references.


3) Random number generation in Lua: math.random, seeding
   (math.randomseed), and implications for reproducibility and RNG
   quality.

- Explanation:
  - The file seeds the RNG in the `--data` demo for reproducible
    runs. `math.random` is used everywhere; its quality and period
    depend on the Lua implementation.

- Code (seeding in eg demo):

  ```lua
  eg["--data"] = function(s)
    math.randomseed(tonumber(s or 42))
    model = DATA({...})
    ...
  end
  ```

- Notes:
  - Reproducibility requires the same seed and the same Lua RNG
    implementation/version; `math.random` distribution and edge
    behavior (e.g. inclusion of 0 or 1) matter for transforms.


4) Triangular distribution: parameterization by (lo, mid, hi)
   and the sampling technique using two uniform samples to bias
   toward the mode.

- Explanation:
  - The code stores `lo, mid, hi` in a TRI object and samples by
    combining two uniforms, using `min(u,v)` and `abs(u-v)` with a
    mode ratio `p` to produce the triangular density.

- Code (TRI constructor and sampler):

  ```lua
  local function TRI(lo,mid,hi)
    return {it=TRI,n=0, lo=lo or 0, mid=mid or 0.5, hi=hi or 1} end

  if i.it==TRI then
    local u, v, p = rand(), rand(), (i.mid - i.lo) / (i.hi - i.lo)
    return i.lo + (i.hi - i.lo) * (min(u, v) + p * abs(u - v))
  end
  ```

- ASCII intuition (density bins):

  ```
  **
  *****
  ***
  **
  *
  ```

- Notes:
  - This sampling approach is efficient and avoids explicit inverse
    CDF algebra in the code.


5) Gaussian (normal) distribution generation: the Box–Muller
   transform (using log, cos, uniform RNG) to produce normally
   distributed samples.

- Explanation:
  - The code uses the standard Box–Muller trig form with two
    uniform draws: sqrt(-2 ln U1) * cos(2*pi*U2), scaled by `sd`
    and shifted by `mu`.

- Code (normal sampling for NUM):

  ```lua
  elseif i.it==NUM then
    return i.sd==0 and i.mu or i.mu+i.sd*(-2*log(rand()))^0.5 * cos(2*pi*rand())
  end
  ```

- Notes:
  - Avoid `log(0)` by ensuring RNG never returns exact 0; Lua's
    `math.random()` typically returns values in (0,1].


6) Categorical (symbolic) sampling: sampling from discrete
   distributions by cumulative counts and mode fallback.

- Explanation:
  - `SYM` stores counts in `has` and total `n`. Sampling chooses
    a random r in `[0,n)` and subtracts counts until r<=0; if
    rounding leaves none chosen, it returns the mode.

- Code (SYM constructor and sampling):

  ```lua
  local function SYM(has,    n)
    n=0; for _,n1 in pairs(has or {}) do n = n + n1 end
    return {it=SYM, n=n, has=has or {} } end

  elseif i.it==SYM then
    local most,mode,r = -1, nil, rand() * i.n
    for x, count in pairs(i.has) do
      r = r - count
      if r <= 0 then return x end 
      if count > most then mode,most = x,count end end
    return mode 
  end
  ```

- Notes:
  - Replace integer counts with float weights directly; same loop
    works as long as `i.n` holds the weight sum.


7) Online statistics (one-pass algorithms): Welford’s algorithm
   for incremental mean (mu), second moment accumulator (m2),
   variance and standard deviation updates.

- Explanation:
  - `add` updates `n`, `mu`, and `m2` in a stable one-pass way.
    Standard deviation `sd` computed from `m2/(n-1)`. This is
    Welford’s algorithm which avoids cancellation.

- Code (`add` NUM branch):

  ```lua
  function add(i, v)
    if v == "?" then return v end
    i.n = i.n + 1
    if i.it == NUM then
      local d = v - i.mu
      i.mu = i.mu + d / i.n
      i.m2 = i.m2 + d * (v - i.mu)
      i.sd = (i.n < 2 or i.m2 < 0) and 0 or (i.m2 / (i.n - 1))^0.5
    ...
    end
    return v
  end
  ```

- Notes:
  - `m2` holds the sum of squared deviations; avoid deriving
    variance via subtraction of large numbers.


8) Handling missing data: sentinel values (e.g., "?") and
   propagation/avoidance in aggregations.

- Explanation:
  - `add` immediately returns when value is `"?"`, skipping the
    update so missing data does not affect counts or summaries.

- Code (missing-value guard):

  ```lua
  function add(i, v)
    if v == "?" then return v end
    -- proceed with updates otherwise
  end
  ```

- Notes:
  - This is a simple ignore/missing policy; other policies
    (imputation) would modify `add` to substitute values.


9) Symbolic summaries: frequency tables, counting occurrences,
   computing the mode and total counts.

- Explanation:
  - `SYM` constructor computes total `n` from `has`, and `add`
    increments `has[v]`. Mode is found when sampling or by
    scanning counts.

- Code (SYM add branch and constructor):

  ```lua
  local function SYM(has,    n)
    n=0; for _,n1 in pairs(has or {}) do n = n + n1 end
    return {it=SYM, n=n, has=has or {} } end

  elseif i.it == SYM then
    i.has[v] = (i.has[v] or 0) + 1
  ```

- Notes:
  - Keep `n` in sync on incremental adds (the constructor sums
    initial counts; `add` increments counts but must also bump `n`).


10) Composite data structures and recursive operations: DATA
    objects that contain columns, and recursive add/sample
    operations over nested columns.

- Explanation:
  - `DATA` stores `cols` (a table of column descriptors).
  - `add` delegates to column `add` for each entry in a row.
  - `sample` builds a synthetic row by sampling each column.

- Code (DATA, recursive add, and recursive sample):

  ```lua
  local function DATA(t) return {it=DATA, cols=t;n=0} end

  else
    for j,col in pairs(i.cols) do add(col,v[j]) end

  else
    local u={}; for k,v in pairs(i.cols) do u[k]=sample(v) end; return u end
  ```

- Notes:
  - This design supports heterogenous columns (NUM, TRI, SYM).


11) Sampling and Monte Carlo methods: drawing many random
    samples, aggregating results, and using sampling to
    approximate distributional properties.

- Explanation:
  - `samples` generates many draws from a distribution and
    sorts them to estimate quantiles; `tens` picks five summary
    positions (quintiles) from the sorted list.

- Code (`samples` and `tens`):

  ```lua
  local function samples(i,  n,   u)
    u={}; for j=1,(n or 10^4) do u[j] = sample(i) end; table.sort(u); return u end

  local function tens(t,  n,      f) 
    n,f = #t//20,floor
    return {f(t[n]), f(t[5*n]), f(t[10*n]), f(t[15*n]), f(t[19*n])} end
  ```

- Notes:
  - Monte Carlo sampling is simple but costs O(n log n) to sort
    the generated values; streaming quantile estimators avoid
    storing/sorting all samples.


12) Sorting and quantile estimation: sorting samples and
    selecting indices to compute quintiles/five-number summaries.

- Explanation:
  - `samples` sorts a vector of sampled values, `tens` uses
    indices at 5%, 25%, 50%, 75%, 95% (approx) to form a summary.

- Code (`tens` shown above).

- Notes:
  - For production with large n, use online quantile
    estimators (e.g., P² or GK) to reduce memory.


13) Statistical summary functions: constructing and interpreting
    five-number/quintile summaries and simple tabular summaries.

- Explanation:
  - `tens` returns a five-value summary used by `eg` demos and
    printing via `cat` to show representative quantiles.

- Code (`cat` helper and tens usage):

  ```lua
  local function cat(t) print("{".. table.concat(t,", ") .."}") end

  eg["--num"]  = function(_) cat(tens(samples(NUM(30,5)))) end
  ```

- Notes:
  - The chosen indices in `tens` are implementation-specific but
    provide a quick snapshot of distribution shape.


14) Numerical stability and edge cases: handling small sample
    sizes (n < 2), zero variance cases, and guarding against
    negative m2 due to floating-point error.

- Explanation:
  - `sd` is guarded to be 0 when `n < 2` or `m2 < 0`. Small
    floating-point errors may produce tiny negative `m2`.

- Code (guard in `add`):

  ```lua
  i.sd = (i.n < 2 or i.m2 < 0) and 0 or (i.m2 / (i.n - 1))^0.5
  ```

- Notes:
  - Defensive guards like this are important for long-running
    streams and finite-precision arithmetic.


15) Performance considerations: time complexity of repeated
    sampling and sorting, and memory allocation for large sample
    sets.

- Explanation:
  - `samples` allocates O(n) memory and sorts (O(n log n)).
  - Streaming stats (`add` with Welford) are O(1) per sample and
    require only O(1) memory.

- Code (`samples` reiteration):

  ```lua
  local function samples(i,  n,   u)
    u={}; for j=1,(n or 10^4) do u[j] = sample(i) end; table.sort(u); return u end
  ```

- Notes:
  - For very large experiments prefer streaming or reservoir
    sampling and targeted estimators for quantiles.


16) Common Lua idioms used here: constructor functions returning
    typed tables, lightweight tagging via `it` fields, and using
    function tables for small test examples (`eg` table).

- Explanation:
  - Constructors return small tables with `it` pointing to the
    constructor function itself; this allows `i.it == NUM` checks
    and calling `col.it()` to create new columns.

- Code (examples shown earlier: NUM, TRI, SYM, eg, clone):

  ```lua
  local function NUM(mu,sd) return {it=NUM, n=0, mu=mu or 0, m2=0, sd=sd or 0} end

  local function TRI(lo,mid,hi) return {it=TRI,n=0, lo=lo or 0, mid=mid or 0.5, hi=hi or 1} end

  local eg = {}
  eg["--tri"]  = function(_) cat(tens(samples(TRI(10,20,60)))) end
  ```

- Notes:
  - Using the constructor function itself as the tag (`it=NUM`)
    makes creating "new" columns easy by calling `col.it()`.


