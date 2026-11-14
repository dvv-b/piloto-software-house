# Desempenho do gerador de CPFs (1 milhão únicos)

## Pedido original
Analise o desempenho do gerador de CPFs para gerar 1 milhão de CPFs únicos e otimize o que for gargalo.

## Interpretação e plano
- Medir `gerar_cpfs(1_000_000)`, otimizar gargalos preservando API, unicidade e exclusão dos 10 repetidos.
- T1 (líder): reescrever núcleo de `cpf/gerador.py`. T2 (líder): testes novos. T3 (líder): registro da decisão.
- Validação: qa + revisor. Resultado e números em `docs/ia/2026-11-12-decisao-cpf-repetidos-e-unicidade.md` (seção Desempenho).
