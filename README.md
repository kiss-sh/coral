# coral - transpilador de python para javascript

### projeto para a disciplina de compiladores
membros:
--------
* [Gabriel Jales](https://github.com/gabrieljales)
* [jefferson Ximenes](https://github.com/jeffersonximeness)
* [Jonas Rodrigues](https://github.com/jonis69)
* [Marcos Fonseca](https://github.com/marcosfnsc)

Como usar o transpiler:
```console
$ ./coral <codigo.py>
```
caso um arquivo não seja passado como argumento, o transpiler vai entrar
em um modo shell, que permite testar a conversão de algumas intruções
sem precisar criar um arquivo, esse modo é mais limitado pois não
pode criar blocos de codigo

O transpiler dá suporte a um subconjunto da linguagem python, suporta tipos
primitvos como strings, ints, floats, bools, None e funções embutidas como print,
blocos de codigos suportados são if, elif, else e while

Estrutura do projeto:
```
.
├── coral               # codigo principal
├── examples            # exemplos de codigo testado no transpiler
│   └── ex0.py
├── generation_code.py  # responsavel por juntar os tokens e 'deixar' legivel
├── lexer.py            # analisa um arquivo ou entrada do usuario e gera uma lista de tokens
├── LICENSE
├── parser.py           # analisa a lista de tokens e faz alterações necessarias
├── README.md
└── unit_tests.py       # testes unitários, úteis somente durante o desemvolvimento
```
