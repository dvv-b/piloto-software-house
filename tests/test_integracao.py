"""Integração: tudo que o gerador produz deve passar no validador."""

import random
import unittest

from cpf.gerador import gerar_cpf, gerar_cpfs
from cpf.validador import validar_cpf


class TestIntegracao(unittest.TestCase):
    def test_gerados_sem_mascara_sao_validos(self):
        for cpf in gerar_cpfs(5000, rng=random.Random(1)):
            self.assertTrue(validar_cpf(cpf), cpf)

    def test_gerados_com_mascara_sao_validos(self):
        for cpf in gerar_cpfs(5000, formatado=True, rng=random.Random(2)):
            self.assertTrue(validar_cpf(cpf), cpf)

    def test_gerar_cpf_sem_rng_e_valido(self):
        for _ in range(200):
            self.assertTrue(validar_cpf(gerar_cpf()))

    def test_alterar_um_digito_verificador_invalida(self):
        for cpf in gerar_cpfs(500, rng=random.Random(3)):
            dv = int(cpf[-1])
            quebrado = cpf[:-1] + str((dv + 1) % 10)
            self.assertFalse(validar_cpf(quebrado), quebrado)


if __name__ == "__main__":
    unittest.main()
