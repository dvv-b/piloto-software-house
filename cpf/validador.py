"""Validação de CPFs com ou sem a pontuação convencional."""


def _digito_verificador(digitos: str, pesos: range) -> int:
    """Calcula um dígito verificador pelo método módulo 11."""
    resto = sum(int(digito) * peso for digito, peso in zip(digitos, pesos)) % 11
    return 0 if resto < 2 else 11 - resto


def _normalizar(valor: str) -> str | None:
    """Retorna os onze dígitos se o formato for aceito."""
    if not isinstance(valor, str):
        return None

    texto = valor.strip()
    if len(texto) == 11 and all("0" <= caractere <= "9" for caractere in texto):
        return texto

    if len(texto) == 14 and texto[3] == "." and texto[7] == "." and texto[11] == "-":
        digitos = texto[:3] + texto[4:7] + texto[8:11] + texto[12:]
        if all("0" <= caractere <= "9" for caractere in digitos):
            return digitos

    return None


def validar_cpf(valor: str) -> bool:
    """Informa se ``valor`` é um CPF válido, aceitando a máscara opcional.

    Espaços nas pontas são ignorados. Entradas de outro tipo, formatos
    inválidos, sequências repetidas e dígitos verificadores incorretos
    retornam ``False`` sem lançar exceção.
    """
    digitos = _normalizar(valor)
    if digitos is None or len(set(digitos)) == 1:
        return False

    primeiro = _digito_verificador(digitos[:9], range(10, 1, -1))
    segundo = _digito_verificador(digitos[:9] + str(primeiro), range(11, 1, -1))
    return digitos[-2:] == f"{primeiro}{segundo}"
