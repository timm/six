# 54 Programming Heuristics Illustrated

XXX data molde laiga. presentation layer seeprete to business model

XXX too many vars==> too many ideas
XXX vars passed as a group to a subfunction ==> hidden objects

XXX yo yo is hatton's point (does oo syntax with the say we thing)

XXX test driven devlopment fig3 of https://ieeexplore.ieee.org/document/10352439
offers details on test

A comprehensive catalog of programming heuristics with examples from `two.lua`, Python, and larger systems.

These heuristics are represent some basic
ideas about what is "good" SE.

But be careful how you use them. If you only use this knowledge to
complain about 'bad code,' you become the bottleneck to other people'
work. But if you use
it to quietly refactor and fix the problems you see, you can earn
a reputataion as a tech guru.

---

## 1. DRY (Don't Repeat Yourself)

**In two.lua:**

```lua
local help = [[
  -b  bins=7     Number of bins for discretization.
  -e  era=30     Update model every `era` number of rows.
  -r  ruleMax=3  Max conditions in a rule.
  -s  seed=42    Random number seed.]]

local the={}; for k,v in help:gmatch("(%S+)=(%S+)") do the[k] = coerce(v) end
````

Single source of truth - help string defines both documentation AND defaults.

**Python example:**

```python

# Bad: Define settings twice
DEFAULT_TIMEOUT = 30
parser.add_argument('--timeout', default=30, help='Timeout in seconds (default: 30)')

# Good: Define once
DEFAULTS = {'timeout': 30, 'retries': 3}
for key, val in DEFAULTS.items():
    parser.add_argument(f'--{key}', default=val, help=f'{key} (default: {val})')
```

**Bigger system example:**
Django's database models define the schema once, then auto-generate admin interfaces, forms, migrations, and API serializers from that single definition.

-----

## 2\. Rule of Representation (Fold knowledge into data)

**In two.lua:**

```lua
col = (s:match"^[A-Z]" and NUM or SYM)(n,s)
t = s:find"[+-]$" and y or x
```

Column names encode the schema - uppercase=numeric, `+`/`-`=goals, `X`=skip.

**Python example:**

```python
# Encode validation rules in data
RULES = {
    'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
    'phone': r'^\d{3}-\d{3}-\d{4}$',
    'zip': r'^\d{5}$'
}

def validate(field, value):
    return re.match(RULES[field], value)
```

**Bigger system example:**
Unix file permissions (`rwxr-xr--`) encode all access rules in 9 bits. The `chmod` program is simple because the data structure (permission bits) carries the knowledge.

-----

## 3\. Rule of Simplicity

**In two.lua:**

```lua
local function add(i,v,  inc)
  if v == "?" then return v end
  inc = inc or 1
  i.n = i.n + inc
  if i.mode then i.has[v] = inc + (i.has[v] or 0) 
  elseif i.mu then ...
  elseif i.rows then ...
