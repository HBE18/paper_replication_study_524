# CENG524 Paper Replication Study  
## Portfolio Optimization: LSTM vs. Random Forests

This repository contains the replication work for the CENG524 Advanced Machine Learning course project.

The selected paper is:

**Jinyuan Sun, “A Comparative Analysis of Portfolio Optimization: LSTM vs. Random Forests.”**

The goal of this project is to examine whether the methodology and results reported in the paper can be reproduced using the publicly released implementation and dataset artifacts.

## Original Work

Original implementation repository:

https://github.com/Jinyuan-S/portfolio_optimization

Original dataset reported by the paper:

https://www.kaggle.com/datasets/svaningelgem/nyse-100-daily-stock-prices/data

The original paper reports that it uses NYSE daily stock data and focuses on four healthcare and insurance-related stocks:

- LLY
- PGR
- CI
- UNH

The paper claims to compare:

- Long Short-Term Memory (LSTM)
- Random Forest
- Mean-Variance portfolio construction
- NASDAQ benchmark performance

## Repository Structure

```text
paper_replication_study_524/
├── archive/
│   ├── ABBV.csv
│   ├── ABT.csv
│   ├── ...
│   └── ...
├── 00_dataset_manifest.py
├── A Comparative Analysis of Portfolio Optimization-LSTM vs. Random Forests.pdf
├── app.ipynb
├── app_execution_as_released.ipynb
├── app_execution_as_released_controlled.ipynb
├── draw.ipynb
├── image-1.png
├── image.png
├── nasdaq31.csv
├── replication_dataset_manifest.csv
├── requirements.txt
├── sp500.csv
├── LICENSE
├── .gitignore
└── README.md
```

## File Descriptions

### `archive/`

Contains the fixed stock-level CSV files released with the original implementation. These files were used as the exact data artifacts for the replication instead of re-downloading data from Kaggle or using a live financial API.

### `00_dataset_manifest.py`

Script used to inspect and fingerprint the released CSV artifacts. It records file names, file sizes, SHA-256 hashes, row counts, column counts, and schema information.

### `A Comparative Analysis of Portfolio Optimization-LSTM vs. Random Forests.pdf`

The selected paper used as the reference study for this replication.

### `app.ipynb`

The original notebook from the released implementation.

### `app_execution_as_released.ipynb`

Execution copy of the original notebook. This notebook was used to test whether the released implementation reproduces its own saved outputs when run from a fresh kernel without methodological changes.

### `app_execution_as_released_controlled.ipynb`

Controlled deterministic version of the notebook. The same dataset, implemented models, and portfolio logic were preserved. Fixed random seeds were added to test whether result instability was caused by uncontrolled randomness.

### `draw.ipynb`

Additional notebook from the original repository. It was retained as part of the original project artifact set.

### `image.png` and `image-1.png`

Image files from the original repository. They were retained as part of the released artifact set.

### `nasdaq31.csv`

NASDAQ benchmark data used by the original notebook.

### `replication_dataset_manifest.csv`

Output of the dataset manifest script. It documents the available data artifacts used in the replication.

### `requirements.txt`

Lists the Python packages required to run the notebooks and replication scripts.

### `sp500.csv`

A root-level CSV artifact from the original repository. In this replication, this file was found to be empty. It was treated as a reproducibility warning, although it does not appear to be used by the main notebook pipeline.

### `LICENSE`

License file for the repository.

### `.gitignore`

Specifies files and folders that should not be tracked by Git, such as virtual environments, cache folders, notebook checkpoints, and temporary files.

### `README.md`

Project overview file for the GitHub repository.

## Replication Objective

The objective of this replication study is to check whether the paper's central claims can be verified from the released implementation and data artifacts.

The replication focuses on three questions:

1. Can the released notebook run successfully?
2. Can the released notebook reproduce stable numerical results across fresh-kernel executions?
3. Does the released implementation match the methodology described in the paper?

## Main Finding

The official released notebook does not implement an LSTM model.

Instead, it trains:

- `RandomForestRegressor`
- `DecisionTreeRegressor`

However, the generated outputs are later labeled as:

- “LSTM”
- “Random Forest”

This means that the released implementation does not verify the paper's central claim that LSTM outperforms Random Forest. The implementation compares Random Forest and Decision Tree, while the paper claims to compare LSTM and Random Forest.

## Additional Reproducibility Findings

Several additional discrepancies were found:

1. The paper states that `Adj Close` prices are used, but the released CSV files and notebook use the raw `close` column.
2. The paper describes covariance shrinkage, but the notebook uses ordinary sample covariance through `returns.cov()`.
3. The paper reports 1147 total market days and 1117 training days, while the notebook produces 1117 total rows and 1087 training rows after preprocessing.
4. The released notebook does not set random seeds.
5. Repeated fresh-kernel executions of the released notebook produce different portfolio returns.
6. After adding deterministic seeds, the implemented Random Forest and Decision Tree pipeline becomes reproducible, but it still does not reproduce the LSTM methodology claimed in the paper.

## Execution Results

### As-Released Repeated Runs

Repeated fresh-kernel executions of the released notebook produced stable NASDAQ benchmark results, but unstable model-based portfolio returns.

| Run | NASDAQ Return | RF Return | DT Return |
|---:|---:|---:|---:|
| Original saved notebook output | -0.0344847098 | 0.1581967765 | 0.1072814419 |
| Rerun 1 | -0.0344847098 | 0.1579421955 | 0.1727922072 |
| Rerun 2 | -0.0344847098 | 0.1508853359 | 0.1142518220 |
| Rerun 3 | -0.0344847098 | 0.1474317305 | 0.1345048082 |
| Rerun 4 | -0.0344847098 | 0.1470093299 | 0.1296921705 |

### Controlled Deterministic Runs

After adding fixed random seeds, repeated fresh-kernel executions produced identical results.

| Run | NASDAQ Return | RF Return | DT Return |
|---:|---:|---:|---:|
| Controlled run 1 | -0.0344847098 | 0.1492175467 | 0.1039672433 |
| Controlled run 2 | -0.0344847098 | 0.1492175467 | 0.1039672433 |
| Controlled run 3 | -0.0344847098 | 0.1492175467 | 0.1039672433 |

## Environment

The project was executed with Python and common data science libraries.

Suggested packages:

```bash
pip install pandas numpy matplotlib scikit-learn tqdm jupyter ipykernel
```

## Conclusion

The released implementation can be made deterministic by adding fixed random seeds. However, even after controlling randomness, the implementation does not reproduce the methodology described in the paper.

The main reason is that the released notebook does not contain an LSTM model. It implements Random Forest and Decision Tree models, while the paper claims to compare LSTM and Random Forest.

Therefore, the central claim of the paper cannot be verified from the released implementation.

## References
- Jinyuan Sun, original implementation repository: https://github.com/Jinyuan-S/portfolio_optimization
- Original Kaggle dataset: https://www.kaggle.com/datasets/svaningelgem/nyse-100-daily-stock-prices/data