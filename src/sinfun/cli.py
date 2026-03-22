"""sinfun — command line entrypoint."""
import json
import click


@click.group()
@click.version_option()
def cli():
    """sinfun-chain — research toolkit for speculative DeFi."""


@cli.command("inspect")
@click.argument("mint")
@click.option("--chain", default="solana", type=click.Choice(["solana", "base", "hyperliquid"]))
@click.option("--json", "as_json", is_flag=True, help="emit JSON instead of pretty output")
def inspect_cmd(mint, chain, as_json):
    """Quick rug-feature snapshot for a single token."""
    from .signals.rug_features import featurize

    if chain == "solana":
        from .chains.solana import HeliusClient
        c = HeliusClient()
        holders = c.top_holders(mint)
        rec = {"mint": mint, "holders": holders}
    elif chain == "base":
        click.echo("base inspect not implemented yet — use solana")
        return
    else:
        from .chains.hyperliquid import get_open_interest
        out = get_open_interest(mint)
        click.echo(json.dumps(out) if as_json else out)
        return
    rec.update(featurize(rec))
    if as_json:
        rec.pop("holders", None)  # too verbose for json line use
        click.echo(json.dumps(rec))
        return
    for k, v in rec.items():
        if k == "holders":
            continue
        click.echo(f"  {k:>22s}  {v}")


@cli.command("backfill")
@click.option("--mints-file", required=True)
@click.option("--out", default="data/")
@click.option("--chain", default="solana")
def backfill_cmd(mints_file, out, chain):
    import subprocess, sys
    if chain == "solana":
        subprocess.run([sys.executable, "scripts/backfill_solana.py",
                        "--mints-file", mints_file, "--out", out])
    else:
        click.echo(f"chain {chain} not yet supported")


if __name__ == "__main__":
    cli()
