# VC_valuation_comparison

VC投資の比較分析のために、IPO前後の主要指標を時系列で揃え、企業間比較を可視化するための最小構成です。

## 定義済みの指標と期間軸

- 指標: 売上、純利益、営業利益、時価総額、TAM/SAM/SOM
- 期間軸: IPO年を0として、IPO前3年〜IPO後2年（`-3`〜`2`）をデフォルトで定義

指標定義は `analytics/metrics.py` に集約しています。

## 使い方

1. 集計データの生成

```bash
python analytics/aggregate.py
```

2. 比較ビューの表示

```bash
python -m http.server 8000 --directory ui
```

ブラウザで `http://localhost:8000` を開くと、グラフ・テーブル・フィルタ付きの比較ビューが表示されます。

## ディレクトリ構成

- `analytics/` : 指標定義と集計ロジック（CSV/JSON出力）
- `ui/` : ダッシュボードUI（グラフ/テーブル/フィルタ/情報ソース）
