# design notes

## why parquet instead of postgres?

  - the dataset is mostly append-only; there's no OLTP workload
  - partitioning by chain + day makes incremental loads cheap
  - duckdb / pandas can query parquet directly, no server to maintain
  - if anyone ever needs olap aggregations, parquet works

## why no real-time ingestion?

  - the research workflow is offline. labeling and analysis happen days
    after the fact. there's no point streaming.
  - real-time would require running validators or paid websockets, which
    is out of scope for a research toolkit.

## why heuristics instead of a single big classifier?

  - the heuristics (concentration, dev dump, bundled buys, exit liq) are
    interpretable. when a token gets flagged, a human researcher can
    understand why.
  - the classifier in `ml.py` builds on top of these features. it's the
    end of the pipeline, not the whole thing.
