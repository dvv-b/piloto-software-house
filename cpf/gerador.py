"""Geração de CPFs fictícios, destinados exclusivamente a testes."""

import random

# 10**9 bases de nove dígitos, menos as 10 de dígitos repetidos.
MAXIMO_UNICOS = 10**9 - 10


def _calcular_digito(digitos: list[int], pesos: range) -> int:
    """Calcula um dígito verificador pelo módulo 11."""
    resto = sum(digito * peso for digito, peso in zip(digitos, pesos)) % 11
    return 0 if resto < 2 else 11 - resto


def _gerar_cpf_numerico(rng: random.Random) -> str:
    """Gera um CPF válido sem formatação."""
    while True:
        base = [rng.randrange(10) for _ in range(9)]
        if len(set(base)) == 1:
            continue

        primeiro = _calcular_digito(base, range(10, 1, -1))
        segundo = _calcular_digito(
            [*base, primeiro], range(11, 1, -1)
        )
        return "".join(map(str, [*base, primeiro, segundo]))


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
    resultado: list[str] = []
    vistos: set[str] = set()
    while len(resultado) < quantidade:
        cpf = _gerar_cpf_numerico(gerador)
        if unicos and cpf in vistos:
            continue
        vistos.add(cpf)
        resultado.append(_formatar(cpf, formatado))
    return resultado
