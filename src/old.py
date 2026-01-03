def peeking(data,rows):            # best if rows arrived shuffled
  d = clone(data, rows[:the.warm]) # all rows labelled by this function
  a,z = clone(data),clone(data)    # best, rest labelled rows
  x = lambda r: distx(d,r,mids(a)) - distx(d,r,mids(z)) # <0 if closest to best
  y = lambda r: disty(d,r) # distanace of goals to "heaven" (best values)
  d.rows.sorted(key=y)
  adds(d.rows[:the.warm//2], a)
  adds(d.rows[the.warm//2:], z)
  for r in rows[the.warm:]:
    if d.n >= the.budget: break
    elif x(r) < 0:
      add(d, add(a,r))
      if a.n > sqrt(d.n): # too many best things
        a.rows.sorted(key=y)
        add(z, sub(a, a.rows[-1])) # demote worse row in best to rest
  d.rows.sort(key=x)
  return obj(sorter=x, labelled=d)


