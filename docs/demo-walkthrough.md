# Token Risk Feature Store Demo

This walkthrough presents the repo as a feature pipeline for noisy, fast-moving
token markets.

![Token risk feature store demo](assets/screenshots/feature-store-demo.png)

## Flow Chart

```mermaid
flowchart LR
    A[Source APIs and RPCs] --> B[Chain adapters]
    B --> C[Normalization]
    C --> D[Risk feature modules]
    D --> E[Append-only parquet partitions]
    E --> F[Research notebooks]
    E --> G[Offline classifiers]
```

## Entity Graph

```mermaid
erDiagram
    TOKEN ||--o{ SNAPSHOT : has
    SNAPSHOT ||--|| HOLDER_DISTRIBUTION : includes
    SNAPSHOT ||--o{ DEV_WALLET_EVENT : records
    SNAPSHOT ||--o{ BUNDLED_BUY_CLUSTER : groups
    SNAPSHOT ||--|| FEATURE_VECTOR : produces
    FEATURE_VECTOR ||--o{ LABEL : supports

    TOKEN {
      string chain
      string mint
      datetime first_seen
    }
    FEATURE_VECTOR {
      float top1_pct
      float top10_pct
      float gini
      bool exit_liquidity_flag
    }
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant CLI as sinfun CLI
    participant Adapter as Source Adapter
    participant Feature as Feature Modules
    participant Store as Parquet Store
    participant Notebook as Analysis Notebook

    CLI->>Adapter: request token snapshot
    Adapter-->>CLI: normalized holders and metadata
    CLI->>Feature: compute concentration and lifecycle signals
    Feature-->>Store: append feature row
    Notebook->>Store: query historical partitions
    Store-->>Notebook: offline analysis dataset
```

## Sample Feature Row

```json
{
  "chain": "solana",
  "mint": "MINT_ADDRESS",
  "snapshot_day": "2026-05-17",
  "top1_pct": 47.2,
  "top10_pct": 81.4,
  "gini": 0.94,
  "bundled_buy_score": 0.73,
  "exit_liquidity_flag": true
}
```
