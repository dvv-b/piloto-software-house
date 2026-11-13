# Módulo CPF (validador + gerador)

## Pedido original
Preciso de um módulo Python para trabalhar com CPF nos meus projetos:
uma função que valida CPF (formato e dígitos verificadores, aceitando com ou sem pontuação)
e um gerador de CPFs fictícios válidos para usar em testes.
Quero testes automatizados cobrindo bem os dois.
Delegue ao Codex as partes independentes pela orquestração da Alethe, porque isso faz parte do teste da equipe.

## Interpretação e plano
- Pacote `cpf/` (stdlib, unittest): `validar_cpf`, `gerar_cpf`, `gerar_cpfs`.
- T1 (Codex): validador + testes. T2 (Codex): gerador + testes (verificador independente nos testes).
- T3 (lead): `__init__.py`, teste de integração gerador→validador, QA e revisão.
- Sem GitHub remoto: registro aqui.
