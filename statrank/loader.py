"""
loader.py
Leitura e limpeza de arquivos CSV com dados numéricos.
Detecta automaticamente encoding (utf-8, latin-1) e separador (, ou ;).
"""

import csv
import os

_ENCODINGS = ["utf-8-sig", "utf-8", "latin-1"]


def _open_csv(filepath):
    """
    Abre o CSV detectando encoding e separador automaticamente.
    Retorna (file_object, encoding, delimiter).
    """
    for enc in _ENCODINGS:
        for delim in [";", ","]:
            try:
                f = open(filepath, newline="", encoding=enc)
                sample = f.read(4096)
                f.seek(0)
                first_line = sample.split("\n")[0]
                if first_line.count(delim) >= 1:
                    return f, enc, delim
                f.close()
            except (UnicodeDecodeError, OSError):
                try:
                    f.close()
                except Exception:
                    pass
    raise ValueError(
        "Não foi possível detectar o encoding/separador do arquivo."
    )


def _clean(val):
    """Converte string numérica brasileira (1.234,56) para float."""
    v = val.strip().replace("R$", "").replace(" ", "")
    # Formato brasileiro: ponto como milhar, vírgula como decimal
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    elif "," in v:
        v = v.replace(",", ".")
    return v


def load_csv(filepath, column=None):
    """
    Lê um CSV e retorna uma lista de floats de uma coluna numérica.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    f, enc, delim = _open_csv(filepath)
    try:
        reader = csv.DictReader(f, delimiter=delim)
        headers = reader.fieldnames

        if not headers:
            raise ValueError("CSV não possui cabeçalho.")

        if column is None:
            column = _detect_numeric_column(reader, headers)
            f.seek(0)
            reader = csv.DictReader(f, delimiter=delim)

        if column not in headers:
            raise ValueError(
                f"Coluna '{column}' não encontrada. Disponíveis: {headers}"
            )

        values = []
        for row in reader:
            try:
                values.append(float(_clean(row[column])))
            except (ValueError, TypeError):
                continue
    finally:
        f.close()

    if not values:
        raise ValueError(f"Nenhum valor numérico encontrado na coluna '{column}'.")

    return values


def _detect_numeric_column(reader, headers):
    """Detecta automaticamente a primeira coluna com valores numéricos."""
    rows = []
    for i, row in enumerate(reader):
        rows.append(row)
        if i >= 20:
            break

    for col in headers:
        hits = sum(1 for row in rows if _is_numeric(row[col]))
        if hits >= len(rows) * 0.7:
            return col

    raise ValueError(
        "Não foi possível detectar coluna numérica. Use --column para especificar."
    )


def _is_numeric(val):
    try:
        float(_clean(val))
        return True
    except (ValueError, TypeError):
        return False


def list_columns(filepath):
    """Retorna as colunas disponíveis no CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    f, enc, delim = _open_csv(filepath)
    try:
        reader = csv.DictReader(f, delimiter=delim)
        cols = reader.fieldnames or []
        print(f"  (encoding: {enc}, separador: '{delim}')")
        return cols
    finally:
        f.close()