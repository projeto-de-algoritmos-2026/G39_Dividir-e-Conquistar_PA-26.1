"""
test_algorithms.py
Testes unitários para os três algoritmos de seleção.

Uso:
    python -m pytest tests/ -v
"""

import pytest
import random

from statrank.algorithms import baseline_select, quickselect, median_of_medians, percentile


ALGORITMOS = [
    ("baseline", baseline_select),
    ("quickselect", quickselect),
    ("mom", median_of_medians),
]


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_k_minimo(nome, func):
    arr = [5, 3, 1, 4, 2]
    assert func(arr, 1) == 1, f"{nome}: k=1 deve retornar o menor"


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_k_maximo(nome, func):
    arr = [5, 3, 1, 4, 2]
    assert func(arr, 5) == 5, f"{nome}: k=n deve retornar o maior"


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_k_medio(nome, func):
    arr = [5, 3, 1, 4, 2]
    assert func(arr, 3) == 3, f"{nome}: k=3 deve retornar a mediana"


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_array_um_elemento(nome, func):
    assert func([42], 1) == 42


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_array_com_duplicatas(nome, func):
    arr = [3, 3, 3, 1, 1, 5]
    assert func(arr, 1) == 1
    assert func(arr, 3) == 3
    assert func(arr, 6) == 5


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_array_negativos(nome, func):
    arr = [-5, -1, -3, -2, -4]
    assert func(arr, 1) == -5
    assert func(arr, 5) == -1


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_consistencia_com_sort(nome, func):
    """Todos os algoritmos devem concordar com sorted() para arrays aleatórios."""
    random.seed(42)
    for _ in range(20):
        n = random.randint(10, 200)
        arr = [random.uniform(-1000, 1000) for _ in range(n)]
        k = random.randint(1, n)
        esperado = sorted(arr)[k - 1]
        assert func(list(arr), k) == pytest.approx(esperado, rel=1e-9), \
            f"{nome}: discordância para n={n}, k={k}"


@pytest.mark.parametrize("nome, func", ALGORITMOS)
def test_k_invalido(nome, func):
    arr = [1, 2, 3]
    with pytest.raises(ValueError):
        func(arr, 0)
    with pytest.raises(ValueError):
        func(arr, 4)


def test_percentil_mediana():
    arr = list(range(1, 101))
    assert percentile(arr, 50, method="mom") == 50


def test_percentil_metodos_concordam():
    random.seed(7)
    arr = [random.randint(0, 10_000) for _ in range(500)]
    for p in [10, 25, 50, 75, 90]:
        b = percentile(arr, p, method="baseline")
        q = percentile(arr, p, method="quickselect")
        m = percentile(arr, p, method="mom")
        assert b == q == m, f"Divergência no P{p}: baseline={b}, qs={q}, mom={m}"