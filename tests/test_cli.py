"""Testes da linha de comando (python -m cpf)."""

import contextlib
import io
import os
import random
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from cpf.cli import MAXIMO_CLI, main
from cpf.gerador import gerar_cpf
from cpf.validador import validar_cpf

RAIZ = Path(__file__).resolve().parent.parent
MASCARA = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")


def _executar(*argv: str, stdin: str = "") -> tuple[int, str, str]:
    saida, erro = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
        with mock.patch("sys.stdin", io.StringIO(stdin)):
            codigo = main(list(argv))
    return codigo, saida.getvalue(), erro.getvalue()


class ValidarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cpf = gerar_cpf(rng=random.Random(21))  # fictício

    def test_valido_por_argumento_e_por_stdin(self) -> None:
        self.assertEqual(_executar("validar", self.cpf), (0, "válido\n", ""))
        self.assertEqual(_executar("validar", stdin=self.cpf + "\n")[:2], (0, "válido\n"))
        self.assertEqual(_executar("validar", "-", stdin=self.cpf)[:2], (0, "válido\n"))

    def test_invalido_dv_alterado_e_repetido(self) -> None:
        errado = self.cpf[:-1] + str((int(self.cpf[-1]) + 1) % 10)
        for valor in (errado, "111.111.111-11"):
            with self.subTest(valor=valor):
                self.assertEqual(_executar("validar", valor)[:2], (1, "inválido\n"))

    def test_nao_ecoa_o_cpf(self) -> None:
        _, saida, erro = _executar("validar", self.cpf)
        self.assertNotIn(self.cpf, saida + erro)

    def test_entrada_vazia_e_uso_incorreto(self) -> None:
        codigo, saida, erro = _executar("validar", stdin="  \n")
        self.assertEqual((codigo, saida), (2, ""))
        self.assertIn("erro:", erro)


class FormatarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cpf = gerar_cpf(rng=random.Random(22))  # fictício
        self.mascarado = f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def test_com_e_sem_mascara_dao_a_mesma_saida(self) -> None:
        for entrada in (self.cpf, self.mascarado):
            self.assertEqual(_executar("formatar", entrada), (0, self.mascarado + "\n", ""))

    def test_por_stdin(self) -> None:
        self.assertEqual(_executar("formatar", stdin=self.cpf)[:2], (0, self.mascarado + "\n"))

    def test_formato_invalido_nao_ecoa_a_entrada(self) -> None:
        entrada = self.cpf[:9]
        codigo, saida, erro = _executar("formatar", entrada)
        self.assertEqual((codigo, saida), (1, ""))
        self.assertIn("erro: formato inválido", erro)
        self.assertNotIn(entrada, erro)

    def test_entrada_vazia(self) -> None:
        self.assertEqual(_executar("formatar", stdin="")[0], 2)


class GerarTest(unittest.TestCase):
    def test_padrao_gera_um(self) -> None:
        codigo, saida, _ = _executar("gerar")
        self.assertEqual(codigo, 0)
        self.assertEqual(len(saida.splitlines()), 1)

    def test_quantidade_unicos_e_validos(self) -> None:
        _, saida, _ = _executar("gerar", "50")
        linhas = saida.splitlines()
        self.assertEqual(len(set(linhas)), 50)
        self.assertTrue(all(validar_cpf(c) for c in linhas))

    def test_formatado(self) -> None:
        _, saida, _ = _executar("gerar", "5", "-f")
        self.assertTrue(all(MASCARA.fullmatch(c) for c in saida.splitlines()))

    def test_mesma_semente_repete_a_saida(self) -> None:
        a = _executar("gerar", "10", "--semente", "7")
        b = _executar("gerar", "10", "--semente", "7")
        c = _executar("gerar", "10", "--semente", "8")
        self.assertEqual(a, b)
        self.assertNotEqual(a[1], c[1])

    def test_zero_nao_imprime_nada(self) -> None:
        self.assertEqual(_executar("gerar", "0"), (0, "", ""))

    def test_quantidade_fora_da_faixa_ou_invalida(self) -> None:
        for valor in ("-1", str(MAXIMO_CLI + 1), "abc", "2.5"):
            with self.subTest(valor=valor):
                self.assertEqual(_executar("gerar", valor)[0], 2)

    def test_limite_superior_rejeitado_com_mensagem(self) -> None:
        codigo, saida, erro = _executar("gerar", str(MAXIMO_CLI + 1))
        self.assertEqual((codigo, saida), (2, ""))
        self.assertIn(f"entre 0 e {MAXIMO_CLI}", erro)


