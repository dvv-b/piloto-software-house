# Regras do projeto: piloto-software-house

> Regras específicas deste projeto. As regras gerais da Software House já valem
> (instaladas globalmente); aqui entra só o que é deste projeto.

## O que é
Piloto da Software House. Contém o módulo `cpf/` (Python, só biblioteca padrão): validação de CPF (`validar_cpf`) e gerador de CPFs fictícios válidos para testes (`gerar_cpf`, `gerar_cpfs`).

## Stack e comandos
- Linguagem/framework: Python 3.12, somente biblioteca padrão (`unittest`; pytest não está instalado)
- Instalar: nada a instalar
- Rodar: `from cpf import validar_cpf, gerar_cpf` (a partir da raiz do projeto)
- CLI: `python -m cpf <validar|gerar|formatar>` (uso detalhado no README.md da raiz)
- Testar: `python -m unittest discover -s tests -t .`

## Regras do projeto
- CPFs em testes, exemplos e docs são sempre fictícios (use o gerador); nunca CPF real.
- Os 10 CPFs de dígitos repetidos são sempre inválidos (no validador) e nunca gerados.
- Docstrings e mensagens em português; testes do gerador não importam o validador (verificador independente).

## Documentação
- Para pessoas: `docs/humano/`
- Para agentes: `docs/ia/` (decisões, lições, tarefas, retrospectivas)
- Decisões de arquitetura: `docs/adr/`
