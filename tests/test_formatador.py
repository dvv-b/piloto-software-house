"""Testes do formatador de CPF."""

import random
import unittest

from cpf.formatador import formatar_cpf
from cpf.gerador import gerar_cpf


class FormatarCpfTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cpf = gerar_cpf(rng=random.Random(11))  # fictício
        self.mascarado = f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def test_formata_onze_digitos(self) -> None:
        self.assertEqual(formatar_cpf(self.cpf), self.mascarado)

    def test_e_idempotente(self) -> None:
        self.assertEqual(formatar_cpf(self.mascarado), self.mascarado)

    def test_ignora_espacos_nas_pontas(self) -> None:
        self.assertEqual(formatar_cpf(f"  {self.cpf}\n"), self.mascarado)

    def test_nao_confere_digitos_verificadores(self) -> None:
        self.assertEqual(formatar_cpf("11111111111"), "111.111.111-11")

    def test_formatos_invalidos_levantam_value_error(self) -> None:
        invalidos = [
            "", "   ", self.cpf[:10], self.cpf + "0", "1234567890a",
            "123.456.789.00", "12.3456.789-00", "123.456.78900", None, 123,
        ]
        for valor in invalidos:
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    formatar_cpf(valor)  # type: ignore[arg-type]

    def test_mensagem_de_erro_nao_inclui_o_valor(self) -> None:
        entrada = self.cpf[:10]
        with self.assertRaises(ValueError) as ctx:
            formatar_cpf(entrada)
        self.assertNotIn(entrada, str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
