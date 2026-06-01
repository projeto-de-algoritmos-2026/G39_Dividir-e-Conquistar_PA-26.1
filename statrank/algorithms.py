"""
algorithms.py
Implementações dos três algoritmos de seleção do k-ésimo menor elemento.
"""
import random


def baseline_select(arr, k):
    """
    Baseline: ordena o array e retorna o k-ésimo menor elemento.
    Complexidade: O(n log n) tempo, O(n) espaço.
    k é 1-indexado (k=1 retorna o menor elemento).
    """
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} fora do intervalo válido [1, {len(arr)}]")
    return sorted(arr)[k - 1]


def quickselect(arr, k):
    """
    Quickselect iterativo com partição de 3 vias (Dutch National Flag).
    Trata duplicatas corretamente — sem RecursionError.
    Complexidade: O(n) médio, O(n²) pior caso.
    k é 1-indexado.
    """
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} fora do intervalo válido [1, {len(arr)}]")
    return _quickselect(list(arr), 0, len(arr) - 1, k - 1)


def _quickselect(arr, left, right, k):
    """
    Versão iterativa com partição de 3 vias.
    Trata duplicatas corretamente — evita RecursionError em arrays com muitos iguais.
    """
    while left < right:
        pivot = arr[random.randint(left, right)]

        # Partição de 3 vias: [left..lt-1] < pivot, [lt..gt] == pivot, [gt+1..right] > pivot
        lt, i, gt = left, left, right
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1

        if k < lt:
            right = lt - 1
        elif k > gt:
            left = gt + 1
        else:
            return pivot  # k está na zona de iguais

    return arr[left]


def median_of_medians(arr, k):
    """
    Mediana das Medianas: seleção com pivô garantido.
    Complexidade: O(n) pior caso.
    k é 1-indexado.
    """
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} fora do intervalo válido [1, {len(arr)}]")
    return _mom_select(list(arr), k - 1)


def _mom_select(arr, k):
    if len(arr) <= 5:
        return sorted(arr)[k]

    # Passo 1: divide em grupos de 5
    chunks = [arr[i:i + 5] for i in range(0, len(arr), 5)]

    # Passo 2: ordena cada grupo e extrai a mediana
    medians = [sorted(chunk)[len(chunk) // 2] for chunk in chunks]

    # Passo 3: encontra o MOM recursivamente — pivô com garantia de qualidade
    # Garante que pelo menos 3n/10 elementos ficam em cada lado (ver análise T(n/5))
    pivot = _mom_select(medians, len(medians) // 2)

    # Passo 4: particiona o array original em torno do MOM
    low   = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    high  = [x for x in arr if x > pivot]

    # Passo 5: recursa no subproblema relevante
    # Equivalente a kth_smallest(R, k-(|L|+1)) do slide quando não há duplicatas
    if k < len(low):
        return _mom_select(low, k)
    elif k < len(low) + len(equal):
        return pivot                                      # k-ésimo é o próprio pivô
    else:
        return _mom_select(high, k - len(low) - len(equal))


def percentile(arr, p, method="mom"):
    """
    Calcula o p-ésimo percentil (0–100) usando o método escolhido.
    method: 'mom' | 'quickselect' | 'baseline'
    """
    if not 0 <= p <= 100:
        raise ValueError("Percentil deve estar entre 0 e 100")
    n = len(arr)
    k = max(1, min(n, round(p / 100 * n)))
    if method == "mom":
        return median_of_medians(arr, k)
    elif method == "quickselect":
        return quickselect(arr, k)
    else:
        return baseline_select(arr, k)