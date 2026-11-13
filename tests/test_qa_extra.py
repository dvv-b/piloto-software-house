"""Testes adicionais de QA: oráculo independente, bordas e determinismo."""

import random
import unittest

from cpf.gerador import gerar_cpf, gerar_cpfs
from cpf.validador import validar_cpf


def _oraculo(cpf: str) -> bool:
    """Implementação independente (aritmética direta, sem reutilizar o código)."""
    d = [int(c) for c in cpf]
    if len(set(d)) == 1:
        return False
    s1 = sum(d[i] * (10 - i) for i in range(9))
    dv1 = (s1 * 10) % 11 % 10
    s2 = sum(d[i] * (11 - i) for i in range(9)) + dv1 * 2
    dv2 = (s2 * 10) % 11 % 10
    return d[9] == dv1 and d[10] == dv2


def _mascara(c: str) -> str:
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"


class TestOraculoIndependente(unittest.TestCase):
    def test_validador_concorda_com_oraculo_em_cpfs_aleatorios(self):
        rng = random.Random(20261112)
        validos = 0
        for _ in range(100_000):
            c = "".join(rng.choice("0123456789") for _ in range(11))
            esperado = _oraculo(c)
            validos += esperado
            self.assertEqual(validar_cpf(c), esperado, c)
            self.assertEqual(validar_cpf(_mascara(c)), esperado, c)
        self.assertGreater(validos, 500)  # amostra contém positivos suficientes

    def test_validador_concorda_com_oraculo_em_bases_com_dv_correto(self):
        rng = random.Random(7)
        for _ in range(20_000):
            base = "".join(rng.choice("0123456789") for _ in range(9))
            d = [int(x) for x in base]
            dv1 = (sum(d[i] * (10 - i) for i in range(9)) * 10) % 11 % 10
            dv2 = (sum(d[i] * (11 - i) for i in range(9)) + dv1 * 2) * 10 % 11 % 10
            c = f"{base}{dv1}{dv2}"
            self.assertEqual(validar_cpf(c), len(set(c)) > 1, c)

    def test_todo_dv_alterado_em_gerados_e_invalido(self):
        rng = random.Random(3)
        for c in gerar_cpfs(500, rng=rng):
            for pos in (9, 10):
                for novo in "0123456789":
                    if novo == c[pos]:
                        continue
                    m = c[:pos] + novo + c[pos + 1:]
                    with self.subTest(cpf=m):
                        self.assertFalse(validar_cpf(m))

    def test_cobre_todos_os_restos_de_cada_dv(self):
        restos1, restos2 = set(), set()
        rng = random.Random(11)
        for _ in range(5000):
            d = [rng.randrange(10) for _ in range(9)]
            r1 = sum(d[i] * (10 - i) for i in range(9)) % 11
            dv1 = 0 if r1 < 2 else 11 - r1
            r2 = (sum(d[i] * (11 - i) for i in range(9)) + dv1 * 2) % 11
            restos1.add(r1)
            restos2.add(r2)
        self.assertEqual(restos1, set(range(11)))
        self.assertEqual(restos2, set(range(11)))


class TestBordasValidador(unittest.TestCase):
    def test_rejeita_espaco_ou_quebra_interna(self):
        for v in ("529 982 247 25", "529.982.247- 25", "5299822 4725", "529.982.247-25\n25"):
            with self.subTest(v=v):
                self.assertFalse(validar_cpf(v))

    def test_mascara_com_separadores_trocados_ou_extras(self):
        for v in ("529-982-247.25", "529.982.247.25", "529,982,247-25",
                  "529.982.247–25", "529.982.247-255", "5.29.982.247-25",
                  "..529982247-25", "529.982.2472-5"):
            with self.subTest(v=v):
                self.assertFalse(validar_cpf(v))

    def test_unicode_variantes(self):
        for v in ("５２９９８２２４７２５",      # dígitos fullwidth
                  "529.982.247-２５",
                  "5299822472٥",            # arábico-índico
                  "529982247²25",           # sobrescrito
                  "52998224725​",           # zero-width space
                  "﻿52998224725"):          # BOM
            with self.subTest(v=repr(v)):
                self.assertFalse(validar_cpf(v))

    def test_whitespace_nas_pontas_variantes(self):
        self.assertTrue(validar_cpf("\n52998224725\r\n"))
        self.assertTrue(validar_cpf("\t529.982.247-25\t"))

    def test_tipos_estranhos_nao_lancam(self):
        class Estranho:
            def __str__(self):
                raise RuntimeError("não deve ser chamado")

        for v in (None, 0, 5.29, True, object(), Estranho(), (), {}, bytearray(b"52998224725"),
                  float("nan"), "".join(["5"] * 1000)):
            with self.subTest(v=type(v).__name__):
                self.assertIs(validar_cpf(v), False)

    def test_str_subclasse_e_aceita(self):
        class S(str):
            pass

        self.assertTrue(validar_cpf(S("52998224725")))

    def test_retorna_bool_estrito(self):
        self.assertIs(validar_cpf("52998224725"), True)
        self.assertIs(validar_cpf("52998224724"), False)


class TestDeterminismoGerador(unittest.TestCase):
    def test_gerar_cpfs_mesma_seed_mesma_lista(self):
        a = gerar_cpfs(200, rng=random.Random(5))
        b = gerar_cpfs(200, rng=random.Random(5))
        self.assertEqual(a, b)

    def test_formatado_e_apenas_mascara_da_versao_numerica(self):
        n = gerar_cpf(rng=random.Random(8))
        f = gerar_cpf(formatado=True, rng=random.Random(8))
        self.assertEqual(f, _mascara(n))

    def test_rng_externo_e_consumido_e_nao_reiniciado(self):
        rng = random.Random(1)
        a, b = gerar_cpf(rng=rng), gerar_cpf(rng=rng)
        self.assertNotEqual(a, b)

    def test_nao_usa_estado_global_do_random(self):
        random.seed(1)
        x = gerar_cpf(rng=random.Random(42))
        random.seed(999)
        y = gerar_cpf(rng=random.Random(42))
        self.assertEqual(x, y)

    def test_gerados_validam_com_oraculo_e_validador_mascarado(self):
        for c in gerar_cpfs(3000, rng=random.Random(77)):
            self.assertTrue(_oraculo(c))
            self.assertTrue(validar_cpf(_mascara(c)))

    def test_unicos_false_permite_repeticao_sem_travar_e_tamanho_correto(self):
        self.assertEqual(len(gerar_cpfs(50, unicos=False, rng=random.Random(2))), 50)

    def test_quantidade_um(self):
        self.assertEqual(len(gerar_cpfs(1, rng=random.Random(2))), 1)

    def test_quantidade_invalida_de_tipo(self):
        with self.assertRaises(TypeError):
            gerar_cpfs("3")




class TestLimiteUnicos(unittest.TestCase):
    def test_quantidade_acima_do_maximo_unico_levanta_erro(self):
        from cpf.gerador import MAXIMO_UNICOS, gerar_cpfs

        with self.assertRaises(ValueError):
            gerar_cpfs(MAXIMO_UNICOS + 1)

    def test_sem_unicos_nao_aplica_limite_de_unicidade(self):
        from cpf.gerador import gerar_cpfs

        self.assertEqual(len(gerar_cpfs(10, unicos=False)), 10)


if __name__ == "__main__":
    unittest.main()
