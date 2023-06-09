from typing import Generic, TypeVar, Callable, List, Dict, Optional
T = TypeVar('T')

class DynamicSegmentTree(Generic[T]):

  def __init__(self, u: int, op: Callable[[T, T], T], e: T):
    '''Build a new DynamicSegmentTree. / O(1)'''
    self._op = op
    self._e = e
    self._u = u
    self._log  = (self._u-1).bit_length()
    self._size = 1 << self._log
    self._data: Dict[int, T] = {}

  def set(self, k: int, v: T) -> None:
    '''Update a[k] <- x. / O(logU)'''
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.set({k}: int, {v}: T), n={self._u}'
    if k < 0: k += self._u
    k += self._size
    self._data[k] = v
    e = self._e
    for _ in range(self._log):
      k >>= 1
      self._data[k] = self._op(self._data.get(k<<1, e), self._data.get(k<<1|1, e))

  def get(self, k: int) -> T:
    '''Return a[k]. / O(1)'''
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.get({k}: int), n={self._u}'
    if k < 0: k += self._u
    return self._data.get(k+self._size, self._e)

  def prod(self, l: int, r: int) -> T:
    '''Return op([l, r)). / O(logU)'''
    assert 0 <= l <= r <= self._u, \
        f'IndexError: DynamicSegmentTree.prod({l}: int, {r}: int)'
    l += self._size
    r += self._size
    e = self._e
    lres = e
    rres = e
    while l < r:
      if l & 1:
        lres = self._op(lres, self._data.get(l, e))
        l += 1
      if r & 1:
        rres = self._op(self._data.get(r^1, e), rres)
      l >>= 1
      r >>= 1
    return self._op(lres, rres)

  def all_prod(self) -> T:
    '''Return op([0, n)). / O(1)'''
    return self._data[1]

  def max_right(self, l: int, f: Callable[[T], bool]) -> int:
    '''Find the largest index R s.t. f([l, R)) == True. / O(logU)'''
    assert 0 <= l <= self._u, \
        f'IndexError: DynamicSegmentTree.max_right({l}, f) index out of range'
    assert f(self._e), \
        f'DynamicSegmentTree.max_right({l}, f), f({self._e}) must be true.'
    if l == self._u:
      return self._u 
    l += self._size
    e = self._e
    s = e
    while True:
      while l & 1 == 0:
        l >>= 1
      if not f(self._op(s, self._data.get(l, e))):
        while l < self._size:
          l <<= 1
          if f(self._op(s, self._data.get(l, e))):
            s = self._op(s, self._data.get(l, e))
            l |= 1
        return l - self._size
      s = self._op(s, self._data.get(l, e))
      l += 1
      if l & -l == l:
        break
    return self._u

  def min_left(self, r: int, f: Callable[[T], bool]) -> int:
    '''Find the smallest index L s.t. f([L, r)) == True. / O(logU)'''
    assert 0 <= r <= self._u, \
        f'IndexError: DynamicSegmentTree.min_left({r}, f) index out of range'
    assert f(self._e), \
        f'DynamicSegmentTree.min_left({r}, f), f({self._e}) must be true.'
    if r == 0:
      return 0 
    r += self._size
    e = self._e
    s = e
    while True:
      r -= 1
      while r > 1 and r & 1:
        r >>= 1
      if not f(self._op(self._data.get(r, e), s)):
        while r < self._size:
          r = r << 1 | 1
          if f(self._op(self._data.get(r, e), s)):
            s = self._op(self._data.get(r, e), s)
            r ^= 1
        return r + 1 - self._size
      s = self._op(self._data.get(r, e), s)
      if r & -r == r:
        break 
    return 0

  def tolist(self) -> List[T]:
    '''Return List[self]. / O(NlogN)'''
    return [self.get(i) for i in range(self._u)]

  def __getitem__(self, k: int) -> T:
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.__getitem__({k}: int), n={self._u}'
    return self.get(k)

  def __setitem__(self, k: int, v: T) -> None:
    assert -self._u <= k < self._u, \
        f'IndexError: DynamicSegmentTree.__setitem__{k}: int, {v}: T), n={self._u}'
    self.set(k, v)

  def __str__(self) -> str:
    return str(self.tolist())

  def __repr__(self) -> str:
    return f'DynamicSegmentTree({self})'


def op(s, t):
  return
 
e = None

