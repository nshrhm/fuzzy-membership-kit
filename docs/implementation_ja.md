# 実装ガイド

## 1. 設計方針

このリポジトリは、次の方針で設計する。

1. **数式との対応を明確にする。** 実装された各関数は、`docs/theory_ja.md` の数式と対応する。
2. **ハードコーディングを避ける。** 実験では、メンバーシップ関数のパラメータをスクリプト内に埋め込まず、JSON/YAML の設定ファイルに保存する。
3. **Python から使いやすくする。** スカラー、リスト、NumPy 配列を受け取れるようにする。
4. **査読者・追試者が確認しやすくする。** 論文では、利用した設定ファイルとパッケージ版を明示する。

## 2. ディレクトリ構成

```text
src/fuzzymf/core.py          # メンバーシップ関数と設定仕様
src/fuzzymf/io.py            # JSON/YAML の読み書き
src/fuzzymf/validation.py    # 範囲・単調性の簡易検査
src/fuzzymf/cli/plot.py      # 設定ファイルから図を描く CLI
examples/configs/            # 設定例
tests/                       # 単体テスト
```

## 3. 関数名

| 関数名 | 意味 |
| --- | --- |
| `triangular` | 三角型 |
| `trapezoid_rising` | 増加型台形肩関数 |
| `trapezoid_falling` | 減少型台形肩関数 |
| `trapezoid_pi` | 台形型の中央概念 |
| `gaussian` | ピーク値 1 のガウス型 |
| `s_curve` | Zadeh 型の 2 次 S 関数 |
| `z_curve` | S 関数の補関数 |
| `pi_curve` | S と Z を組み合わせた滑らかな pi 関数 |
| `sigmoid` | ロジスティック変換 |
| `compressed_s` | シグモイド合成 S 関数 |
| `compressed_z` | シグモイド合成 Z 関数 |
| `compressed_pi` | 二側型のシグモイド合成 pi 関数 |

## 4. 設定ファイル形式

設定ファイルは、任意の `universe`、任意の `metadata`、必須の `memberships` を持つ。

```yaml
universe:
  name: Visual analogue scale
  symbol: u
  min: 0
  max: 100
metadata:
  paper: example
  version: 0.1.0
memberships:
  - name: high
    kind: compressed_s
    params:
      focus: 50
      far: 90
      upper_q: 0.9
```

各 `memberships` 要素は次を持つ。

- `name`: 下流の分析で使う安定した識別子。
- `kind`: 登録済み関数名。
- `params`: 関数に渡すパラメータ。
- `description`: 任意の説明。

## 5. 論文用マニフェストで残す項目

論文投稿用には、少なくとも次を残す。

```text
package_name
package_version
repository_commit
membership_config_path
membership_config_sha256
universe_definition
semantic_anchor_policy
parameter_selection_policy
score_input_files
score_output_files
```

これにより、メンバーシップ関数の数学的定義、採用したパラメータ、適用したデータを分離して説明できる。

## 6. 検査

`validation.range_report` で出力が \([0,1]\) に収まるかを確認できる。`validation.monotonicity_report` で、増加型または減少型として意図した単調性を数値的に確認できる。

```python
import numpy as np
from fuzzymf import compressed_s
from fuzzymf.validation import range_report, monotonicity_report

grid = np.linspace(0, 100, 1001)
func = lambda u: compressed_s(u, focus=50, far=90)

print(range_report(func, grid))
print(monotonicity_report(func, grid, direction="increasing"))
```

これは形式的証明ではなく、実装された設定が意図どおりに振る舞うかを確認するための数値的な健全性検査である。

## 7. 新しい関数を追加する手順

1. `src/fuzzymf/core.py` に関数を追加する。
2. `FUNCTIONS` レジストリに名前と関数を登録する。
3. `docs/theory.md` と `docs/theory_ja.md` に数式を追加する。
4. `tests/` に少なくとも 1 つ単体テストを追加する。
5. 公開再利用を想定する場合は、`examples/configs/` に設定例を追加する。
