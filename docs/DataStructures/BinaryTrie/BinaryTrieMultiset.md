_____

# [`BinaryTrieMultiset.py`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BinaryTrie/BinaryTrieMultiset.py)

`BinaryTrieMultiset` です。0以上u未満の正整数からなる**多重**集合を管理できます。

空間 `O((要素数)logu)` のはずです。

____

## 仕様

#### `bt = BinaryTrieMultiset(u: int, a: Iterable[int]=[])`
- `a` から、**0 以上 u 未満**の正整数を管理する `BinaryTrieMultiset` を構築します。
- `O(nlogu)` です。

#### `bt.reserve(n: int) -> None`
- 内部のメモリを `O(n)` だけ確保します。
- `O(n)` です。

#### `bt.add(key: int, cnt: int=1) -> None`
- `key` を `cnt` 個追加します。
- `cnt` の値に依らず、 `O(logu)` です。

#### `bt.discard(key: int, cnt: int=1) -> bool`
- `key` が存在するなら `key` を `min(cnt, keyの個数)` 個削除し `True` を返します。そうでないなら何もせず `False` を返します。
- `O(logu)` です。

#### `bt.conut(key: int) -> int`
- `key` の個数を返します。
- `O(logu)` です。

#### `bt.pop(k: int=-1) / .pop_max() / .pop_min() -> int`
- (最大(昇順 `k` 番目) / 最大 / 最小) の値を削除し、その値を返します。
- `O(logu)` です。

#### `bt.get_max() / .get_min() -> int`
- (最大 / 最小) の値を返します。
- `O(logu)` です。

#### `bt.all_xor(x: int) -> None`
- すべての要素に `x` で `xor` をかけます。
- `O(1)` です。

#### `bt.index(key: int) / .index_right(key: int) -> int`
- `key` (より小さい / 以下の) 要素の数を返します。
- `O(logu)` です。

#### `bt.le(key: int) / .lt(key) / .ge(key) / gt(key) -> Optional[int]`
- `key` (以下の / より小さい / 以上の / より大きい) 値で (最大 / 最大 / 最小 / 最小) の値を返します。存在しなければ `None` を返します。
- `O(logu)` です。

#### `bt.tolist() -> List[int]`
- `key` を昇順に並べたリストを返します。
- `O(Nlogu)` です。

#### `key: int in bt`
- 存在判定です。
- `O(logu)` です。

#### `bt[k: int] -> int`
- 昇順 `k` 番目の値を返します
- `O(logu)` です。

#### `bool(bt) / iter(bt) / next(bt) / len(bt)`
- よしなです。

#### `str(bt) / repr(bt)`
- よしなです。

## 使用例

```python
q = int(input())
bt = BinaryTrieMultiset(1<<30)  # 0 以上 1<<30 未満の整数を管理する多重集合 bt を定義
bt.reserve(q)
for _ in range(q):
  t, x = map(int, input().split())
  if t == 0:
    bt.add(x)  # x を追加する
  elif t == 1:
    bt.discard(x)  # x を削除する
  else:
    # 全体に x を xor した時の最小値を出力する 
    bt.all_xor(x)
    print(bt[0])
    bt.all_xor(x)
```
