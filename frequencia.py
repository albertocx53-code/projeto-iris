import math

def freq_nao_agrupada(valores):
    freq = {}
    for v in valores:
        freq[v] = freq.get(v, 0) + 1
    return sorted(freq.items(), key=lambda t: t[0])

def classes_por_sturges(valores):
    n = len(valores)
    k = max(1, round(1 + 3.3 * math.log10(n)))
    minimo = min(valores)
    maximo = max(valores)
    amp_total = maximo - minimo
    h = (amp_total / k) if amp_total != 0 else 0.0
    return k, h, minimo, maximo

def freq_agrupada(valores, k, h, minimo, maximo):
    tabela = []
    if k <= 0:
        return tabela

    # cria classes
    for i in range(k):
        a = minimo + i * h
        b = a + h if h != 0 else maximo
        if i == k - 1:
            b = maximo  # fecha no máximo
        tabela.append({"lower": a, "upper": b, "midpoint": (a + b) / 2, "fi": 0})

    # conta
    for v in valores:
        if h == 0:
            tabela[0]["fi"] += 1
            continue
        idx = int((v - minimo) / h)
        if idx >= k:
            idx = k - 1
        if idx < 0:
            idx = 0
        tabela[idx]["fi"] += 1

    return tabela

def grouped_mean(tabela):
    total = sum(c["fi"] for c in tabela)
    return sum(c["fi"] * c["midpoint"] for c in tabela) / total

def grouped_variance(tabela):
    total = sum(c["fi"] for c in tabela)
    m = grouped_mean(tabela)
    return sum(c["fi"] * (c["midpoint"] - m) ** 2 for c in tabela) / total

def grouped_std_dev(tabela):
    return math.sqrt(grouped_variance(tabela))

def grouped_median(tabela):
    N = sum(c["fi"] for c in tabela)
    metade = N / 2
    fac = 0
    for c in tabela:
        fac_ant = fac
        fac += c["fi"]
        if fac >= metade and c["fi"] > 0:
            L = c["lower"]
            h = c["upper"] - c["lower"]
            return L + ((metade - fac_ant) / c["fi"]) * h
    return tabela[-1]["midpoint"]