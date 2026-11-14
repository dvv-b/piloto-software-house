"""Utilitários de CPF: validação e geração de CPFs fictícios para testes."""

from cpf.gerador import gerar_cpf, gerar_cpfs
from cpf.validador import validar_cpf

__all__ = ["validar_cpf", "gerar_cpf", "gerar_cpfs"]
