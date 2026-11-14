"""Formatação de CPFs com a máscara padrão."""

_MENSAGEM = (
    "formato inválido: esperado 11 dígitos, "
    "com ou sem a pontuação 000.000.000-00"
)


def formatar_cpf(valor: str) -> str:
    """Devolve ``valor`` com a máscara ``000.000.000-00``.

    Aceita 11 dígitos ou a máscara exata (idempotente); espaços nas pontas
    são ignorados. Não confere os dígitos verificadores: para isso, use
    ``validar_cpf``. Qualquer outro formato levanta ``ValueError``, cuja
    mensagem nunca inclui o valor recebido.
    """
    if not isinstance(valor, str):
        raise ValueError(_MENSAGEM)

    texto = valor.strip()
    if len(texto) == 14 and texto[3] == "." and texto[7] == "." and texto[11] == "-":
        texto = texto[:3] + texto[4:7] + texto[8:11] + texto[12:]

    if len(texto) != 11 or not all("0" <= c <= "9" for c in texto):
        raise ValueError(_MENSAGEM)
    return f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
