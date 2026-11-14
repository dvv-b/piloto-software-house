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