```

One function handles NUM, SYM, and DATA with minimal branching.

**Python example:**

```python
def median(numbers):
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    return sorted_nums[mid] if n % 2 else (sorted_nums[mid-1] + sorted_nums[mid]) / 2
```

Simple, direct algorithm. No complex edge case handling.

**Bigger system example:**
Git's object model - everything is either a blob, tree, commit, or tag. Four types, composed simply, create an entire version control system.

-----

## 4\. Rule of Parsimony

**In two.lua:**
Entire incremental XAI system in \~150 lines. Functions like:

```lua
local function cut(a0,n,  data)
  local a1,a2 = {},{}
  for j,v in ipairs(a0) do if j <= n then a1[1+#a1]=v else a2[1+#a2]=v end end
  if data then return clone(data,a1),clone(data,a2) end
  return a1,a2 end
```

**Python example:**

```python
# Flask web server in 5 lines
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello(): return "Hello World!"

app.run()
```

**Bigger system example:**
SQLite is \~150K lines for a full SQL database. Compare to Oracle's millions of lines. Parsimony wins for embedded use.

-----

## 5\. Rule of Clarity

**In two.lua:**

```lua
local lt = function(f) return function(a,b) return f(a) < f(b) end end
local cat = function(a) return "{".. table.concat(a," ") .."}" end
```

Names tell you exactly what they do: `lt` makes comparators, `cat` concatenates.

**Python example:**

```python
def is_palindrome(text):
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
```

Name and implementation clearly express intent.

**Bigger system example:**
Go's error handling - `if err != nil { return err }` is verbose but crystal clear. No hidden control flow like exceptions.

-----

## 6\. Rule of Economy

**In two.lua:**

```lua
local shuffle = function(t,    n)
  for m=#t,2,-1 do n=math.random(m); t[m],t[n]=t[n],t[m] end; return t end
```

Simple Fisher-Yates, not some optimized version. Programmer time \> machine time.

**Python example:**

```python
# Simple bubble sort for teaching
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
```

Not efficient, but easy to understand and maintain.

**Bigger system example:**
Python's `sorted()` uses Timsort - it's complex internally, but the API is dead simple: `sorted(items)`. Economy of interface, not implementation.

-----

## 7\. Rule of Generation

**In two.lua:**

```lua
local the={}; for k,v in help:gmatch("(%S+)=(%S+)") do the[k] = coerce(v) end
```

Generate config parser from help string automatically.

**Python example:**

```python
# Generate test cases from data
test_cases = [(i, i**2) for i in range(10)]

for input_val, expected in test_cases:
    assert square(input_val) == expected
```

**Bigger system example:**
Protocol Buffers - define data schema once, generate serializers/deserializers for 20+ languages automatically.

-----

## 8\. Rule of Least Surprise

**In two.lua:**

```lua
local function add(i,v,  inc) ...
local function sub(i,v) return add(i,v,-1) end
```

`add` adds, `sub` subtracts. Does what the name says.

**Python example:**

```python
class Stack:
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop()
    def peek(self): return self.items[-1]
```

Method names are intuitive verbs that do exactly what you expect.

**Bigger system example:**
jQuery's `$('.class').hide()` - method names are verbs that do exactly what they say. No surprises.

-----

## 9\. Separation of Concerns

**In two.lua:**

```lua
-- File I/O
local function csv(file,    src)
  src = assert(io.open(file))
  return function(    s)
    s = src:read()
    if s then return s2a(s) else src:close() end end end

-- String parsing
local function s2a(s,   a)
  a={}; for s1 in s:gmatch"([^,]+)" do a[1+#a] = coerce(s1) end; return a end

-- Type conversion
local function coerce(s) 
  if s then return tonumber(s) or s:match'^%s*(.-)%s*$' end end
```

Each function handles one concern: I/O, parsing, or type conversion.

**Python example:**

```python
# Separate data access, business logic, presentation
class UserRepository:
    def get_user(self, id): return db.query(User).get(id)

class UserService:
    def activate_user(self, user_id):
        user = self.repo.get_user(user_id)
        user.active = True
        return user

class UserView:
    def render(self, user): return f"<div>{user.name}</div>"
```

**Bigger system example:**
MVC pattern - Models handle data, Views handle presentation, Controllers handle user input. Each concern separated.

Important sub-case. 

- don't pollute the presetation layer with model concerns
- e.g. dont always print to console

### Should you replace `print` with `say`?

**Yes.** Replacing raw `print` statements is a best practice in software engineering. Relying on raw prints creates "noise" that is difficult to turn off when you move from development to production.

You generally have two paths to solve this: the **Custom Wrapper** (your "say" idea) or **Standard Logging**.

#### Option 1: The "Say" Wrapper (Quick & Simple)

This is exactly what you proposed. It is a lightweight solution perfect for **scripts, CLI tools, and small prototypes**.

**How it works:**
You wrap the print function in a conditional check based on a global flag.

```python
# Configuration
VERBOSE = True  # Toggle this single flag to silence the app

def say(message):
    if VERBOSE:
        print(f"[INFO] {message}")

# Usage
say("Fetching data...")     # Prints only if VERBOSE is True
print("Fatal Error: 404")   # Always prints (standard print for actual results)
```

**Pros:**

  * **Zero Dependencies:** No libraries to import or configure.
  * **Total Control:** You can easily add timestamps or colors to the `say` function later.
  * **Binary Silence:** It is either ON or OFF.

#### Option 2: The Logging Library (The Industry Standard)

If your project is an **application, a server, or a library used by others**, you should skip the "say" function and use a logging library (like Python's `logging`, Java's `Log4j`, or JS `winston`).

**How it works:**
Instead of a binary on/off switch, you use **Levels**. This allows you to silence "chatter" while keeping "warnings" active.

```python
import logging

# Configuration: Set to INFO to hide DEBUG messages
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger()

# Usage
logger.debug("Variable x = 5")        # Silenced (Level is too low)
logger.info("Process started.")       # Printed
logger.warning("Disk space low.")     # Printed
logger.error("Database crashed!")     # Printed
```

**Pros:**

  * **Granularity:** You can silence trivia without silencing warnings.
  * **Destinations:** You can send logs to a file, the console, and an email simultaneously.
  * **Standardization:** Other developers already know how to use it.


#### Comparison Summary

| Feature | Raw `print()` | Custom `say()` Wrapper | Standard `logging` |
| :--- | :--- | :--- | :--- |
| **Control** | None | High (Custom code) | High (Configuration) |
| **Silencing** | Manual deletion | **Single Flag (All or Nothing)** | **Leveled (Debug vs Error)** |
| **Complexity** | Low | Low | Medium |
| **Best For** | Throwaway code | Scripts & Tools | Production Apps |

#### Recommendation

1.  **Refactor immediately:** Move away from raw `print` statements for any informational text.
2.  **Start with `say`:** If you just need a "mute button," your proposed solution is perfect.
3.  **Upgrade to `logging` later:** If the project grows and you need to differentiate between "This is just info" and "This is a warning," switch to a logging library.


-----

## 10\. Single Responsibility Principle

**In two.lua:**

```lua
local function shuffle(t,    n)  -- Only shuffles
local function cut(a0,n,  data)  -- Only splits
local function norm(i,v)         -- Only normalizes
```

**Python example:**

```python
def read_file(path):
    with open(path) as f:
        return f.read()

def parse_json(text):
    return json.loads(text)

def validate_config(config):
    assert 'version' in config
    return config

# Each does one thing
config = validate_config(parse_json(read_file('config.json')))
```

**Bigger system example:**
Unix utilities - `grep` only searches, `sort` only sorts, `uniq` only deduplicates. Compose them with pipes.

-----

## 11\. Open/Closed Principle

**In two.lua:**

```lua
local function add(i,v,  inc)
  if v == "?" then return v end
  inc = inc or 1
  i.n = i.n + inc
  if i.mode then i.has[v] = inc + (i.has[v] or 0) 
  elseif i.mu then ...
  elseif i.rows then ...
```

Open for extension (new types via new fields), closed for modification (don't change `add`).

**Python example:**

```python
class Shape:
    def area(self): raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

class Square(Shape):
    def __init__(self, s): self.s = s
    def area(self): return self.s ** 2

# Can add new shapes without modifying existing code
shapes = [Circle(5), Square(4)]
total_area = sum(s.area() for s in shapes)
```

**Bigger system example:**
Linux kernel modules - add new device drivers without modifying kernel core. Open for extension, closed for modification.

-----

## 12\. Composition Over Inheritance

**In two.lua:**

```lua
function DATA(  src) return adds(src, {n=0,rows={},cols=nil}) end
function COLS(row,    t,x,y,all,col)
  x,y,all = {},{},{}
  for n,s in ipairs(row) do
    col = (s:match"^[A-Z]" and NUM or SYM)(n,s)
    all[n] = col ...
```

DATA has COLS, COLS has array of NUM/SYM. Tables composed, not inherited.

**Python example:**

```python
class Engine:
    def start(self): return "Engine running"

class Wheels:
    def roll(self): return "Rolling"

class Car:
    def __init__(self):
        self.engine = Engine()
        self.wheels = Wheels()
    
    def drive(self):
        return f"{self.engine.start()}, {self.wheels.roll()}"
```

Car composed of Engine and Wheels, not inheriting from them.

**Bigger system example:**
React components - compose small components into larger ones. No deep inheritance hierarchies, just composition.

-----

## 13\. Uniform Access Principle

**In two.lua:**

```lua
local function mid(i)
  if i.mu then return i.mu 
  elseif i.has then return mode(i.has) 
  elseif i.rows then
    i._mid = i._mid or mode(i.has)
    return i._mid end end
```

Same interface `mid(i)` works for NUM, SYM, or DATA.

**Python example:**

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

t = Temperature(100)
print(t.fahrenheit)  # Accessed like attribute, computed like method
```

**Bigger system example:**
Ruby - `array.length` and `string.length` use same interface, don't care if it's a method or property.

-----

## 14\. Command-Query Separation

**In two.lua:**

```lua
-- Commands (modify state, but also return for chaining)
local function add(i,v,  inc) ... end  

-- Queries (just read, never modify)
local function mid(i) ...              
local function distx(i,row1,row2) ...  
```

**Python example:**

```python
class Stack:
    # Command - modifies state
    def push(self, item):
        self.items.append(item)
    
    # Query - just reads
    def size(self):
        return len(self.items)
    
    # Command that also returns (useful for chaining)
    def pop(self):
        return self.items.pop()
```

**Bigger system example:**
SQL - `SELECT` queries don't modify data, `INSERT/UPDATE/DELETE` commands do. Clear separation.

-----

## 15\. Fail Fast

**In two.lua:**

```lua
src = assert(io.open(file))
```

Die immediately if file missing, don't propagate errors everywhere.

**Python example:**

```python
def divide(a, b):
    assert b != 0, "Cannot divide by zero"
    return a / b

def process_user(user):
    assert user is not None, "User cannot be None"
    assert user.email, "User must have email"
    return send_email(user.email)
```

**Bigger system example:**
Rust's `unwrap()` - panic immediately on None/Err rather than silently propagating null through the system.

-----

## 16\. Duck Typing / Polymorphism via Duck Typing

**In two.lua:**

```lua
local function add(i,v,  inc)
  ...
  if i.mode then i.has[v] = inc + (i.has[v] or 0) 
  elseif i.mu then ...
```

"If it has `.mu`, treat it as NUM; if it has `.mode`, treat it as SYM"

**Python example:**

```python
def process(file_like):
    data = file_like.read()
    file_like.close()
    return data

# Works with real files, StringIO, network sockets, etc.
from io import StringIO
process(open('data.txt'))
process(StringIO("hello"))
```

**Bigger system example:**
Python's file-like objects - anything with `.read()`, `.write()`, `.close()` can be treated as a file. StringIO, network sockets, HTTP responses all work the same.

-----

## 17\. Postel's Law (Robustness Principle)

**In two.lua:**

```lua
local function aha(col,v1,v2)
  if v1=="?" and v2=="?" then return 1 end
  if col.mode then return v1==v2 and 0 or 1 end
  v1 = v1 ~= "?" and v1 or (v2 > 0.5 and 0 or 1)
  v2 = v2 ~= "?" and v2 or (v1 > 0.5 and 0 or 1)
  return math.abs(v1 - v2) end
```

Liberal in what you accept - handles missing values gracefully.

**Python example:**

```python
def safe_int(value, default=0):
    """Accept strings, floats, None - be liberal"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

safe_int("42")      # 42
safe_int("hello")   # 0
safe_int(None)      # 0
safe_int(3.14)      # 3
```

**Bigger system example:**
HTML parsers - browsers accept malformed HTML and do their best to render it. Conservative in output (valid HTML), liberal in input (broken HTML).

-----

## 18\. Principle of Least Knowledge (Law of Demeter)

**In two.lua:**

```lua
return function(row)  return d(row,best) - d(row, rest) end
```

`two()` returns a function, not exposing internal `best`/`rest` structures.

**Python example:**

```python
# Bad: reaches through multiple objects
customer.wallet.money.subtract(price)

# Good: ask, don't reach
customer.pay(price)

class Customer:
    def pay(self, amount):
        self.wallet.deduct(amount)
```

**Bigger system example:**
jQuery - `$('#id').find('.class').hide()` - each method only knows about what it returns, not the whole DOM tree structure.

-----

## 19\. Make Illegal States Unrepresentable

**In two.lua:**

```lua
function NUM(at,s) 
  return {at=at or 0, of=s, n=0, mu=0, m2=0, sd=0,
          best=(tostring(s) or ""):find"+$" and 1 or 0} end

function SYM(at,s) return {at=at, of=s, n=0, has={}, mode=0, most=-1} end
```

NUM has `mu/m2/sd`, SYM has `has/mode` - can't accidentally mix them.

**Python example:**

```python
from enum import Enum

class Status(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3

# Can't accidentally set status to "maybe" or 42
order.status = Status.APPROVED  # OK
order.status = "approved"       # Type error
```

**Bigger system example:**
Rust's type system - `Option<T>` means "might be None", forcing you to handle the case. Can't accidentally use null.

-----

## 20\. Worse is Better

**In two.lua:**

```lua
local function mode(d,   v,n)
  v,n = nil,0
  for v1,n1 in pairs(d) do if n1>n then v,n=v1,n1 end end
  return v end 
```

O(n) scan, not a maintained heap. Simple, works, good enough.

**Python example:**

```python
# Simple O(n²) solution for small lists
def find_duplicates(items):
    dups = []
    for i, item in enumerate(items):
        if item in items[i+1:]:
            dups.append(item)
    return dups
```

For small lists, clarity beats optimization.

**Bigger system example:**
C's `malloc/free` vs garbage collection. Simple, predictable, worse than GC in some ways but wins for systems programming.

-----

## 21\. Referential Transparency

**In two.lua:**

```lua
local function distx(i,row1,row2,     d)
  d=0; for _,x in pairs(i.cols.x) do d= d + aha(x, row1[x.at],row2[x.at])^2 end
  return sqrt(d/#i.cols.x) end

local function norm(i,v)
  return 1/(1 + math.exp(-1.7 * (v - i.mu)/(i.sd + 1e-32))) end
```

Pure functions - same inputs always give same outputs.

**Python example:**

```python
# Referentially transparent
def add(a, b):
    return a + b

# Not referentially transparent
counter = 0
def increment():
    global counter
    counter += 1
    return counter
```

**Bigger system example:**
Functional programming languages like Haskell - pure functions are the default, side effects are explicit and tracked by type system.

-----

## 22\. Lazy Evaluation / Generators

**In two.lua:**

```lua
local function csv(file,    src)
  src = assert(io.open(file))
  return function(    s)
    s = src:read()
    if s then return s2a(s) else src:close() end end end
```

Returns a function that reads one line at a time, not all at once.

**Python example:**

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Only computes what you use
for i, fib in enumerate(fibonacci()):
    if i > 10: break
    print(fib)
```

**Bigger system example:**
Python's `range()` - `range(1000000)` doesn't create a million numbers in memory, it creates a generator that yields them one at a time.

-----

## 23\. Factory Pattern

**In two.lua:**

```lua
function COLS(row,    t,x,y,all,col)
  x,y,all = {},{},{}
  for n,s in ipairs(row) do
    col = (s:match"^[A-Z]" and NUM or SYM)(n,s)
    all[n] = col
```

The column name determines which constructor to call (NUM or SYM).

**Python example:**

```python
def create_logger(log_type):
    if log_type == "file":
        return FileLogger()
    elif log_type == "console":
        return ConsoleLogger()
    elif log_type == "network":
        return NetworkLogger()

logger = create_logger("file")
```

**Bigger system example:**
Django's database backends - `connection.cursor()` returns different cursor objects (PostgreSQL, MySQL, SQLite) based on configuration.

-----

## 24\. Builder Pattern (Fluent Interface)

**In two.lua:**

```lua
add(seen, add(best, row))
```

Chaining operations - `add` returns the added value so you can immediately add it somewhere else.

**Python example:**

```python
class QueryBuilder:
    def __init__(self):
        self.query = ""
    
    def select(self, fields):
        self.query += f"SELECT {fields} "
        return self
    
    def from_table(self, table):
        self.query += f"FROM {table} "
        return self
    
    def where(self, condition):
        self.query += f"WHERE {condition}"
        return self

# Fluent chaining
query = QueryBuilder().select("*").from_table("users").where("age > 18")
```

**Bigger system example:**
jQuery: `$('#element').fadeIn().addClass('active').slideDown()` - each method returns the object so you can chain.

-----

## 25\. Strategy Pattern

**In two.lua:**

```lua
local function distys(i,  rows,      y)
   y = function(row) return disty(i, row) end
   return sort(rows or i.rows, function(r1,r2) return y(r1) < y(r2) end) end
```

Pass in different comparison functions to get different sorting behaviors.

**Python example:**

```python
class PaymentProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def process(self, amount):
        return self.strategy.pay(amount)

class CreditCard:
    def pay(self, amount): return f"Paid ${amount} with credit card"

class PayPal:
    def pay(self, amount): return f"Paid ${amount} with PayPal"

processor = PaymentProcessor(CreditCard())
processor.process(100)
```

**Bigger system example:**
JavaScript's `Array.sort()` - pass any comparison function: `items.sort((a,b) => a.price - b.price)`.

-----

## 26\. Default Arguments / Sensible Defaults

**In two.lua:**

```lua
function NUM(at,s) 
  return {at=at or 0, of=s, n=0, mu=0, m2=0, sd=0,
          best=(tostring(s) or ""):find"+$" and 1 or 0} end
```

Uses `or` to provide defaults when arguments are nil.

**Python example:**

```python
def greet(name="World", greeting="Hello"):
    return f"{greeting}, {name}!"

greet()                          # "Hello, World!"
greet("Tim")                     # "Hello, Tim!"
greet("Tim", "Hi")              # "Hi, Tim!"
greet(greeting="Hey")           # "Hey, World!"
```

**Bigger system example:**
Python's `requests.get()` - `requests.get('http://example.com')` has sensible defaults for timeout, headers, SSL verification.

-----

## 27\. Null Object Pattern

**In two.lua:**

```lua
local function add(i,v,  inc)
  if v == "?" then return v end
  inc = inc or 1
  ...
```

"?" is treated as a special null/missing value. Code handles it gracefully.

**Python example:**

```python
class NullLogger:
    def log(self, msg): pass
    def error(self, msg): pass

class RealLogger:
    def log(self, msg): print(f"LOG: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")

# No if-checks needed
logger = NullLogger() if quiet_mode else RealLogger()
logger.log("Starting process")  # Works either way
```

**Bigger system example:**
NumPy's NaN handling - operations on NaN propagate gracefully: `np.mean([1, 2, np.nan, 4])` returns `nan` rather than crashing.

-----

## 28\. Immutable Core, Mutable Shell

**In two.lua:**

```lua
-- Immutable/pure calculations
local function distx(i,row1,row2,     d)
  d=0; for _,x in pairs(i.cols.x) do d= d + aha(x, row1[x.at],row2[x.at])^2 end
  return sqrt(d/#i.cols.x) end

-- Mutable updates
local function add(i,v,  inc)
  i.n = i.n + inc
  ...
```

**Python example:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
    def distance_to(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

# Core data is immutable, but can build new points
p1 = Point(0, 0)
p2 = Point(3, 4)
# p1.x = 5  # Error! Frozen
```

**Bigger system example:**
React's virtual DOM - rendering functions are pure (props in → virtual DOM out), but the framework handles mutations to the real DOM separately.

-----

## 29\. Caching / Memoization

**In two.lua:**

```lua
local function mid(i)
  ...
  elseif i.rows then
    i._mid = i._mid or mode(i.has)
    return i._mid end end
```

Cache the computed `_mid` value. Compute once, reuse many times.

**Python example:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# Exponential → linear with one line
fibonacci(100)  # Fast!
```

**Bigger system example:**
Redis - entire databases dedicated to caching. Web apps cache database queries, API responses, rendered HTML.

-----

## 30\. Small Functions (Extract Method)

**In two.lua:**

```lua
local function mode(d,   v,n)
  v,n = nil,0
  for v1,n1 in pairs(d) do if n1>n then v,n=v1,n1 end end
  return v end 

local function mid(i)
  if i.mu then return i.mu 
  elseif i.has then return mode(i.has) 
  ...
```

**Python example:**

```python
def process_order(order):
    validate_order(order)
    charge_customer(order)
    send_confirmation(order)
    update_inventory(order)

def validate_order(order):
    assert order.items, "Order must have items"
    assert order.customer, "Order must have customer"
```

**Bigger system example:**
Unix philosophy - `cat log | grep ERROR | sort | uniq -c | sort -rn | head` - small tools composed.

-----

## 31\. Guard Clauses (Early Return)

**In two.lua:**

```lua
local function add(i,v,  inc)
  if v == "?" then return v end
  inc = inc or 1
  i.n = i.n + inc
  if i.mode then i.has[v] = inc + (i.has[v] or 0) 
  elseif i.mu then ...
```

**Python example:**

```python
def process_payment(amount, account):
    if amount <= 0:
        return "Invalid amount"
    
    if not account:
        return "No account"
    
    if account.balance < amount:
        return "Insufficient funds"
    
    # Happy path has minimal nesting
    account.balance -= amount
    return "Success"
```

**Bigger system example:**
Express.js middleware - authentication checks return early:

```javascript
function requireAuth(req, res, next) {
  if (!req.user) return res.status(401).send('Unauthorized');
  next();
}
```

-----

## 32\. Intentional Naming

**In two.lua:**

```lua
local function distx(i,row1,row2,     d)  -- distance in X space
local function disty(i,row,     d)        -- distance in Y space
local function distys(i,  rows,      y)   -- sort all by Y distance
```

Names tell you exactly what space you're operating in.

**Python example:**

```python
# Bad
def calc(x, y):
    return x * y * 0.7

# Good
def calculate_discounted_price(original_price, quantity, discount_rate=0.7):
    return original_price * quantity * discount_rate
```

**Bigger system example:**
Ruby on Rails - `User.find(id)` finds one, `User.where(name: 'Tim')` finds many, `user.save` persists.

-----

## 33\. Closure (Lexical Scope Capture)

**In two.lua:**

```lua
return function(row)  return d(row,best) - d(row, rest) end
```

The returned function "closes over" `d`, `best`, and `rest` from the enclosing scope.

**Python example:**

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor  # Captures 'factor' from outer scope
    return multiply

times_three = make_multiplier(3)
times_five = make_multiplier(5)

print(times_three(10))  # 30
print(times_five(10))   # 50
```

**Bigger system example:**
JavaScript event handlers - `button.onclick = () => this.handleClick()` captures `this` from the surrounding context.

-----

## 34\. Optional Chaining / Safe Navigation

**In two.lua:**

```lua
best=(tostring(s) or ""):find"+$" and 1 or 0
```

Convert to string, or use empty string if nil. Chain safely without crashes.

**Python example:**

```python
# Using dict.get() for safe navigation
user_name = user.get('profile', {}).get('name', 'Anonymous')

# Or with walrus operator
if (profile := user.get('profile')) and (name := profile.get('name')):
    print(name)
```

**Bigger system example:**
JavaScript's optional chaining: `user?.address?.street?.name` - if any part is undefined, entire expression becomes undefined instead of throwing TypeError.

-----

## 35\. KISS (Keep It Simple, Stupid)

**In two.lua:**

```lua
local function cli(d,funs)
  for i,s in pairs(arg) do
    if funs[s]
    then funs[s](coerce(arg[i+1])) ...
```

The command line argument parser is a simple loop checking a dictionary. No complex flag parsing libraries used.

**Python example:**

```python
# Simple config loading
import json
def load_config(path):
    with open(path) as f:
        return json.load(f)
```

Don't use a heavy configuration management library when a simple JSON load suffices.

**Bigger system example:**
Redis - uses a simple text-based protocol (RESP) that is human-readable and easy to parse, rather than a complex binary protocol.

-----

## 36\. YAGNI (You Aren't Gonna Need It)

**In two.lua:**

```lua
local function two(data) 
  -- ... logic for clustering ...
  return function(row) return d(row,best) - d(row, rest) end end
```

The code calculates clusters but doesn't implement features to "save" the model to disk or "export" to JSON. It runs, outputs, and exits.

**Python example:**

```python
class User:
    def __init__(self, name):
        self.name = name
        # YAGNI: Don't add address, phone, ssn until actually needed
```

**Bigger system example:**
Extreme Programming (XP) - emphasizes implementing only the user stories scheduled for the current iteration, never building infrastructure for future hypothetical requirements.

-----

## 37\. Avoid Premature Optimization

**In two.lua:**

```lua
local function distx(i,row1,row2,     d)
  d=0; for _,x in pairs(i.cols.x) do d= d + aha(x, row1[x.at],row2[x.at])^2 end
  return sqrt(d/#i.cols.x) end
```

Calculates distance on-the-fly every time. It does not cache a distance matrix (which would consume $O(N^2)$ memory) because the dataset size in this context doesn't warrant it yet.

**Python example:**

```python
# Write clear code first, optimize later
total = sum(item.price for item in cart)
# Don't switch to numpy arrays unless 'cart' has millions of items
```

**Bigger system example:**
Donald Knuth's famous quote regarding the layout of TeX: "Premature optimization is the root of all evil." He focused on correctness first, optimizing only the critical hotspots later.

-----

## 38\. Optimize for Reading, Not Writing

**In two.lua:**

```lua
local fmt = string.format
local function o(v, ...) -- complex stringification logic
```

The `o` function is complex to *write*, but it ensures that the *output* (and the code using it) is readable and clean.

**Python example:**

```python
# Verbose to write, easy to read
if user.is_active and user.has_permission and not user.is_blocked:
    grant_access()

# Hard to read (Code golf)
if all([u.a, u.p, not u.b]): g()
```

**Bigger system example:**
Python itself - strictly enforces indentation. It makes writing code slightly stricter, but guarantees that all code looks visually similar, optimizing for the reader.

-----

## 39\. Minimize Cognitive Load

**In two.lua:**

```lua
local help = [[
two.lua : stochastic incremental XAI
...
Options:
  -h             Show help.
  -b  bins=7     Number of bins for discretization. ]]
```

All configuration options are visible in one place at the top of the file. You don't have to hunt through 5 files to find the settings.

**Python example:**

```python
# Facade pattern helps minimize load
# Instead of importing 10 classes, import one
from my_library import easy_api
easy_api.run()
```

**Bigger system example:**
Go (Golang) - The language specification is small enough to hold in your head. It lacks features like generics (historically) or operator overloading to keep the mental model of the code simple.

-----

## 40\. Structured Programming

**In two.lua:**

```lua
local function distys(i,  rows,      y)
   y = function(row) return disty(i, row) end
   return sort(rows or i.rows, function(r1,r2) return y(r1) < y(r2) end) end
```

Uses clear block structures (functions, scoped variables) and higher-order functions instead of `goto` or spaghetti jumps.

**Python example:**

```python
# Structured control flow
try:
    process_data()
except Error:
    handle_error()
finally:
    cleanup()
```

**Bigger system example:**
Dijkstra's "Go To Statement Considered Harmful" - the foundation of modern languages (Java, C\#, etc.) which enforce structured loops and blocks over arbitrary jumps.

-----

## 41\. No Magic Numbers

**In two.lua:**

```lua
local the={}; for k,v in help:gmatch("(%S+)=(%S+)") do the[k] = coerce(v) end
...
if n > 256 then break end  -- Wait, 256 is magic!
```

*Critique:* `two.lua` actually *violates* this in `if n > 256`.
*Correction:* It moves most numbers to `help` string (`bins=7`, `era=30`), making them named constants in `the`.

**Python example:**

```python
# Bad
time.sleep(86400)

# Good
SECONDS_IN_DAY = 86400
time.sleep(SECONDS_IN_DAY)
```

**Bigger system example:**
HTTP Status Codes - We use `HTTP_200_OK` or `HTTP_404_NOT_FOUND` in constants files rather than hardcoding `200` or `404` throughout the application logic.

-----

## 42\. Strict in Types, Loose in Values

**In two.lua:**

```lua
local function coerce(s) 
  if s then return tonumber(s) or s:match'^%s*(.-)%s*$' end end
```

The system is strict about needing a value (or a default), but loose in accepting a string and converting it to a number if it looks like one.

**Python example:**

```python
def add_to_cart(item_id):
    # Accepts int or string "123", converts to int 123
    id = int(item_id) 
    ...
```

**Bigger system example:**
REST APIs - Often accept "true", "True", or boolean `true` in JSON payloads for boolean fields to be accommodating to different clients.

-----

## 43\. Name Things Once

**In two.lua:**

```lua
local help = [[ ... -b  bins=7 ... ]]
-- The name "bins" is defined in the string, parsed into 'the.bins'.
-- We don't manually type 'the.bins = 7' separately.
```

The definitions in the help string drive the logic. The variable name exists in one place.

**Python example:**

```python
from collections import namedtuple

# Define field names once
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
# Use p.x, p.y - names are consistent
```

**Bigger system example:**
Terraform - You define a resource name (e.g., `aws_instance.web`) once, and reference that symbolic name elsewhere in the infrastructure definition.

-----

## 44\. Choose Boring Technology

**In two.lua:**

```lua
-- No "require 'torch'" or "require 'lfs'"
-- Uses only standard math, table, string, and io libraries.
```

The script runs on standard Lua. It doesn't require complex package managers or bleeding-edge compilers.

**Python example:**

```python
# Sticking to standard library when possible
import datetime # Built-in, boring, reliable
# vs
import arrow # Better API, but an extra dependency
```

**Bigger system example:**
PostgreSQL - Startups often choose Postgres (boring, reliable, standard) over niche new NoSQL databases because "boring" means "it won't lose my data at 3 AM."

-----

## 45\. Tell, Don’t Ask

**In two.lua:**

```lua
local function add(i,v,  inc)
  -- Logic for how to add is INSIDE the object 'i' (via the function)
  -- We don't ask "is i a NUM?" then do math.
  if i.mode then i.has[v] = ...
  elseif i.mu then ...
```

You tell the `add` function to process `v`, and the internal logic decides how to handle it based on the object's structure.

**Python example:**

```python
# Bad (Asking)
if wallet.balance > amount:
    wallet.balance -= amount

# Good (Telling)
wallet.debit(amount) # Internal check raises error if insufficient
```

**Bigger system example:**
Microservices - You send a command "Process Order" to the Order Service. You don't query the Order Service database, check the status, and then write a new status yourself.

-----

## 46\. Localize Side Effects

**In two.lua:**

```lua
math.randomseed(the.seed)
```

The randomness is seeded once at the very top level. Functions like `distx` are pure calculations; they don't change global state or print to the console.

**Python example:**

```python
def main():
    # Side effects (IO, DB) only in main/controller
    data = read_file()
    result = pure_calculation(data)
    write_file(result)

def pure_calculation(data):
    return data * 2 # No print statements here
```

**Bigger system example:**
Redux (React) - Reducers are pure functions with zero side effects. All side effects (API calls) are localized in "Thunks" or "Sagas".

-----

## 47\. Avoid Temporal Coupling

**In two.lua:**

```lua
local function two(data) 
  local train,test,start,todo,seen,best,rest,d
  shuffle(data.rows)
  train,test = cut(data.rows, data.n//2)
  -- ...
```

The `two` function initializes `train`, `test`, `seen` right before using them. It doesn't rely on a global `init()` having been called 5 minutes earlier.

**Python example:**

```python
# Bad: Order matters implicitly
obj.init()
obj.load()
obj.run()

# Good: Constructor handles it
obj = Runner(data) # Ready to go
obj.run()
```

**Bigger system example:**
Dependency Injection Containers - They ensure that when you request a service, all its dependencies are already created and wired together, removing manual temporal setup steps.

-----

## 48\. Avoid Boolean Parameters

**In two.lua:**

```lua
local function cut(a0,n,  data)
  -- 'data' is an optional object, not a boolean 'is_data'
  if data then return clone(data,a1),clone(data,a2) end
```

Instead of passing `true` to say "return data objects", it passes the data object itself. If it's nil, it returns lists.

**Python example:**

```python
# Bad
def create_user(name, is_admin=False): ...

# Good (Enums or separate methods)
def create_user(name, role=Role.USER): ...
def create_admin(name): ...
```

**Bigger system example:**
Windows API (bad example) - `CreateFile` takes many boolean flags, making calls cryptic (`true, false, true, false`). Modern APIs prefer passing a config object or specific types.

-----

## 49\. Design for Debuggability

**In two.lua:**

```lua
local function o(v,     list,dict)--> s;; Make anything a string.
  -- This entire function exists solely to make complex tables 
  -- human-readable for debugging/printing.
```

The code includes a robust "toString" equivalent (`o`) specifically to make internal state visible.

**Python example:**

```python
class User:
    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
    # Now print(user) gives useful info, not <object at 0x123>
```

**Bigger system example:**
Chrome DevTools - The entire web ecosystem is built with inspection tools in mind (Elements panel, Console, Network tab) to allow developers to peek into the runtime.

-----

## 50\. Error Handling Is Control Flow

**In two.lua:**

```lua
local function csv(file,    src)
  src = assert(io.open(file)) -- Stops flow if file fails
  return function(    s)
    s = src:read()
    if s then return s2a(s) else src:close() end end end
```

Using `assert` halts the program immediately if the file is invalid. The closure uses `if s then ... else close` to control the loop termination.

**Python example:**

```python
try:
    process_payment()
except InsufficientFunds:
    redirect_to_wallet() # Error drives the UX flow
```

**Bigger system example:**
Erlang/Elixir Supervisors - The "Let it Crash" philosophy. If a process errors, it crashes, and a supervisor catches that crash (control flow) to restart it.

-----

## 51\. Zero-One-Infinity Rule

**In two.lua:**

```lua
for n,s in ipairs(row) do
  -- Handles ANY number of columns. 
  -- Not restricted to "2 columns" or "10 columns".
```

The code works for 0 columns (empty), 1 column, or N columns. It doesn't arbitrary cap the schema size.

**Python example:**

```python
# Allow list of any size
def process_items(items):
    for item in items:
        ...
# Don't create variables item1, item2, item3
```

**Bigger system example:**
UNIX File Descriptors - You can open as many files as memory/OS limits allow. The system doesn't arbitrarily limit you to "3 open files."

-----

## 52\. CLI Modularity

**In two.lua:**

```lua
local function cli(d,funs)
  for i,s in pairs(arg) do
    if funs[s]
    then funs[s](coerce(arg[i+1])) ...
```

The CLI logic `cli` is generic. It takes a table of functions `funs` (egs). You can add new commands just by adding to `egs`, without changing the `cli` parser.

**Python example:**

```python
import argparse
# Argparse handles the parsing logic separate from your business logic
parser = argparse.ArgumentParser()
parser.add_argument('--train', action='store_true')
```

**Bigger system example:**
Git subcommands (`git commit`, `git add`) - Git is structured so that many subcommands are actually standalone binaries (`git-commit`, `git-add`) invoked by the main wrapper.

-----

## 53\. Pattern Matching (Simulated)

**In two.lua:**

```lua
local function add(i,v,  inc)
  if i.mode then ... -- It matches a SYM type
  elseif i.mu then ... -- It matches a NUM type
```

Lua lacks native pattern matching, so it simulates it by checking for the existence of unique keys (`mode` vs `mu`).

**Python example:**

```python
# Python 3.10+ Pattern Matching
match shape:
    case Circle(r):
        return 3.14 * r * r
    case Rectangle(w, h):
        return w * h
```

**Bigger system example:**
Rust `match` - The primary way to handle control flow. It forces you to handle every variant of an Enum, ensuring safety.

-----

## 54\. Variable Scoping (Local by Default)

**In two.lua:**

```lua
local DATA, NUM, SYM, COLS, clone, adds
local exp,sqrt,log  = math.exp, math.sqrt, math.log
```

Everything is declared `local`. This prevents polluting the global namespace and is faster in Lua.

**Python example:**

```python
def my_func():
    x = 10 # Local variable
    global y # Explicitly asking for global (discouraged)
```

**Bigger system example:**
JavaScript (`let`/`const` vs `var`) - Modern JS moved to block scoping (`let`) to avoid the issues caused by function-scoped or global variables (`var`).


You are right; while "Hungarian Notation" is the classic reference for encoding types in names, your `header.md` defines a much lighter, more ergonomic variant (e.g., `n` for number, `s` for string) that reduces visual noise while keeping the benefits.

Here are the missing heuristics (55–60) to complete your catalog, including the **Layered Architecture**, **TDD**, and the specific **Type Hinting** breakdown you requested.

-----

## 55\. Test-Driven Development (TDD)

**In two.lua:**

```lua
local function runs(  out)
  for k, fun in pairs(eg) do -- 'eg' is a table of test functions
    math.randomseed(the.seed) -- Reset seed before every test
    out = fun()
    if out == false then print("FAIL", k) else print("PASS", k) end
  end
end
```

The test runner is built into the file itself. You write the test in `eg` *before* the code to define the expected behavior.

**Python example:**

```python
import pytest

# Write this FIRST (Red)
def test_calculator_add():
    assert add(2, 3) == 5

# Write this SECOND (Green)
def add(a, b):
    return a + b
```

**Bigger system example:**
**CI/CD Pipelines (GitHub Actions):** Modern infrastructure won't let you merge code unless the test suite passes. The tests act as the "gatekeeper" of truth, enforcing that new code doesn't break old features.

-----

## 56\. Layered Architecture: Data Independence

**In two.lua:**

```lua
-- The logic (DATA class) doesn't know where data comes from.
function DATA:new(src)
  self.rows = {}
  if type(src) == "string" then csv(src, function(row) self:add(row) end) -- CSV file
  else for _,row in pairs(src or {}) do self:add(row) end                 -- In-memory table
  end 
end
```

The business logic (`DATA`) is decoupled from the storage mechanism. It works equally well with a CSV filename or a raw Lua table.

**Python example:**

```python
# The Repository Pattern
class UserRepository:
    def get(self, id):
        # Could be SQL, could be JSON, could be Redis.
        # The calling code doesn't need to know.
        return db.execute("SELECT * FROM users WHERE id=?", id)

user = repo.get(1) # Business logic is protected from SQL syntax
```

**Bigger system example:**
**ODBC / JDBC:** These drivers allow applications to connect to SQLite, Postgres, or Oracle using the exact same function calls. The database implementation is completely hidden from the application layer.

-----

## 57\. Layered Architecture: Dialog Independence

**In two.lua:**

```lua
-- Pure Logic (Core)
local function dist(r1, r2) return (r1.x - r2.x)^2 end

-- Presentation Layer (CLI)
local function cli() 
  print(dist(req_row(), db_row())) 
end
-- If we moved to a GUI, 'dist' would not change. Only 'cli' would be replaced.
```

The core algorithms do not contain `print` statements or GUI widgets. They return data, which the presentation layer decides how to display.

**Python example:**

```python
# Core Logic
def calculate_tax(income):
    return income * 0.3

# Web Presentation (Flask)
@app.route('/tax/<int:income>')
def web_tax(income):
    return f"<h1>Tax: {calculate_tax(income)}</h1>"

# CLI Presentation (Click)
@click.command()
def cli_tax(income):
    print(f"Tax is: {calculate_tax(income)}")
```

**Bigger system example:**
**X11 Window System / React Native:** The logic runs in one place (the client or the JS thread), and the "view" can be a Linux Desktop, an iOS screen, or an Android screen. The core logic is independent of the dialog toolkit.

-----

## 58\. Functional Programming (Higher-Order Functions)

**In two.lua:**

```lua
local function map(t, fun,    u) 
  u={}; for k,v in pairs(t) do u[k]=fun(v) end; return u 
end

-- Usage: Pass behavior as an argument
local squared = map({1,2,3}, function(x) return x*x end)
```

Functions are first-class citizens. You can pass logic (functions) around just like data.

**Python example:**

```python
# Passing behavior into a function
numbers = [1, 2, 3, 4]
evens = list(filter(lambda x: x % 2 == 0, numbers))
doubled = list(map(lambda x: x * 2, numbers))
```

**Bigger system example:**
**React Hooks / Callbacks:** `useEffect(() => { doSomething() })`. You pass a function to the framework, and the framework calls it back when the time is right.

-----

## 59\. Type Hinting (Hungarian vs. Lite vs. Modern)

**In two.lua (Lite Hungarian):**
Instead of verbose "System Hungarian" (`lpszName`), `two.lua` uses a "Lite" schema defined in the header:

```lua
-- n=number; s=string; b=boolean
-- a,d = array,dict 
-- ds,dn = dict of strings, dict of numbers

local function add(n, s, t) ... end
-- 'n' tells us it expects a number
-- 's' tells us it expects a string
-- 't' tells us it expects a table
```

This reduces cognitive load without the visual clutter of full Hungarian notation.

**Classic Hungarian (Historical Context):**

```c
// Apps Hungarian (Simonyi) - prefix indicates 'kind'
char  *szName;   // Zero-terminated String
int    iCount;   // Integer
long   lIndex;   // Long
```

**Python example (Modern Type Hints):**
Modern languages moved the hint from the *variable name* to the *syntax* itself.

```python
# Modern Type Hinting
def connect(timeout: int, retries: int = 3) -> bool:
    return True
```

The code documents itself. IDEs can now catch errors before you run the code.

**Bigger system example:**
**TypeScript:** JavaScript was "loose," causing millions of runtime errors. TypeScript added a layer of strict types on top, becoming the industry standard for large web apps because it catches errors at compile time.

-----

## 60\. Documentation as Contract

**In two.lua:**

```lua
local help = [[
NAME:
  two.lua
SYNOPSIS:
  Classifies rows into 'best' or 'rest'.
INPUTS:
  csv file with headers. 
  Uppercase headers are numerics.
]]
```

The documentation isn't separate from the code; it is embedded *in* the code, often driving the configuration parsing (as seen in Rule 1/7).

**Python example:**

```python
def square(n):
    """
    Returns the square of n.
    
    >>> square(2)
    4
    >>> square(-3)
    9
    """
    return n * n
```

Python Docstrings (`"""`) allow tools to auto-generate websites (Sphinx) and run tests (Doctest) directly from the documentation.

**Bigger system example:**
**OpenAPI (Swagger):** You write a YAML file describing your API. This file generates the documentation *and* the code *and* the testing tools. The documentation *is* the code.


Yes, absolutely. In software engineering, "personnel" and "process" heuristics are arguably more critical than syntax because they govern how the code actually gets written and maintained by humans.

Here are the heuristics for **tackling complexity**, **maintaining motivation**, and **sorting priorities**, formatted to match your existing catalog.

-----

## 61\. Gall's Law (Tackling Big Problems)

**In two.lua:**

```lua
-- Start simple. A complex system that works is invariably found to have 
-- evolved from a simple system that worked.
function DATA:new(src)
  self.rows = {} 
  -- Version 1: Just load the data. Worry about discretization later.
  if src then self:load(src) end
end
```

Do not try to build the complex version (bins, entropy, discretization) first. Build the version that just loads the file. If that works, add the next layer.

**Python example:**

```python
# The "Walking Skeleton"
# Don't build the whole API. Build one endpoint that returns "Hello World".
# Ensure the database, server, and network connect before adding logic.

@app.get("/")
def health_check():
    return {"status": "ok"} 
```

**Bigger system example:**
**The MVP (Minimum Viable Product):** Twitter started as a simple SMS service. Amazon started as a list of books. You cannot design a complex system from scratch; you must evolve it from a working simple system.

-----

## 62\. Weighted Shortest Job First (Agile Prioritization)

**In two.lua:**

```lua
-- Sorting the backlog (simulated)
local tasks = {
  {name="fix_typo",  cost=1,  val=1,  ratio=1},
  {name="crit_bug",  cost=5,  val=50, ratio=10}, -- Do this first!
  {name="new_feat",  cost=100,val=20, ratio=0.2}
}
table.sort(tasks, function(a,b) return a.ratio > b.ratio end)
```

To escape the "slump" of an infinite backlog, you don't sort by "importance" (Value) or "ease" (Cost). You sort by **Cost of Delay** (Value / Duration). This gives you the biggest bang for the buck immediately.

**Python example:**

```python
# The Eisenhower Matrix in code
def get_next_task(tasks):
    urgent = [t for t in tasks if t.urgent and t.important]
    if urgent: return urgent[0]
    
    plan = [t for t in tasks if not t.urgent and t.important]
    return plan[0] # Schedule these
```

**Bigger system example:**
**SAFe (Scaled Agile Framework):** Large enterprises formally calculate `WSJF = (User Value + Time Criticality) / Job Size`. This removes the "loudest person in the room" bias and provides a mathematical way to pick what to work on next.

-----

## 63\. Short Feedback Loops (Escaping Motivational Slumps)

**In two.lua:**

```lua
-- The Repl (Read-Eval-Print Loop) approach
-- Don't write 100 lines. Write 1, print it.
local n = 10
print(n) -- Sanity check: I am not crazy, the computer is listening.
```

Motivational slumps often come from working in the dark for too long. The cure is to shorten the loop between "I type code" and "I see result."

**Python example:**

```python
# TDD Red/Green loop
# 1. Write a failing test (Instant feedback: "It failed")
# 2. Write just enough code to pass (Instant feedback: "It passed")
# The dopamine hit of the "Green Bar" keeps you moving.
```

**Bigger system example:**
**Hot Reloading (React/Flutter/Vite):** In modern web dev, you save the file and the browser updates instantly without a refresh. This keeps the developer in the "Flow State," preventing the mind from wandering during compilation times.

-----

## 64\. The Bus Factor (Personnel Patterns)

**In two.lua:**

```lua
-- This code is written using 'Lite Hungarian'
-- so that if 'timm' gets hit by a bus, someone else knows that
-- 'nC' is a number representing a count.
local function bins(nC, sName) ... end
```

Code readability is not about the computer; it is about the *next* human. If only one person understands the code, the project is fragile.

**Python example:**

```python
# Docstrings are knowledge transfer
def calculate_variance(data):
    """
    Uses Welford's online algorithm to avoid catastrophic cancellation.
    Reference: Knuth Vol 2, p 232.
    """
    # The comment explains *why* we didn't just use sum(x^2), 
    # saving the next developer from "refactoring" it back to a buggy version.
```

**Bigger system example:**
**Pair Programming / Code Review:** In systems like Linux or Google's Monorepo, no code enters the codebase without being read by a second person. This ensures that knowledge is distributed, "escaping" the head of a single developer.

-----

## 65\. Conway's Law (Organization Architecture)

**In two.lua:**

```lua
-- The code is split into DATA, NUM, SYM.
-- If three different people work on this, they will naturally 
-- create three distinct modules to avoid stepping on each other's toes.
```

"Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations."

**Python example:**

```python
# Microservices often reflect team structures.
# Team A owns the 'User' service.
# Team B owns the 'Payment' service.
# They communicate via API (HTTP) because the teams talk via Slack/Meetings.
import requests
response = requests.get('http://payment-service/api/v1/charge')
```

**Bigger system example:**
**Amazon's "Two-Pizza Teams":** Amazon structures its teams so they are small enough to be fed by two pizzas. Consequently, their software architecture is composed of thousands of small, decoupled services. If they had a giant team, they would have built a giant monolith.

You are absolutely right to keep the momentum. The Spotify example is a perfect real-world analogy for the Space-Time tradeoff because it translates "Memory vs. CPU" into terms everyone understands: "Storage vs. Bandwidth."

Here is the final, polished set of the operational heuristics (66–70), including the corrected **Space-Time** (with Spotify) and **Idempotency** entries.

-----

## 66\. Fail Fast (Defensive Programming)

**In two.lua:**

```lua
function NUM:add(n)
  -- Don't wait for the math to return NaN later. 
  -- Stop execution immediately if the input is bad.
  assert(type(n) == "number", "NUM:add expects a number")
  self.n = self.n + 1
  ...
end
```

If the state is invalid, crash immediately. Debugging a crash at the source is 100x easier than debugging "why is my final calculation slightly off" three hours later.

**Python example:**

```python
def process_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative") # Stop right here.
    return math.log(age)
```

**Bigger system example:**
**Erlang "Let It Crash":** In telecom systems (and WhatsApp), instead of trying to recover from a corrupted state, a process kills itself immediately. The supervisor detects the death and spawns a fresh, clean replacement instantly.

-----

## 67\. Space-Time Tradeoff (Memoization with Invalidation)

**In two.lua:**

```lua
-- 1. THE CACHE: mid() calculates the central tendency (centroid) of all columns.
-- This is expensive (it loops over every column).
local function mid(i)
  -- If we are a DATA object (have rows) and have a cached answer, return it.
  if i.rows and i._mid then return i._mid end
  
  -- Otherwise, calculate it and STORE it in _mid
  local t={}; for _,col in pairs(i.cols.all) do t[1+#t] = mid(col) end 
  i._mid = t 
  return i._mid 
end

-- 2. THE INVALIDATION: When data changes, we must wipe the cache.
local function add(i,v,  inc)
  if i.rows then
    i._mid = nil -- <--- DIRTY FLAG: Data changed, so old cache is invalid
    ...
  end
end
```

We trade memory (`i._mid`) to save CPU cycles. However, unlike a static cache, this one is dynamic: the moment `add()` modifies the data, we explicitly set `i._mid = nil` so the next call to `mid()` knows to re-calculate.

**Python example:**

```python
class Dataset:
    def __init__(self):
        self._cached_stats = None
        self.data = []

    def add(self, row):
        self.data.append(row)
        self._cached_stats = None # Invalidate cache

    @property
    def stats(self):
        if self._cached_stats is None:
            # Expensive calculation happens only when needed
            self._cached_stats = calculate_heavy_stats(self.data)
        return self._cached_stats
```

**Bigger system example:**
**Spotify Local Cache:** Spotify downloads your frequently played songs to your device's hard drive (Space). When you press play, it reads from the disk instead of streaming from the internet. This trades **Storage Space** (on your phone) to save **Time/Bandwidth** (network latency).

-----

## 68\. The Law of Demeter (Principle of Least Knowledge)

**In two.lua:**

```lua
-- BAD: Reaching through objects
-- print(myModel.rows[1].cells[3]) 

-- GOOD: Ask the object to do the work for you
print(myModel:getCell(1, 3))
```

An object should only talk to its immediate friends. If you change how `rows` are stored (e.g., from an array to a database cursor), the "Bad" code breaks. The "Good" code survives because the implementation is hidden.

**Python example:**

```python
# Bad
user.wallet.credit_card.charge(100)

# Good
user.make_payment(100) # The user object knows how to handle its own wallet.
```

**Bigger system example:**
**Microservices API Gateways:** Service A never talks directly to Service B's database. It calls Service B's API. This ensures Service B can change its database schema without breaking Service A.

-----

## 69\. Idempotency (Config-Driven State Reset)

**In two.lua:**

```lua
-- The '-s' flag does two things:
-- 1. Updates the config record (the.seed)
-- 2. IMMEDIATELY forces the runtime state (math.randomseed) to match.
egs["-s"] = function(n) 
  math.randomseed(n) -- Reset the RNG now
  the.seed = n       -- Remember this for later
end
```

This ensures that the command-line argument isn't just a "suggestion" for future operations; it is an imperative command to reset the universe *right now*. This guarantees that `lua two.lua -s 42` behaves identically every single time it is run, regardless of what happened before that line was executed.

**Python example:**

```python
import random
import sys

def set_seed(n):
    # Update global config AND runtime state simultaneously
    CONFIG['seed'] = n
    random.seed(n)

if __name__ == "__main__":
    if "--seed" in sys.argv:
        # User input forces immediate deterministic state
        set_seed(int(sys.argv[sys.argv.index("--seed") + 1]))
```

**Bigger system example:**
**Terraform / Ansible:** These tools are designed to be idempotent. If you run "Ensure Server X exists" 50 times, it creates the server once and does nothing the other 49 times. It forces the reality to match the configuration, resetting state only if necessary.

-----

## 70\. The Pareto Principle vs. Premature Optimization

  * **Premature Optimization** is a rule about **Time** (When). "Don't optimize yet because you don't know what matters."
  * **The Pareto Principle** is a rule about **Focus** (Where). "When you *do* optimize, only look at the 20% of code that is running 80% of the time."

**In two.lua:**

```lua
-- Optimization Strategy:
-- 1. Write clear code first (Avoid Premature Opt).
-- 2. If slow, find the 'hot loop' (Pareto).
-- 3. Only optimize that loop.

function DATA:dist(row1, row2) 
   -- This function is called N^2 times. 
   -- Optimizing THIS function yields 80% of the speedup.
   -- Optimizing the CLI argument parser yields 0% of the speedup.
end
```

**Python example:**

```python
# cProfile output
# ncalls  tottime  filename:lineno(function)
# 100000    5.000  myscript.py:20(heavy_math)  <-- The 20% to fix
#      1    0.001  myscript.py:1(setup)        <-- The 80% to ignore
```

**Bigger system example:**
**Bug Bounties:** Microsoft found that fixing the top 20% of reported bugs eliminated 80% of the crashes and security errors. Not all bugs are created equal.

Here is the updated list. I have softened the tone on the "Root/Sudo" heuristic (\#73) to be about *privilege* rather than "brokenness," and I have converted the specific warnings from your "Ell/Backpacker" text into a new category of **Complexity & Dependency Anti-Patterns**.

-----

## 71\. VITAL (Vital Infrastructure: Acquire Locally)

**In two.lua:**

```lua
-- Instead of 'require "argparse"', we write 5 lines of code:
local the={}; for k,v in help:gmatch("(%S+)=(%S+)") do the[k] = coerce(v) end
```

If a dependency does one simple thing (like parsing flags or left-padding a string), **own it**. Copy the logic into your code. Do not import a 5MB library for a 5-line function. Dependencies break over time; your own code stays stable.

**Python example:**

```python
# Bad: pip install colorama (adds dependency, installation step, version conflicts)
# Good: Just define the ANSI codes you need.
class Colors:
    HEADER = '\033[95m'
    ENDC = '\033[0m'
```

**Bigger system example:**
**SQLite:** It has zero external dependencies. It doesn't even use the standard string library of the OS if it can avoid it. This makes it compilable on a toaster.

-----

## 72\. The Lindy Effect (Longevity via Simplicity)

**In two.lua:**

```lua
-- We use CSV. Not Parquet, not Protocol Buffers, not HDF5.
-- CSV was readable in 1980. It will be readable in 2080.
function csv(sFilename, fun) ... end
```

The longer a technology has been around (Text, Shell, Lua, SQL), the longer it is likely to remain around. New, complex formats (`.toml`, `.yaml`, `setup.py`) churn every 5 years. Bet on the technology that has already survived.

**Python example:**

```python
# Bad: Using a specific ORM version (SQLAlchemy 1.4)
# Good: Writing raw SQL queries. SQL is 50 years old and isn't changing.
cursor.execute("SELECT * FROM users WHERE id=?", (1,))
```

**Bigger system example:**
**Makefiles:** Despite thousands of "better" task runners (Grunt, Gulp, Webpack, Turbolore), `make` is still here because it is simple, file-based, and standard.

-----

## 73\. User-Space Sovereignty (Principle of Least Privilege)

**In two.lua:**

```lua
-- Does not require 'luarocks install'. 
-- Does not require writing to /usr/bin.
-- It runs where it sits.
```

Tools should respect the system they run on. Requiring `sudo` (root) to install a text-processing tool creates security risks and friction. Good tools run comfortably in user-space (`~/bin`) and clean up after themselves.

**Python example:**

```python
# Bad: Hardcoding paths to /var/log/myapp (Requires Root)
# Good: Adhering to XDG_DATA_HOME or local directories
log_dir = os.environ.get('XDG_DATA_HOME', './logs')
```

**Bigger system example:**
**AppImage / PortableApps:** Applications that bundle everything they need into a single file that runs without installation, respecting the user's environment.

-----

## 74\. The "Hello World" Latency (Instant Start)

**In two.lua:**

```lua
-- Startup time is dominated by parsing the source code. 
-- No heavy VM initialization, no container spin-up.
-- Run time < 0.01s for help.
```

Control feels like **friction** if it is slow. CLI tools must start instantly. If the user hesitates to run the command because of the startup time, the tool is too heavy.

**Python example:**

```python
# Bad: import pandas as pd (Takes 0.5s - 1.5s just to load)
# Good: import csv (Instant)
```

**Bigger system example:**
**Ripgrep (rg) vs Grep:** Ripgrep is preferred by many developers not just because it searches faster, but because it *starts* instantly and respects `.gitignore` by default, reducing friction.

-----

## 75\. Transparency (No Magic Black Boxes)

**In two.lua:**

```lua
-- The model isn't a binary blob. It's a readable table of centroids.
-- You can print(DATA.stats) and read the logic with human eyes.
```

You cannot "own" what you cannot read. Binary formats, pickled objects, and compiled black boxes prevent you from fixing problems when the original author disappears.

**Python example:**

```python
# Bad: Pickle (Python object serialization). It is opaque and dangerous.
# Good: JSON. It is verbose, but you can debug it with 'cat'.
```

**Bigger system example:**
**Unix /proc file system:** Linux exposes kernel internals as text files. You don't need a special API to see CPU info; you just `cat /proc/cpuinfo`.



# Anti Patterns

### Found in two.lua

Based on the code in `two.lua`, here are common software engineering anti-patterns present in the file:

  * **Magic Numbers:** Hardcoded constants like `1.7`, `1e-32`, and `6.28` appear directly in mathematical formulas without explanation.
  * **Cryptic Naming:** Widespread use of single-letter variables (`i`, `v`, `c`, `t`) reduces readability for outsiders.
  * **God Class:** The `DATA` class mixes multiple responsibilities: file I/O, data storage, statistical summarization, and machine learning logic.
  * **Reinventing the Wheel:** Manual implementation of CSV parsing and CLI argument parsing instead of using standard libraries.
  * **Global Mutable State:** The global `the` table controls application behavior and is mutable from anywhere.
  * **Command-Query Separation Violation:** The `add` function modifies the object's state *and* returns the value added, blurring the line between action and query.
  * **Implicit Type Coercion:** The `coerce` function silently converts strings to numbers or booleans based on regex matching, which can hide type errors.
  * **Shotgun Surgery:** The `add` function contains conditional logic for `NUM`, `SYM`, and `DATA`, meaning a change to "adding" logic requires editing one complex function.
  * **Stringly Typed:** Configuration defaults are parsed directly from a help string rather than being defined in a structured configuration object.
  * **Primitive Obsession:** Complex concepts like "Rows" or "Clusters" are treated as generic Lua tables rather than distinct data types.

### Complexity & Dependency Anti-Patterns (The "Modern Stack" Traps)

  * **Resume-Driven Development:** Choosing a complex technology (Kubernetes, React, Microservices) for a simple problem just to put it on your CV.
  * **Dependency Hell:** When your tool requires a library, which requires another library, which conflicts with the version of the library your OS uses.
  * **Supply Chain Suicide:** Referencing a package manager URL that you do not own. If the internet goes down, or the author deletes the repo (e.g., the "Left-Pad" incident), your build fails.
  * **Config Porn:** Having more lines of YAML/TOML configuration and CI/CD scripts than actual application logic.
  * **Container Obsession:** "It works on my machine because I shipped my machine." Using Docker to run a simple 50-line script is an admission of failure in portability.
  * **Friction Tolerance:** Accepting slow startup times, complex install procedures, or flaky builds as "normal" parts of the development process.

### Management & Process Anti-Patterns

  * **Death March:** A project destined to fail where the team is pressured to work unsustainable hours (nights/weekends) to meet an impossible deadline.
  * **Brooks’ Law:** Adding manpower to a late software project makes it later (due to ramp-up time and communication overhead).
  * **Gold Plating:** Continuing to work on a feature well past the point where the extra effort adds any value to the user.
  * **Feature Creep:** The continuous addition of new features that go beyond the original scope, preventing the project from ever finishing.
  * **Mushroom Management:** Keeping developers in the dark (about business goals) and feeding them fertilizer (misinformation).
  * **Smoke and Mirrors:** Creating a demo that looks like it works but is actually hardcoded or faked behind the scenes.
  * **Vendor Lock-In:** becoming so dependent on a vendor's proprietary technology that switching becomes prohibitively expensive.

### Architectural Anti-Patterns

  * **The Golden Hammer:** Assuming that a favorite technology (e.g., "Blockchain" or "AI") is the solution to every single problem.
  * **Boat Anchor:** Retaining a piece of code or library that is no longer used "just in case" we need it later.
  * **Lava Flow:** Old, poorly understood code that remains in the system because everyone is too afraid to delete it.
  * **Poltergeists:** Classes that have no real responsibility other than to call methods in other classes (often called `Manager` or `Controller`).
  * **Big Ball of Mud:** A system with no recognizable structure or architecture (the ultimate result of unchecked "Spaghetti Code").
  * **Stovepipe System:** Independent systems that cannot talk to each other, resulting in duplicate data entry.
  * **Swiss Army Knife:** A single component or interface designed to handle too many unrelated tasks (excessive complexity).

### Coding Anti-Patterns

  * **Soft Coding:** Moving so much logic into configuration files (DB-driven behavior) that the config file becomes a programming language itself.
  * **Action at a Distance:** When a change in one part of the program causes an unexpected error in a completely unrelated part.
  * **Blind Faith:** Calling a function (especially an API or system call) and assuming it works without checking the return value or catching errors.
  * **Object Orgy:** Failing to encapsulate data, allowing any part of the system to modify the internals of an object directly.
  * **Yo-Yo Problem:** A class hierarchy so deep that you have to bounce up and down (yo-yo) between definitions to understand the code.
  * **Copy-Paste Programming:** Duplicating code blocks instead of creating a reusable function (violates DRY).
