# リポジトリと Paper 1 の対応表

この文書は、Paper 1 の原稿要素と `fuzzy-membership-kit` ハブリポジトリ内の成果物を対応づける。著者が主張を追跡しやすくし、査読者が実装・テスト・再現性メタデータを確認しやすくすることを目的とする。これは原稿そのものではなく、論文固有のデータセットも含まない。

| 論文章節 | 主張・定義・結果 | リポジトリ成果物 | テストまたは検証 | 再現出力 | 査読者向け確認点 |
| --- | --- | --- | --- | --- | --- |
| 古典的メンバーシップ関数 | 三角型、台形型、Gaussian、S/Z/pi、sigmoid-composed S/Z/pi の基準関数 | `src/fuzzymf/core.py`; `docs/theory.md`; `docs/theory_ja.md` | `tests/test_core.py`; 設定ファイル利用は `tests/test_io.py` | `examples/configs/` の既存例; `fuzzymf-plot` による任意の図 | 定義、領域・範囲、連続性の説明、期待される形状を確認する。 |
| フォーカス-aware ワーピング枠組み | 合成式 `mu(u)=h(w_theta(u))` | `src/fuzzymf/focus.py`; `docs/warping_framework.md`; `docs/warping_framework_ja.md` | `tests/test_focus.py` | `scripts/reproduce_paper1_diagnostics.py` の membership 行 | 合成挙動と、`w(far)=q` と `mu(far)=h(q)` の区別を確認する。 |
| ワーピング族 | logistic、tanh、arctan、Gompertz、generalized logistic | `src/fuzzymf/warping.py` | `tests/test_warping.py` | Paper 1 診断 CSV の warp 行 | `w(focus)=0.5`、`w(far)=q`、単調性、有限値、範囲を確認する。 |
| アンカー解法 | `focus`、`far`、ワープ後座標目標 `q` からの意味的アンカーによるパラメータ決定 | `src/fuzzymf/anchors.py` | `tests/test_anchors.py` | ワーピング診断スクリプト内で利用 | 任意調整ではなく、宣言された意味的アンカーからパラメータが決まることを確認する。 |
| 診断指標 | 範囲、単調性、局所識別性、尾部圧縮、傾き、曲率、アンカー誤差 | `src/fuzzymf/diagnostics.py`; `docs/diagnostics.md`; `docs/diagnostics_ja.md` | `tests/test_diagnostics.py` | `scripts/reproduce_paper1_diagnostics.py` による診断 CSV | 指標が設計目標に対応し、warp の目標と membership の目標を区別していることを確認する。 |
| Paper 1 再現例 | `focus=50`、`far=210`、`q=0.9` によるワーピング族比較と診断デモ | `examples/configs/paper1_warping_comparison.yaml`; `scripts/reproduce_paper1_diagnostics.py` | スクリプトの smoke run; 標準 pytest/ruff チェック | 既定では `results/csv/` の CSV; matplotlib があれば `results/figures/` の任意図 | 外部データなしに CSV を再生成でき、`warp` と `membership` の両方の行があることを確認する。 |
| 再現性メタデータ | 成果物の利用可能性、パッケージ版、ファイル単位チェックサム | `MANIFEST.json`; `scripts/generate_manifest.py`; `pyproject.toml`; `CITATION.cff` | manifest generator とチェックサム確認; パッケージチェック | commit-friendly な `MANIFEST.json` は既定で一時的な Git 状態を含まない | パッケージ版、依存関係メタデータ、ファイルチェックサム、引用メタデータを確認する。 |
| 文書の分離 | 理論、実装、診断、査読者向けメモを将来の論文原稿から分離 | `docs/theory*.md`; `docs/implementation*.md`; `docs/warping_framework*.md`; `docs/diagnostics*.md`; `docs/reviewer_notes.md` | 文書整合性の目視確認; 任意の MkDocs build | `mkdocs build` によるローカルサイト | このリポジトリに原稿を追加せず、数式・コード利用・再現性主張を追跡できることを確認する。 |

## 将来の Paper 1 リポジトリへのメモ

将来の Paper 1 spoke リポジトリでは、このパッケージのバージョンとコミットまたはリリース成果物を引用し、原稿ファイル、論文固有の図、実験出力はこのハブリポジトリの外に置く。Paper 2 の人間較正と Paper 3 の interval-valued/type-2 拡張は Paper 1 の範囲外に保つ。
