import math

def mean(lista):
    return sum(lista) / len(lista)

def median(lista):
    s = sorted(lista)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2

def mode(lista):
    freq = {}
    for v in lista:
        freq[v] = freq.get(v, 0) + 1
    maxf = max(freq.values())
    candidatos = [v for v, f in freq.items() if f == maxf]
    return min(candidatos)  # critério consistente

def variance(lista):
    m = mean(lista)
    return sum((x - m) ** 2 for x in lista) / len(lista)

def std_dev(lista):
    return math.sqrt(variance(lista))