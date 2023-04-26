from typing import Optional, List, Iterable, Sequence
from array import array
from __pypy__ import newlist_hint

class BinaryTrieSet():

  def __init__(self, u: int, a: Iterable[int]=[]):
    self.left = array('I', bytes(8))
    self.right = array('I', bytes(8))
    self.par = array('I', bytes(8))
    self.size = array('I', bytes(8))
    self.end = 2
    self.root = 1
    self.bit = (u - 1).bit_length()
    self.lim = 1 << self.bit
    self.xor = 0
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[int]) -> None:
    left, right, par, size = self.left, self.right, self.par, self.size
    def rec(node: int, d: int, l: int, r: int) -> None:
      k, ng = r, l-1
      while k - ng > 1:
        mid = (k + ng) >> 1
        if a[mid] >> d & 1:
          k = mid
        else:
          ng = mid
      if l != k:
        lnode = self._make_node()
        left[node] = lnode
        par[lnode] = node
        size[lnode] = k - l
        if d: rec(lnode, d - 1, l, k)
      if k != r:
        rnode = self._make_node()
        right[node] = rnode
        par[rnode] = node
        size[rnode] = r - k
        if d: rec(rnode, d - 1, k, r)
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    assert 0 <= a[0] and a[-1] < self.lim, \
        f'ValueError: BinaryTrieSet._build({a}), lim={self.lim}'
    self.reserve(len(a))
    rec(self.root, self.bit-1, 0, len(a))
    size[self.root] = len(a)

  def _make_node(self) -> int:
    end = self.end
    if end >= len(self.left):
      self.left.append(0)
      self.right.append(0)
      self.par.append(0)
      self.size.append(0)
    self.end += 1
    return end

  def reserve(self, n: int) -> None:
    assert n >= 0, f'ValueError: BinaryTrieSet.reserve({n})'
    a = array('I', bytes(4*n))
    self.left += a
    self.right += a
    self.par += a
    self.size += a

  def add(self, key: int) -> bool:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.add({key}), lim={self.lim}'
    left, right, par, size = self.left, self.right, self.par, self.size
    key ^= self.xor
    node = self.root
    for i in range(self.bit-1, -1, -1):
      if key >> i & 1:
        left, right = right, left
      if not left[node]:
        left[node] = self._make_node()
        par[left[node]] = node
      node = left[node]
      if key >> i & 1:
        left, right = right, left
    if size[node]: return False
    size[node] = 1
    for i in range(self.bit):
      node = par[node]
      size[node] += 1
    return True

  def _discard(self, node: int) -> None:
    left, right, par, size = self.left, self.right, self.par, self.size
    for i in range(self.bit):
      size[node] -= 1
      if left[par[node]] == node:
        node = par[node]
        left[node] = 0
        if right[node]: break
      else:
        node = par[node]
        right[node] = 0
        if left[node]: break
    while node:
      size[node] -= 1
      node = par[node]

  def discard(self, key: int) -> bool:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.discard({key}), lim={self.lim}'
    left, right, par, size = self.left, self.right, self.par, self.size
    node = self.find(key)
    if not node: return False
    self._discard(node)
    return True

  def pop(self, k: int=-1) -> int:
    assert -len(self) <= k < len(self), \
        f'IndexError: BinaryTrieSet.pop({k}), len={len(self)}'
    if k < 0: k += len(self)
    left, right, size = self.left, self.right, self.size
    node = self.root
    res = 0
    for i in range(self.bit-1, -1, -1):
      b = self.xor >> i & 1
      if b:
        left, right = right, left
      t = size[left[node]]
      res <<= 1
      if not left[node]:
        node = right[node]
        res |= 1
      elif not right[node]:
        node = left[node]
      else:
        t = size[left[node]]
        if t <= k:
          k -= t
          res |= 1
          node = right[node]
        else:
          node = left[node]
      if b:
        left, right = right, left
    self._discard(node)
    return res ^ self.xor

  def pop_min(self) -> int:
    assert self, f'IndexError: BinaryTrieSet.pop_min(), len={len(self)}'
    return self.pop(0)

  def find(self, key: int) -> Optional[int]:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.find({key}), lim={self.lim}'
    left, right = self.left, self.right
    key ^= self.xor
    node = self.root
    for i in range(self.bit-1, -1, -1):
      if key >> i & 1:
        left, right = right, left
      if not left[node]: return None
      node = left[node]
      if key >> i & 1:
        left, right = right, left
    return node

  def all_xor(self, x: int) -> None:
    assert 0 <= x < self.lim, \
        f'ValueError: BinaryTrieSet.all_xor({x}), lim={self.lim}'
    self.xor ^= x

  def get_min(self) -> int:
    assert self, f'IndexError: BinaryTrieSet.get_min()'
    left, right = self.left, self.right
    key = self.xor
    ans = 0
    node = self.root
    for i in range(self.bit-1, -1, -1):
      ans <<= 1
      if key >> i & 1:
        if right[node]:
          node = right[node]
          ans |= 1
        else:
          node = left[node]
      else:
        if left[node]:
          node = left[node]
        else:
          node = right[node]
          ans |= 1
    return ans ^ self.xor

  def get_max(self) -> int:
    assert self, f'IndexError: BinaryTrieSet.get_max()'
    left, right = self.left, self.right
    key = self.xor
    ans = 0
    node = self.root
    for i in range(self.bit-1, -1, -1):
      ans <<= 1
      if key >> i & 1:
        if left[node]:
          node = left[node]
        else:
          node = right[node]
          ans |= 1
      else:
        if right[node]:
          ans |= 1
          node = right[node]
        else:
          node = left[node]
    return ans ^ self.xor

  def pop_max(self) -> int:
    return self.pop()

  def index(self, key: int) -> int:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.index({key}), lim={self.lim}'
    left, right, size = self.left, self.right, self.size
    k, now = 0, 0
    node = self.root
    key ^= self.xor
    for i in range(self.bit-1, -1, -1):
      if key >> i & 1:
        k += size[left[node]]
        node = right[node]
      else:
        node = left[node]
      if not node: break
    return k

  def index_right(self, key: int) -> int:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.index_right({key}), lim={self.lim}'
    left, right, size = self.left, self.right, self.size
    k, now = 0, 0
    node = self.root
    key ^= self.xor
    for i in range(self.bit-1, -1, -1):
      if key >> i & 1:
        k += size[left[node]]
        node = right[node]
      else:
        node = left[node]
      if not node: break
    else:
      k += 1
    return k

  def gt(self, key: int) -> Optional[int]:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.gt({key}), lim={self.lim}'
    i = self.index_right(key)
    return None if i >= self.size[self.root] else self.__getitem__(i)

  def lt(self, key: int) -> Optional[int]:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.lt({key}), lim={self.lim}'
    i = self.index(key) - 1
    return None if i < 0 else self.__getitem__(i)

  def ge(self, key: int) -> Optional[int]:
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.ge({key}), lim={self.lim}'
    if key == 0: return self.get_min() if self else None
    i = self.index_right(key - 1)
    return None if i >= self.size[self.root] else self.__getitem__(i)

  def le(self, key: int):
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.le({key}), lim={self.lim}'
    i = self.index(key + 1) - 1
    return None if i < 0 else self.__getitem__(i)

  def tolist(self) -> List[int]:
    a = newlist_hint(len(self))
    if not self: return a
    val = self.get_min()
    while val is not None:
      a.append(val)
      val = self.gt(val)
    return a

  def __contains__(self, key: int):
    assert 0 <= key < self.lim, \
        f'ValueError: BinaryTrieSet.__contains__({key}), lim={self.lim}'
    return self.find(key) is not None

  def __getitem__(self, k: int):
    assert -len(self) <= k < len(self), \
        f'IndexError: BinaryTrieSet.__getitem__({k}), len={len(self)}'
    if k < 0: k += len(self)
    left, right, size = self.left, self.right, self.size
    node = self.root
    res = 0
    for i in range(self.bit - 1, -1, -1):
      b = self.xor >> i & 1
      if b:
        left, right = right, left
      t = size[left[node]]
      res <<= 1
      if not left[node]:
        node = right[node]
        res |= 1
      elif not right[node]:
        node = left[node]
      else:
        t = size[left[node]]
        if t <= k:
          k -= t
          res |= 1
          node = right[node]
        else:
          node = left[node]
      if b:
        left, right = right, left
    return res

  def __bool__(self):
    return self.size[self.root] != 0

  def __iter__(self):
    self.it = 0
    return self

  def __next__(self):
    if self.it == len(self):
      raise StopIteration
    self.it += 1
    return self.__getitem__(self.it - 1)

  def __len__(self):
    return self.size[self.root]

  def __str__(self):
    return '{' + ', '.join(map(str, self)) + '}'

  def __repr__(self):
    return f'BinaryTrieSet({(1<<self.bit)-1}, {self})'

