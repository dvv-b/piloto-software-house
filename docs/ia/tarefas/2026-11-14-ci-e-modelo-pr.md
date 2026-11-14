# CI no GitHub, modelo de PR e formatar_cpf (demanda #8)

## Pedido original
Adicione ao projeto os testes automáticos no GitHub (CI) a partir do modelo da Software House e o modelo de Pull Request. Depois crie uma função formatar_cpf que recebe 11 dígitos e devolve no formato 000.000.000-00, com testes, usando só CPFs fictícios gerados pelo próprio módulo.

## Andamento
- T1 (#9) workflow `.github/workflows/testes.yml` com `unittest`: feita.
- T2 (#10) `.github/pull_request_template.md`; modelo de issue movido de `github/` para `.github/` (e atualizado ao modelo): feita.
- T3 (#11) `formatar_cpf` já existia na main (PR #7); conferido, nada a recriar: feita.
- Decisão: modelo usava pytest; o projeto usa só `unittest`, então o CI roda `python -m unittest discover -s tests -t .`.
- Próximo passo: CI verde no PR, depois Revisão e merge pelo Bruno.
