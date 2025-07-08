"""sinfun — command line entrypoint."""
import click


@click.group()
@click.version_option()
def cli():
    """sinfun-chain — research toolkit for speculative DeFi."""


@cli.command("inspect")
@click.argument("mint")
@click.option("--chain", default="solana", type=click.Choice(["solana", "base", "hyperliquid"]))
def inspect_cmd(mint, chain):
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
        click.echo(get_open_interest(mint))
        return
    rec.update(featurize(rec))
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
