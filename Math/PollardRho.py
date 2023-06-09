from functools import lru_cache
from collections import Counter
import math

class PollardRho():
  # 高速素因数分解

  L = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
  S = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}

  @classmethod
  def factorization(cls, n: int) -> Counter:
    todo = [n]
    res = Counter()
    while todo:
      v = todo.pop()
      if v <= 1: continue
      f = cls._pollard_rho(v)
      if f == v:
        res[v] += 1
      else:
        todo.append(f)
        todo.append(v//f)
    return res

  @staticmethod
  @lru_cache(maxsize=None)
  def _pollard_rho(n: int) -> int:
    if n & 1 == 0: return 2
    if n % 3 == 0: return 3
    s = ((n-1) & (1-n)).bit_length() - 1
    d = n >> s
    for a in PollardRho.L:
      p = pow(a, d, n)
      if p == 1 or p == n-1 or a%n == 0:
        continue
      for _ in range(s):
        prev = p
        p = (p*p) % n
        if p == 1:
          return math.gcd(prev-1, n)
        if p == n-1:
          break
      else:
        for i in range(2, n):
          x = i
          y = (i*i+1)%n
          f = math.gcd(abs(x-y), n)
          while f == 1:
            x = (x*x+1) % n
            y = (y*y+1) % n
            y = (y*y+1) % n
            f = math.gcd(abs(x-y), n)
          if f != n:
            return f
    return n

