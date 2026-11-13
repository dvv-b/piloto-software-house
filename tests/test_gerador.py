"""Testes do gerador de CPFs fictícios."""

import random
import re
import unittest

from cpf.gerador import gerar_cpf, gerar_cpfs


def _cpf_valido(cpf: str) -> bool:
    """Verifica os dígitos sem depender de outro módulo do pacote."""
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if len(set(cpf)) == 1:
        return False

    digitos = [int(digito) for digito in cpf]
    soma_1 = sum(digitos[posicao] * (10 - posicao) for posicao in range(9))
    resto_1 = soma_1 % 11
    dv_1 = 0 if resto_1 < 2 else 11 - resto_1

    soma_2 = sum(digitos[posicao] * (11 - posicao) for posicao in range(10))
    resto_2 = soma_2 % 11
    dv_2 = 0 if resto_2 < 2 else 11 - resto_2
    return digitos[9] == dv_1 and digitos[10] == dv_2


class GeradorCpfTest(unittest.TestCase):
    def test_gera_cpf_com_tamanho_e_apenas_digitos(self) -> None:
        cpf = gerar_cpf(rng=random.Random(7))
        self.assertEqual(len(cpf), 11)
        self.assertTrue(cpf.isdigit())

    def test_gera_cpf_formatado_com_mascara(self) -> None:
        cpf = gerar_cpf(formatado=True, rng=random.Random(7))
        self.assertRegex(cpf, re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))

    def test_milhares_de_cpfs_tem_digitos_validos_e_nao_tem_todos_iguais(self) -> None:
        # Um único gerador mantém a sequência da seed ao longo da amostra.
        rng = random.Random(1234)
        cpfs = [gerar_cpf(rng=rng) for _ in range(5000)]
        self.assertTrue(all(_cpf_valido(cpf) for cpf in cpfs))
        self.assertTrue(all(len(set(cpf)) > 1 for cpf in cpfs))

    def test_mesma_seed_produz_mesma_sequencia(self) -> None:
        rng_a, rng_b = random.Random(99), random.Random(99)
        primeira = [gerar_cpf(rng=rng_a) for _ in range(20)]
        segunda = [gerar_cpf(rng=rng_b) for _ in range(20)]
        self.assertEqual(primeira, segunda)

    def test_seeds_diferentes_produzem_resultados_diferentes(self) -> None:
        self.assertNotEqual(
            gerar_cpf(rng=random.Random(1)), gerar_cpf(rng=random.Random(2))
        )

    def test_gerar_cpfs_com_unicidade(self) -> None:
        cpfs = gerar_cpfs(1000, rng=random.Random(2026))
        self.assertEqual(len(cpfs), 1000)
        self.assertEqual(len(set(cpfs)), 1000)
        self.assertTrue(all(_cpf_valido(cpf) for cpf in cpfs))

    def test_quantidade_zero_retorna_lista_vazia(self) -> None:
        self.assertEqual(gerar_cpfs(0), [])

    def test_quantidade_negativa_gera_value_error(self) -> None:
        with self.assertRaises(ValueError):
            gerar_cpfs(-1)

    def test_gerar_cpfs_respeita_formatacao(self) -> None:
        cpfs = gerar_cpfs(10, formatado=True, rng=random.Random(18))
        self.assertTrue(
            all(re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) for cpf in cpfs)
        )

    def test_geracao_sem_rng_nao_quebra(self) -> None:
        self.assertTrue(_cpf_valido(gerar_cpf()))
        cpfs = gerar_cpfs(3)
        self.assertEqual(len(cpfs), 3)
        self.assertTrue(all(_cpf_valido(cpf) for cpf in cpfs))


if __name__ == "__main__":
    unittest.main()
