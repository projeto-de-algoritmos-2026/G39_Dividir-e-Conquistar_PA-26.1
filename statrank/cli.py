"""
cli.py
Interface de linha de comando do StatRank.

Uso:
    python -m statrank.cli arquivo.csv --k 100
    python -m statrank.cli arquivo.csv --percentil 90
    python -m statrank.cli arquivo.csv --percentil 50 --column salario --metodo mom
    python -m statrank.cli arquivo.csv --colunas
"""

import argparse
import sys
import time

from statrank.loader import load_csv, list_columns
from statrank.algorithms import median_of_medians, quickselect, baseline_select, percentile


def parse_args():
    parser = argparse.ArgumentParser(
        prog="statrank",
        description="Encontra o k-ésimo menor valor em datasets usando Mediana das Medianas.",
    )
    parser.add_argument("arquivo", help="Caminho para o arquivo CSV")
    parser.add_argument("--column", "-c", default=None, help="Nome da coluna numérica")
    parser.add_argument("--k", type=int, default=None, help="k-ésimo menor elemento (1-indexado)")
    parser.add_argument("--percentil", "-p", type=float, default=None, help="Percentil desejado (0–100)")
    parser.add_argument(
        "--metodo", "-m",
        choices=["mom", "quickselect", "baseline"],
        default="mom",
        help="Algoritmo: mom (padrão) | quickselect | baseline",
    )
    parser.add_argument("--colunas", action="store_true", help="Lista as colunas do CSV e sai")
    parser.add_argument("--resumo", action="store_true", help="Exibe resumo estatístico completo")
    return parser.parse_args()


def fmt(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    args = parse_args()

    if args.colunas:
        cols = list_columns(args.arquivo)
        print("Colunas disponíveis:")
        for col in cols:
            print(f"  • {col}")
        sys.exit(0)

    print(f"Carregando dados de '{args.arquivo}'...")
    try:
        dados = load_csv(args.arquivo, column=args.column)
    except (FileNotFoundError, ValueError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

    n = len(dados)
    print(f"{n:,} valores carregados.\n")

    metodo_label = {"mom": "Mediana das Medianas", "quickselect": "Quickselect", "baseline": "Baseline (sort)"}

    if args.resumo:
        print("Resumo estatístico (usando Mediana das Medianas):")
        print("-" * 40)
        for p in [10, 25, 50, 75, 90, 95, 99]:
            val = percentile(dados, p, method="mom")
            print(f"  P{p:>2}: {fmt(val)}")
        print(f"  Mín:  {fmt(min(dados))}")
        print(f"  Máx:  {fmt(max(dados))}")
        print()

    if args.k is not None:
        if not 1 <= args.k <= n:
            print(f"Erro: k={args.k} fora do intervalo [1, {n}]", file=sys.stderr)
            sys.exit(1)

        inicio = time.perf_counter()
        if args.metodo == "mom":
            resultado = median_of_medians(dados, args.k)
        elif args.metodo == "quickselect":
            resultado = quickselect(dados, args.k)
        else:
            resultado = baseline_select(dados, args.k)
        elapsed = time.perf_counter() - inicio

        print(f"Método:    {metodo_label[args.metodo]}")
        print(f"k:         {args.k:,} de {n:,}")
        print(f"Resultado: {fmt(resultado)}")
        print(f"Tempo:     {elapsed * 1000:.3f} ms")

    elif args.percentil is not None:
        inicio = time.perf_counter()
        resultado = percentile(dados, args.percentil, method=args.metodo)
        elapsed = time.perf_counter() - inicio

        print(f"Método:    {metodo_label[args.metodo]}")
        print(f"Percentil: P{args.percentil}")
        print(f"Resultado: {fmt(resultado)}")
        print(f"Tempo:     {elapsed * 1000:.3f} ms")

    else:
        print("Informe --k ou --percentil. Use --help para ver as opções.")
        sys.exit(1)


if __name__ == "__main__":
    main()