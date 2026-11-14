"""Linha de comando do módulo cpf: validar, gerar e formatar."""

import argparse
import random
import sys
from collections.abc import Sequence

from cpf.formatador import formatar_cpf
from cpf.gerador import gerar_cpfs
from cpf.validador import validar_cpf

MAXIMO_CLI = 1_000_000

SUCESSO = 0
NEGATIVO = 1
USO_INCORRETO = 2


# Um CPF tem no máximo 14 caracteres; ler mais que isso só gasta memória.
_LIMITE_ENTRADA = 4096


class _Parser(argparse.ArgumentParser):
    """Parser cujos erros nunca repetem o que foi digitado (pode ser um CPF)."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        _erro("argumentos inválidos (use --help)")
        raise SystemExit(USO_INCORRETO)


def _ler_cpf(argumento: str | None) -> str | None:
    """Lê o CPF do argumento ou, se ausente ou ``-``, de toda a entrada padrão.

    Devolve ``None`` quando a entrada está vazia.
    """
    texto = sys.stdin.read(_LIMITE_ENTRADA) if argumento in (None, "-") else argumento
    texto = texto.strip()
    return texto or None


def _erro(mensagem: str) -> None:
    print(f"erro: {mensagem}", file=sys.stderr)


def _cmd_validar(args: argparse.Namespace) -> int:
    valor = _ler_cpf(args.cpf)
    if valor is None:
        _erro("nenhum CPF informado")
        return USO_INCORRETO
    # Nunca ecoa o CPF recebido (pode ser dado pessoal real).
    if validar_cpf(valor):
        print("válido")
        return SUCESSO
    print("inválido")
    return NEGATIVO


def _cmd_formatar(args: argparse.Namespace) -> int:
    valor = _ler_cpf(args.cpf)
    if valor is None:
        _erro("nenhum CPF informado")
        return USO_INCORRETO
    try:
        print(formatar_cpf(valor))
    except ValueError as exc:
        _erro(str(exc))
        return NEGATIVO
    return SUCESSO


def _cmd_gerar(args: argparse.Namespace) -> int:
    if not 0 <= args.quantidade <= MAXIMO_CLI:
        _erro(f"a quantidade deve estar entre 0 e {MAXIMO_CLI}")
        return USO_INCORRETO
    rng = random.Random(args.semente) if args.semente is not None else None
    cpfs = gerar_cpfs(args.quantidade, formatado=args.formatado, rng=rng)
    if cpfs:
        try:
            sys.stdout.write("\n".join(cpfs) + "\n")
            sys.stdout.flush()
        except BrokenPipeError:
            # Leitor encerrou antes (ex.: `| head`); não é erro.
            pass
    return SUCESSO


def _criar_parser() -> argparse.ArgumentParser:
    parser = _Parser(
        prog="python -m cpf",
        description="Valida, formata e gera CPFs (os gerados são fictícios, "
        "somente para testes).",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    validar = sub.add_parser("validar", help="diz se um CPF é válido")
    validar.add_argument(
        "cpf", nargs="?",
        help="CPF com ou sem pontuação; se ausente ou '-', lê da entrada padrão "
        "(prefira a entrada padrão para CPFs reais: o argumento fica no "
        "histórico do shell)",
    )
    validar.set_defaults(funcao=_cmd_validar)

    formatar = sub.add_parser("formatar", help="coloca a pontuação 000.000.000-00")
    formatar.add_argument(
        "cpf", nargs="?",
        help="11 dígitos ou já formatado; se ausente ou '-', lê da entrada padrão",
    )
    formatar.set_defaults(funcao=_cmd_formatar)

    gerar = sub.add_parser("gerar", help="gera CPFs fictícios únicos e válidos")
    gerar.add_argument(
        "quantidade", nargs="?", type=int, default=1,
        help=f"quantos CPFs gerar, de 0 a {MAXIMO_CLI} (padrão: 1)",
    )
    gerar.add_argument(
        "-f", "--formatado", action="store_true", help="com pontuação"
    )
    gerar.add_argument(
        "--semente", type=int, help="semente: a mesma semente repete a saída"
    )
    gerar.set_defaults(funcao=_cmd_gerar)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a CLI e devolve o código de saída (0, 1 ou 2)."""
    try:
        args = _criar_parser().parse_args(argv)
    except SystemExit as saida:
        return saida.code if isinstance(saida.code, int) else USO_INCORRETO
    return args.funcao(args)
