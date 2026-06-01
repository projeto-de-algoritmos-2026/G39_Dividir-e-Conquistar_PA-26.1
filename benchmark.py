"""
benchmark.py
Compara o tempo de execução dos três algoritmos para diferentes tamanhos de entrada.
Gera gráfico salvo em results/benchmark.png.

Uso:
    python benchmark.py
    python benchmark.py --max-n 500000 --repeticoes 5
"""

import argparse
import random
import time
import statistics
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from statrank.algorithms import baseline_select, quickselect, median_of_medians


def medir_tempo(func, arr, k, repeticoes):
    """Executa a função `repeticoes` vezes e retorna a mediana dos tempos em ms."""
    tempos = []
    for _ in range(repeticoes):
        copia = list(arr)
        inicio = time.perf_counter()
        func(copia, k)
        tempos.append((time.perf_counter() - inicio) * 1000)
    return statistics.median(tempos)


def rodar_benchmark(tamanhos, repeticoes, percentil=50):
    resultados = {
        "baseline": [],
        "quickselect": [],
        "mom": [],
    }

    for n in tamanhos:
        arr = [random.uniform(0, 1_000_000) for _ in range(n)]
        k = max(1, int(n * percentil / 100))

        print(f"  n={n:>8,}  ", end="", flush=True)

        t_b = medir_tempo(baseline_select, arr, k, repeticoes)
        print(f"baseline={t_b:7.2f}ms  ", end="", flush=True)
        resultados["baseline"].append(t_b)

        t_q = medir_tempo(quickselect, arr, k, repeticoes)
        print(f"quickselect={t_q:7.2f}ms  ", end="", flush=True)
        resultados["quickselect"].append(t_q)

        t_m = medir_tempo(median_of_medians, arr, k, repeticoes)
        print(f"mom={t_m:7.2f}ms")
        resultados["mom"].append(t_m)

    return resultados


def plotar(tamanhos, resultados, output_path):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(tamanhos, resultados["baseline"], marker="o", label="Baseline — O(n log n)", linewidth=2)
    ax.plot(tamanhos, resultados["quickselect"], marker="s", label="Quickselect — O(n) médio", linewidth=2)
    ax.plot(tamanhos, resultados["mom"], marker="^", label="Mediana das Medianas — O(n) pior caso", linewidth=2)

    ax.set_xlabel("Tamanho da entrada (n)", fontsize=12)
    ax.set_ylabel("Tempo mediano (ms)", fontsize=12)
    ax.set_title("Comparação de algoritmos de seleção — StatRank", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"\nGráfico salvo em: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark dos algoritmos de seleção.")
    parser.add_argument("--max-n", type=int, default=200_000, help="Tamanho máximo de n (padrão: 200000)")
    parser.add_argument("--repeticoes", type=int, default=3, help="Repetições por medição (padrão: 3)")
    parser.add_argument("--passos", type=int, default=8, help="Quantidade de pontos no gráfico (padrão: 8)")
    parser.add_argument("--output", default="results/benchmark.png", help="Caminho do gráfico de saída")
    args = parser.parse_args()

    step = args.max_n // args.passos
    tamanhos = [step * i for i in range(1, args.passos + 1)]

    print(f"Benchmark — {args.repeticoes} repetições por ponto, percentil P50\n")
    resultados = rodar_benchmark(tamanhos, args.repeticoes)
    plotar(tamanhos, resultados, args.output)


if __name__ == "__main__":
    main()