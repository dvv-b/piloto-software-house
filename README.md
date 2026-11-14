# piloto-software-house

Módulo `cpf/` em Python (somente biblioteca padrão): validação de CPF, formatação
e gerador de CPFs **fictícios** válidos, para uso em testes. Há também uma
[linha de comando](#linha-de-comando).

## Como testar

```
python -m unittest discover -s tests -t .
```

## Uso como biblioteca

```python
from cpf import validar_cpf, formatar_cpf, gerar_cpf, gerar_cpfs

gerar_cpf()                 # ex.: '31071466844'
formatar_cpf("14427250955") # '144.272.509-55'
validar_cpf("144.272.509-55")  # True
gerar_cpfs(3, formatado=True)  # 3 CPFs únicos
```

## Linha de comando

Rode a partir da raiz do projeto: `python -m cpf <comando>`. Nada a instalar.

### `validar [CPF]`

Diz se um CPF é válido (com ou sem pontuação). Imprime só `válido` ou `inválido`;
**nunca repete o CPF recebido**. Os 10 CPFs de dígitos repetidos são inválidos.

```
$ python -m cpf validar 144.272.509-55
válido
$ python -m cpf validar 144.272.509-56
inválido
```

### `formatar [CPF]`

Coloca a pontuação `000.000.000-00`. Aceita 11 dígitos ou um CPF já formatado
(devolve igual). **Só confere o formato, não os dígitos verificadores** (para isso
use `validar`). Outros formatos (9 ou 10 dígitos, letras etc.) são rejeitados.

```
$ python -m cpf formatar 14427250955
144.272.509-55
```

### `gerar [N] [-f] [--semente INT]`

Gera `N` CPFs fictícios, válidos e únicos, um por linha (padrão: 1; de 0 a
1.000.000). `-f`/`--formatado` coloca a pontuação. Com a mesma `--semente`, a saída
se repete.

```
$ python -m cpf gerar 3 --semente 1
14427250955
61117800261
90992504791
$ python -m cpf gerar 2 --semente 1 -f
144.272.509-55
611.178.002-61
```

### Entrada padrão e dados pessoais

Em `validar` e `formatar`, sem argumento (ou com `-`) o CPF é lido da entrada
padrão (no máximo 4096 caracteres). **Para CPFs possivelmente reais, não passe o
CPF como argumento**: ele fica no histórico do shell e na lista de processos.
Prefira digitar quando o comando esperar (encerre com Ctrl+Z e Enter no Windows,
Ctrl+D no Unix) ou redirecionar de um arquivo (`< arquivo.txt`). Evite também
`echo CPF | ...`, que grava o CPF no histórico. Nenhuma mensagem de erro repete o
valor digitado, e a CLI não grava logs nem arquivos. Entrada que não seja texto
UTF-8 válido é tratada como CPF inválido. A entrada é **um único CPF**: um texto
com várias linhas conta como um valor só (e dá `inválido`).

```
$ python -m cpf gerar --semente 1 | python -m cpf validar
válido
```

### Códigos de saída

| código | significado |
|---|---|
| 0 | sucesso (`validar`: CPF válido) |
| 1 | resultado negativo (`validar`: inválido; `formatar`: formato inválido) |
| 2 | uso incorreto (entrada vazia, `N` fora de 0 a 1.000.000, argumentos inválidos) |

No Windows, a saída usa fim de linha CRLF; ao capturar a saída em scripts bash,
remova o caractere `\r` final.

> Todos os CPFs gerados são fictícios. Não use CPFs reais em testes, exemplos ou docs.
