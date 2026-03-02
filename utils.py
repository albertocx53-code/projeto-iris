import csv
import re

def normalize_species(s):
    s = str(s).strip().lower()
    s = s.replace("iris-", "").replace("iris ", "").replace("iris_", "")
    s = s.replace("-", "").replace("_", "").replace(" ", "")
    return s  # setosa/versicolor/virginica

_decimal_comma = re.compile(r"^\s*-?\d+,\d+\s*$")

def detect_delimiter(sample: str) -> str:
    """
    Detecta separador com segurança, inclusive quando números usam vírgula decimal.
    Heurística:
    - Se há ';' e existem números com vírgula (ex.: 5,1), então delimitador = ';'
    - Senão, tenta Sniffer com delimiters comuns
    - fallback: ','
    """
    if ";" in sample and _decimal_comma.search(sample.replace(";", "\n")):
        return ";"
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t|")
        return dialect.delimiter
    except Exception:
        return ","


def to_float(x: str, delim: str) -> float:
    x = str(x).strip()
    # Se delimiter é ';', é muito comum vir decimal com vírgula: 5,1
    if delim == ";" and _decimal_comma.match(x):
        x = x.replace(",", ".")
    return float(x)


def load_iris_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            sample = f.read(4096)
            f.seek(0)

            delim = detect_delimiter(sample)
            reader = csv.reader(f, delimiter=delim)
            rows = [r for r in reader if r]
    except FileNotFoundError:
        return []

    if not rows:
        return []

    # Detecta cabeçalho
    header = [c.strip().lower() for c in rows[0]]
    has_header = any("sepal" in c or "petal" in c or "species" in c for c in header)
    data_rows = rows[1:] if has_header else rows

    out = []
    for r in data_rows:
        if len(r) < 5:
            continue
        try:
            out.append({
                "sepal_length": to_float(r[0], delim),
                "sepal_width":  to_float(r[1], delim),
                "petal_length": to_float(r[2], delim),
                "petal_width":  to_float(r[3], delim),
                "species_norm": normalize_species(r[4]),
            })
        except Exception:
            continue

    return out