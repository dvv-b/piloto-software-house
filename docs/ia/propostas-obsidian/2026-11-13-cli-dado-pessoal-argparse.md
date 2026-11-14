# Proposta de nota global: CLI que recebe dado pessoal (argparse ecoa a entrada)
- data: 2026-11-13
- status: aguardando aprovação do Bruno
- origem: retrospectiva da CLI do módulo cpf (projeto piloto-software-house)
- alvo sugerido: skill dados-pessoais-lgpd

## Proposta 1: argparse repete o valor digitado
Mensagens do argparse (invalid choice, invalid int value) incluem o valor recebido, vazando dado pessoal em terminal e logs. Usar um parser que sobrescreve `error()` com mensagem fixa, sem ecoar a entrada.

## Proposta 2: stdin com limite e sem traceback
Ler stdin com tamanho máximo e tratar entrada inválida (bytes não UTF-8) com mensagem fixa e código de saída definido, nunca com traceback.

## Proposta 3: UTF-8 explícito no Windows
Com pipe, o Python no Windows usa cp1252 e corrompe acentos. Fixar UTF-8 nos fluxos de saída da CLI.

## Proposta 4: teste hostil de segurança
Pedir ao agente de segurança que execute a CLI de forma hostil (entradas inválidas, stdin enorme ou binário). Achou 3 falhas que testes comuns não pegariam.

## Proposta 5: edição de arquivos
Para texto com `\` e acentos, usar a ferramenta Edit, não script Python em heredoc (escapes foram interpretados e quebraram arquivos). Não editar arquivos enquanto qa/revisor os leem.
