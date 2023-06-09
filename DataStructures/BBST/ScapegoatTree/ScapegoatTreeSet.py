import math
from typing import List, TypeVar, Generic, Iterable, Tuple, Optional
T = TypeVar('T')

class ScapegoatTreeSet(Generic[T]):

  alpha = 0.75
  beta = math.log2(1 / alpha)

  class Node:

    def __init__(self, key: T):
      self.key = key
      self.left = None
      self.right = None
      self.size = 1

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.size}\n'
      return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):
    self.node = None
    if not (hasattr(a, '__getitem__') and hasattr(a, '__len__')):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> 'Node':
      mid = (l + r) >> 1
      node = Node(a[mid])
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
      return node
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    Node = ScapegoatTreeSet.Node
    self.node = sort(0, len(a))

  def _rebuild(self, node: Node) -> Node:
    def get(node: 'ScapegoatTreeSet.Node') -> None:
      if node.left is not None:
        get(node.left)
      a.append(node)
      if node.right is not None:
        get(node.right)
    def sort(l: int, r: int) -> Tuple['ScapegoatTreeSet.Node', int]:
      mid = (l + r) >> 1
      node = a[mid]
      node.size = 1
      if l != mid:
        node.left = sort(l, mid)
        node.size += node.left.size
      else:
        node.left = None
      if mid+1 != r:
        node.right = sort(mid+1, r)
        node.size += node.right.size
      else:
        node.right = None
      return node
    a = []
    get(node)
    return sort(0, len(a))

  def add(self, key: T) -> bool:
    Node = ScapegoatTreeSet.Node
    node = self.node
    if node is None:
      self.node = Node(key)
      return True
    path = []
    while node is not None:
      path.append(node)
      if key == node.key:
        return False
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    if key < path[-1].key:
      path[-1].left = Node(key)
    else:
      path[-1].right = Node(key)
    if len(path)*ScapegoatTreeSet.beta > math.log(self.node.size):
      node_size = 1
      while path:
        pnode = path.pop()
        pnode_size = pnode.size + 1
        if ScapegoatTreeSet.alpha * pnode_size < node_size:
          break
        node_size = pnode_size
      new_node = self._rebuild(pnode)
      if not path:
        self.node = new_node
        return True
      if new_node.key < path[-1].key:
        path[-1].left = new_node
      else:
        path[-1].right = new_node
    for p in path:
      p.size += 1
    return True

  def discard(self, key: T) -> bool:
    di = 1
    node = self.node
    path = []
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        di = 1
        node = node.left
      else:
        path.append(node)
        di = 0
        node = node.right
    else:
      return False
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else 0
      while lmax.right is not None:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
    for p in path:
      p.size -= 1
    return True

  def le(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def lt(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def ge(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def gt(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def index(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def index_right(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        k += 1 if node.left is None else node.left.size + 1
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def pop(self, k: int=-1) -> T:
    if k < 0: k += self.node.size
    di = 1
    node = self.node
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        break
      elif t < k:
        path.append(node)
        node = node.right
        k -= t + 1
        di = 0
      elif t > k:
        path.append(node)
        di = 1
        node = node.left
    res = node.key
    if node.left is not None and node.right is not None:
      path.append(node)
      lmax = node.left
      di = 1 if lmax.right is None else 0
      while lmax.right is not None:
        path.append(lmax)
        lmax = lmax.right
      node.key = lmax.key
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di == 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
    for p in path:
      p.size -= 1
    return res

  def pop_min(self) -> T:
    return self.pop(0)

  def claer(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def get_max(self) -> T:
    return self.__getitem__(-1)

  def get_min(self) -> T:
    return self.__getitem__(0)

  def pop_max(self) -> T:
    return self.pop()

  def __contains__(self, key: T):
    node = self.node
    while node is not None:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __getitem__(self, k: int) -> T:
    if k < 0: k += self.__len__()
    node = self.node
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'ScapegoatTreeSet(' + str(self) + ')'

