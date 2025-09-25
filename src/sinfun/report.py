"""Pretty-print a token's rug-feature snapshot."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.2f}"
    if isinstance(v, list):
        return f"[{len(v)} items]"
    if isinstance(v, dict):
        return f"({len(v)} keys)"
    return str(v)


def render_token(rec: dict) -> None:
    console = Console()
    title = rec.get("mint", "(unknown)")
    console.print(Panel.fit(f"sinfun: {title}", style="bold magenta"))
    t = Table(title="features", show_lines=False)
    t.add_column("name")
    t.add_column("value")
    interesting = ("top1_pct", "top10_pct", "gini", "n_holders",
                   "dev_dump_score", "is_mint_renounced",
                   "n_bundled_buy_clusters", "exit_liquidity_events",
                   "age_days", "liquidity_usd")
    for k in interesting:
        if k in rec:
            t.add_row(k, _fmt(rec[k]))
    console.print(t)



def render_token_with_score(rec: dict, model_path: str = None) -> None:
    render_token(rec)
    if model_path:
        try:
            from .ml import predict_rug_prob
            p = predict_rug_prob(model_path, rec)
            console = Console()
            color = "red" if p > 0.5 else "yellow" if p > 0.2 else "green"
            console.print(f"\n[bold {color}]rug probability: {p:.1%}[/]")
        except Exception as e:
            print(f"  (model load failed: {e})")
