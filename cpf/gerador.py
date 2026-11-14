"""Geração de CPFs fictícios, destinados exclusivamente a testes."""

import random

# 10**9 bases de nove dígitos, menos as 10 de dígitos repetidos.
MAXIMO_UNICOS = 10**9 - 10


def _tabela_pesos(pesos: tuple[int, int, int]) -> list[int]:
    """Soma ponderada de cada bloco de três dígitos (000 a 999)."""
    return [
        sum(int(digito) * peso for digito, peso in zip(f"{bloco:03d}", pesos))
        for bloco in range(1000)
    ]


# A base de nove dígitos é tratada como três blocos de três dígitos; a soma
# ponderada de cada bloco vem de tabela, em vez de ser recalculada por CPF.
_PRIMEIRO_A, _PRIMEIRO_B, _PRIMEIRO_C = (
    _tabela_pesos(p) for p in ((10, 9, 8), (7, 6, 5), (4, 3, 2))
)
_SEGUNDO_A, _SEGUNDO_B, _SEGUNDO_C = (
    _tabela_pesos(p) for p in ((11, 10, 9), (8, 7, 6), (5, 4, 3))
)
# Dígito verificador (módulo 11) para cada soma possível; o 2º dígito soma
# ainda 2 * primeiro (máximo 9), por isso o tamanho vem do maior valor.
_MAIOR_SOMA = (
    max(_SEGUNDO_A) + max(_SEGUNDO_B) + max(_SEGUNDO_C) + 2 * 9
)
_DIGITO = [0 if s % 11 < 2 else 11 - s % 11 for s in range(_MAIOR_SOMA + 1)]
_REPETIDOS = frozenset(int(str(d) * 9) for d in range(10))
_LIMITE_BASE = 10**9


def _gerar_cpf_numerico(rng: random.Random) -> str:
    """Gera um CPF válido sem formatação."""
    while True:
        base = rng.randrange(_LIMITE_BASE)
        if base not in _REPETIDOS:
            break
    a, resto = divmod(base, 1_000_000)
    b, c = divmod(resto, 1000)
    primeiro = _DIGITO[_PRIMEIRO_A[a] + _PRIMEIRO_B[b] + _PRIMEIRO_C[c]]
    segundo = _DIGITO[
        _SEGUNDO_A[a] + _SEGUNDO_B[b] + _SEGUNDO_C[c] + 2 * primeiro
    ]
    return f"{base:09d}{primeiro}{segundo}"


def _formatar(cpf: str, formatado: bool) -> str:
    """Aplica a máscara padrão quando solicitado."""
    if not formatado:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def gerar_cpf(formatado: bool = False, rng: random.Random | None = None) -> str:
    """Gera um CPF fictício válido, opcionalmente com máscara.

    Os valores gerados são fictícios e devem ser usados somente em testes.
    """
    gerador = rng if rng is not None else random.Random()
    return _formatar(_gerar_cpf_numerico(gerador), formatado)


def gerar_cpfs(
    quantidade: int,
    formatado: bool = False,
    rng: random.Random | None = None,
    unicos: bool = True,
) -> list[str]:
    """Gera uma lista de CPFs fictícios válidos.

    Com ``unicos=True``, não repete valores na lista. Quantidade negativa
    gera ``ValueError``; quantidade zero retorna uma lista vazia.
    """
    if quantidade < 0:
        raise ValueError("quantidade não pode ser negativa")
    if unicos and quantidade > MAXIMO_UNICOS:
        raise ValueError(
            f"há no máximo {MAXIMO_UNICOS} CPFs únicos possíveis"
        )
    if quantidade == 0:
        return []

    gerador = rng if rng is not None else random.Random()
    sortear = gerador.randrange
    resultado: list[str] = []
    vistos: set[str] = set()
    # Laço quente (milhões de iterações): variáveis locais e cálculo inline,
    # equivalente a _gerar_cpf_numerico, sem chamadas por CPF.
    while len(resultado) < quantidade:
        base = sortear(_LIMITE_BASE)
        if base in _REPETIDOS:
            continue
        a, resto = divmod(base, 1_000_000)
        b, c = divmod(resto, 1000)
        primeiro = _DIGITO[_PRIMEIRO_A[a] + _PRIMEIRO_B[b] + _PRIMEIRO_C[c]]
        segundo = _DIGITO[
            _SEGUNDO_A[a] + _SEGUNDO_B[b] + _SEGUNDO_C[c] + 2 * primeiro
        ]
        if formatado:
            cpf = f"{a:03d}.{b:03d}.{c:03d}-{primeiro}{segundo}"
        else:
            cpf = f"{base:09d}{primeiro}{segundo}"
        if unicos:
            if cpf in vistos:
                continue
            vistos.add(cpf)
        resultado.append(cpf)
    return resultado
