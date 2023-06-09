from typing import List, Callable
from collections import defaultdict

class OfflineDynamicConnectivity():

  class UndoableUnionFind():

    def __init__(self, n: int):
      self._n = n
      self._parents = [-1] * n
      self._all_sum = [0] * n
      self._one_sum = [0] * n
      self._history = []
      self._group_count = n

    def undo(self) -> None:
      assert self._history, f'UndoableUnionFind.undo() with non history'
      y, py, one_sum_y, all_sum_y = self._history.pop()
      x, px, one_sum_x, all_sum_x = self._history.pop()
      if y == -1:
        return
      self._group_count += 1
      self._parents[y] = py
      self._parents[x] = px
      s = (self._all_sum[x] - all_sum_y - all_sum_x) // (-px-py)
      self._all_sum[y] += s * -py
      self._all_sum[x] -= all_sum_y + s * -py
      self._one_sum[x] -= self._one_sum[y]

    def root(self, x: int) -> int:
      while self._parents[x] >= 0:
        x = self._parents[x]
      return x

    def unite(self, x: int, y: int) -> bool:
      x = self.root(x)
      y = self.root(y)
      if x == y:
        self._history.append((-1, -1, -1, -1))
        self._history.append((-1, -1, -1, -1))
        return False
      if self._parents[x] > self._parents[y]:
        x, y = y, x
      self._group_count -= 1
      self._history.append((x, self._parents[x], self._one_sum[x], self._all_sum[x]))
      self._history.append((y, self._parents[y], self._one_sum[y], self._all_sum[y]))
      self._all_sum[x] += self._all_sum[y]
      self._one_sum[x] += self._one_sum[y]
      self._parents[x] += self._parents[y]
      self._parents[y] = x
      return True

    def size(self, x: int) -> int:
      return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
      return self.root(x) == self.root(y)

    def add(self, x: int, v: int) -> None:
      while x >= 0:
        self._one_sum[x] += v
        x = self._parents[x]

    def add_group(self, x: int, v: int) -> None:
      x = self.root(x)
      self._all_sum[x] += v * self.size(x)

    def group_count(self) -> int:
      return self._group_count

    def group_sum(self, x: int) -> int:
      x = self.root(x)
      return self._one_sum[x] + self._all_sum[x]

    def all_group_members(self) -> defaultdict:
      group_members = defaultdict(list)
      for member in range(self._n):
        group_members[self.root(member)].append(member)
      return group_members

    def __str__(self) -> str:
      return '<offline-dc.uf> [\n' + '\n'.join(f'  {k}: {v}' for k, v in self.all_group_members().items()) + '\n]'


  def __init__(self, n: int, q: int):
    self.n = n
    self.q = q
    self.bit = n.bit_length() + 1
    self.msk = (1 << self.bit) - 1
    self.query_count = 0
    self.log  = (self.q - 1).bit_length()
    self.size = 1 << self.log
    self.data = [[] for _ in range(self.size<<1)]
    self.edge = defaultdict(list)
    self.uf = OfflineDynamicConnectivity.UndoableUnionFind(n)

  def add_edge(self, u: int, v: int) -> None:
    assert 0 <= u < self.n and 0 <= v < self.n
    if u > v:
      u, v = v, u
    self.edge[u<<self.bit|v].append(self.query_count<<1)
    self.query_count += 1

  def delete_edge(self, u: int, v: int) -> None:
    assert 0 <= u < self.n and 0 <= v < self.n
    if u > v:
      u, v = v, u
    self.edge[u<<self.bit|v].append(self.query_count<<1|1)
    self.query_count += 1

  def add_relax(self) -> None:
    self.query_count += 1

  def run(self, out: Callable[[int], None]) -> None:
    # O(qlogqlogn)
    assert self.query_count == self.q, \
        f'query_count=({self.query_count}) is not equal to q=({self.q})'
    data, uf, bit, msk, size, q = self.data, self.uf, self.bit, self.msk, self.size, self.q
    size2 = size * 2
    for k, v in self.edge.items():
      LR = []
      i = 0
      cnt = 0
      while i < len(v):
        if v[i] & 1 == 0:
          cnt += 1
        if cnt > 0:
          LR.append(v[i]>>1)
          i += 1
          while i < len(v) and cnt > 0:
            if v[i] & 1 == 0:
              cnt += 1
            else:
              # assert cnt >= 0
              cnt -= 1
              if cnt == 0:
                LR.append(v[i]>>1)
            i += 1
          i -= 1
        i += 1
      if cnt > 0:
        LR.append(q)
      LR.reverse()
      while LR:
        l = LR.pop() + size
        r = LR.pop() + size
        while l < r:
          if l & 1:
            data[l].append(k)
            l += 1
          if r & 1:
            data[r^1].append(k)
          l >>= 1
          r >>= 1
    todo = [1]
    while todo:
      v = todo.pop()
      if v >= 0:
        for uv in data[v]:
          uf.unite(uv>>bit, uv&msk)
        todo.append(~v)
        if v<<1|1 < size2:
          todo.append(v<<1|1)
          todo.append(v<<1)
        elif v - size < q:
          out(v-size)
      else:
        for _ in data[~v]:
          uf.undo()

  def __repr__(self):
    return f'OfflineDynamicConnectivity({self.n}, {self.q})'

