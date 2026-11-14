# Proposta de nota global: checklist para delegar ao Codex (Alethe)
- data: 2026-11-12
- status: aguardando aprovação do Bruno
- origem: retrospectiva do módulo CPF (projeto piloto-software-house)

## Proposta 1: antes de usar isolate, garantir commit inicial
Repositório sem commits tem HEAD inválido e o isolate falha. Checar `git rev-parse HEAD` antes de delegar com isolate; se falhar, criar o commit inicial (com autorização).

## Proposta 2: worker sem interpretador
No brief padrão, incluir: "se não achar Python (ou outro runtime), reporte e não tente instalar; o lead executa os testes". O lead roda os testes e registra o resultado.

## Proposta 3: briefs de geradores definem o espaço de valores
Todo brief de gerador com opção de unicidade deve exigir: tamanho do espaço de valores, limite máximo e erro explícito ao excedê-lo (evita laço infinito).

## Proposta 4: contrato de interface fechado no brief
Fechar assinaturas e comportamento de erro no brief permite workers em paralelo sem conflito. Funcionou bem; verificador independente nos testes + oráculo do QA aumentaram a confiança.
