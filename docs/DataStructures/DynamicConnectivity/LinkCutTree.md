_____

# [LinkCutTree.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/DynamicConnectivity/LinkCutTree.py)

最終更新: 2023/06/16
- メソッド名を少し変更しました
- `path_length()` メソッドを追加しました。
- assertionエラーを追加しました。

`LinkCutTree` です。森を管理します。パスクエリの強さに定評があります。

_____

## 仕様

#### `lct = LinkCutTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None, id: F=None)`
- `n_or_a`が `int` のとき、頂点数 `n` の `LinkCutTree` を構築します。`Iterable` のとき、頂点数はその長さとなります。`op, mapping, composition, e, id` は遅延セグ木のアレです。よしなに。

#### `lct.expose(v: int) -> int`
- `v` が属する木において、その木を管理しているsplay木の根からvまでのパスを作ります。

#### `lct.evert(v: int) -> None`
- `v` を根にします。
- `O(logN)` です。

#### `lct.link(c: int, p: int) -> None`
- 辺 `{c, p}` を追加します。
- `O(logN)` です。

#### `lct.cut(c: int) -> None`

#### `lct.group_count() -> int`

#### `lct.root(v: int) -> int`

#### `lct.lca(u: int, v: int) -> int`

#### `lct.same(u: int, v: int) -> bool`

#### `lct.merge(u: int, v: int) -> bool`

#### `lct.split(u: int, v: int) -> bool`

#### `lct.path_prod(u: int, v: int) -> T`

#### `lct.path_apply(u: int, v: int) -> None`

#### `lct.path_length(u: int, v: int) -> int`

#### `lct.path_kth_elm(s: int, t: int, k: int)`
- `s-t` パスの頂点列を $v_{0}, v_{1}, ..., v_{n}$ としたときの $v_{k}$ を返します。 $k > n$ のとき、 `None` を返します。
- `O(logN)` です。

#### `lct[k] / lct[k] = v`

#### `str(lct) / repr(lct)`