class ArgumentosTest(unittest.TestCase):
    def test_ajuda_e_comando_ausente_devolvem_codigo(self) -> None:
        self.assertEqual(_executar("--help")[0], 0)
        self.assertEqual(_executar()[0], 2)
        self.assertEqual(_executar("inexistente")[0], 2)


class ProcessoTest(unittest.TestCase):
    """Executa ``python -m cpf`` de verdade (entrada, saída e código)."""

    def _rodar(self, *argv: str, entrada: str = "") -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "cpf", *argv],
            input=entrada, capture_output=True, text=True, encoding="utf-8",
            cwd=RAIZ, env={**os.environ, "PYTHONIOENCODING": ""}, timeout=30,
        )

    def test_gerar_e_validar_em_sequencia(self) -> None:
        gerado = self._rodar("gerar", "3", "--semente", "1")
        self.assertEqual(gerado.returncode, 0)
        cpfs = gerado.stdout.split()
        self.assertEqual(len(cpfs), 3)
        validado = self._rodar("validar", entrada=cpfs[0])
        self.assertEqual((validado.returncode, validado.stdout.strip()), (0, "válido"))

    def test_invalido_sai_com_codigo_1(self) -> None:
        resultado = self._rodar("validar", "111.111.111-11")
        self.assertEqual((resultado.returncode, resultado.stdout.strip()), (1, "inválido"))

    def test_entrada_que_nao_e_utf8_nao_gera_traceback(self) -> None:
        resultado = subprocess.run(
            [sys.executable, "-m", "cpf", "validar"],
            input=b"\xff\xfe", capture_output=True, cwd=RAIZ, timeout=30,
        )
        self.assertEqual(resultado.returncode, 1)
        self.assertNotIn(b"Traceback", resultado.stderr)

    def test_argparse_nao_ecoa_o_valor_digitado(self) -> None:
        fake = gerar_cpf(rng=random.Random(31))  # fictício
        for argv in ([fake], ["gerar", fake + "x"], ["gerar", "--semente", fake + "a"],
                     ["validar", fake, fake], ["validar", "--" + fake]):
            with self.subTest(argv=argv[:1]):
                codigo, saida, erro = _executar(*argv)
                self.assertEqual(codigo, 2)
                self.assertNotIn(fake, saida + erro)

    def test_entrada_enorme_e_limitada(self) -> None:
        codigo, saida, _ = _executar("validar", stdin="1" * 5_000_000)
        self.assertEqual((codigo, saida), (1, "inválido\n"))

    def test_gerar_em_processo_confere_o_readme(self) -> None:
        resultado = self._rodar("gerar", "2", "--semente", "1", "-f")
        self.assertEqual(resultado.returncode, 0)
        self.assertEqual(
            resultado.stdout.split(), ["144.272.509-55", "611.178.002-61"]
        )

    def test_varias_linhas_contam_como_um_unico_valor(self) -> None:
        resultado = self._rodar("validar", entrada="14427250955\n61117800261\n")
        self.assertEqual((resultado.returncode, resultado.stdout.strip()), (1, "inválido"))

    def test_formatar(self) -> None:
        resultado = self._rodar("formatar", entrada="11111111111")
        self.assertEqual((resultado.returncode, resultado.stdout.strip()), (0, "111.111.111-11"))


if __name__ == "__main__":
    unittest.main()
