"""Testes automatizados do validador de CPF."""

import unittest

from cpf.validador import validar_cpf


class TestValidarCpf(unittest.TestCase):
    def test_aceita_cpfs_validos_com_e_sem_mascara(self):
        for cpf in (
            "529.982.247-25",
            "52998224725",
            "111.444.777-35",
            "11144477735",
        ):
            with self.subTest(cpf=cpf):
                self.assertTrue(validar_cpf(cpf))

    def test_ignora_espacos_nas_pontas(self):
        self.assertTrue(validar_cpf("  529.982.247-25 \t"))
        self.assertTrue(validar_cpf(" 52998224725 "))

    def test_rejeita_digito_verificador_incorreto(self):
        self.assertFalse(validar_cpf("529.982.247-24"))  # DV2 incorreto
        self.assertFalse(validar_cpf("529.982.247-15"))  # DV1 incorreto

    def test_rejeita_sequencias_de_digitos_repetidos(self):
        for digito in "0123456789":
            cpf = digito * 9 + digito * 2
            with self.subTest(cpf=cpf):
                self.assertFalse(validar_cpf(cpf))
                self.assertFalse(validar_cpf(f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"))

    def test_rejeita_tamanhos_invalidos(self):
        for cpf in ("5299822472", "529982247250", ""):
            with self.subTest(cpf=cpf):
                self.assertFalse(validar_cpf(cpf))

    def test_rejeita_letras_e_caracteres_unicode(self):
        self.assertFalse(validar_cpf("52998224a25"))
        self.assertFalse(validar_cpf("١٢٣.٤٥٦.٧٨٩-٠٩"))

    def test_rejeita_mascaras_malformadas(self):
        for cpf in ("123.45678909", "123-456-789.09", "529982.247-25"):
            with self.subTest(cpf=cpf):
                self.assertFalse(validar_cpf(cpf))

    def test_rejeita_valores_que_nao_sao_string(self):
        for valor in (None, 52998224725, b"52998224725", ["52998224725"]):
            with self.subTest(valor=valor):
                self.assertFalse(validar_cpf(valor))

    def test_resto_zero_ou_um_produz_digito_zero(self):
        # Os primeiros nove dígitos geram resto 0 e 1, respectivamente.
        self.assertTrue(validar_cpf("00000001406"))
        self.assertTrue(validar_cpf("00000000604"))


if __name__ == "__main__":
    unittest.main()
