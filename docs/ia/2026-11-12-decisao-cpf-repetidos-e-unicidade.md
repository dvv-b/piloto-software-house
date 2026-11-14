# Decisão: CPFs repetidos e limite de unicidade (módulo cpf)
- data: 2026-11-12
- contexto: módulo `cpf/` (validador + gerador de CPF fictício). Ver tarefa `tarefas/2026-11-12-modulo-cpf.md`.

## Decisões
1. **Rejeitar CPFs de dígitos repetidos** (000.000.000-00 ... 999.999.999-99). Os dígitos verificadores desses casos até conferem, mas são inválidos na prática. O validador (`cpf/validador.py`) os rejeita e o gerador (`cpf/gerador.py`) nunca os produz (a base de 9 dígitos repetidos é descartada).
2. **Limite de unicidade em `gerar_cpfs`**: com `unicos=True`, o máximo é `MAXIMO_UNICOS = 10**9 - 10` (10**9 bases de nove dígitos menos as 10 repetidas). Acima disso levanta `ValueError`, em vez de laço infinito.
3. Quantidade negativa levanta `ValueError`; zero retorna lista vazia.

## Lição
- Todo gerador com "valores únicos" precisa declarar o tamanho do espaço de valores e falhar cedo ao excedê-lo. O revisor achou que a primeira versão podia entrar em laço infinito.
- Ressalva: perto do limite o sorteio com descarte de repetidos fica muito lento (não há embaralhamento do espaço). Uso realista (milhares de CPFs) não é afetado. Decisão pendente: tratar o caso de quantidade próxima ao máximo só se surgir necessidade.
- CPFs gerados são fictícios, só para testes.

## Desempenho (gerar 1 milhão de CPFs únicos)
- data: 2026-11-12. Tarefa: `tarefas/2026-11-12-desempenho-gerador.md`.
- Gargalos medidos (cProfile): 51% em `randrange(10)` chamado 9x por CPF; 27% no cálculo dos dígitos verificadores (`sum`+genexpr+`zip`); ~15% em `join/map(str)`/listas. A unicidade (set) não era gargalo (479 colisões em 1M).
- Decisão: sortear **1 inteiro por CPF** (`randrange(10**9)`), dígitos verificadores por **tabelas pré-calculadas** (base em 3 blocos de 3 dígitos), laço de `gerar_cpfs` inline.
- **Os valores gerados para uma mesma semente mudaram** nesta versão (nenhum teste/doc dependia deles). Segue valendo: mesma semente → mesma sequência, e `gerar_cpfs(n)` == n chamadas de `gerar_cpf` com o mesmo rng.
- `unicos=False` não preenche mais o set; no modo formatado o set guarda a string final (sem cópia sem máscara).

| cenário (N=1M, Random(42)) | antes | depois |
|---|---|---|
| formatado=False | 10,85 s | 2,15 s (5,0x) |
| formatado=True | 11,54 s | 2,92 s (3,9x) |
| pico de memória (False) | 94,0 MB | 94,0 MB |
| pico de memória (True) | 149,0 MB | ~97 MB (medição do planejador) |

- Ressalva mantida: perto de `MAXIMO_UNICOS` o sorteio com descarte continua lento.
