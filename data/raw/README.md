# Raw Data Directory

This folder contains the original, unmodified source files downloaded from Kaggle.

## Dataset Source

**Kaggle**: [DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

---

## Files in This Directory

| File | Description | Size |
|---|---|---|
| `DataCoSupplyChainDataset.csv` | Primary raw dataset — 180,519 order-item rows, 53 columns. **Do not modify.** | ~91 MB |
| `DescriptionDataCoSupplyChain.csv` | Column descriptions and field metadata provided with the Kaggle dataset | ~3 KB |

---

## Raw Data Rules

> [!CAUTION]
> **DO NOT modify, delete, or overwrite any file in this directory.**
> These files are the immutable source of truth. All transformations happen in the `data/cleaned/` and `data/processed/` directories.

1. **Read-Only**: All pipeline scripts read from this directory but never write to it.
2. **No Synthetic Data**: These files must only contain the original Kaggle dataset. No synthetic rows may be added.
3. **Reproducibility**: Retaining the original raw file ensures that any future pipeline run can be reproduced from scratch.

---

## How the Raw Data Is Used

```
data/raw/DataCoSupplyChainDataset.csv
         │
         └── python/01_data_profiling.py  → (read-only profiling)
         └── python/02_data_cleaning.py   → output: data/cleaned/dataco_cleaned.csv
```

All downstream files (`data/cleaned/`, `data/processed/`) are derived entirely from the raw Kaggle CSV above.
