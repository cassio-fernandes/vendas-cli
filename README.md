
# Vendas-cli - Gerador de Relatório de Vendas Avançado

## instruções

### Instalação

Instale o pacote localmente com pip:

```
pip install .
```

### Uso

Executar o comando `vendas-cli` para ler um arquivo CSV e gerar o relatório.

Exemplos:

```
vendas-cli read <path-to-csv>
vendas-cli read <path-to-csv> --format json
```
ou
```
vendas-cli read <path-to-csv> --format text
```

** 'text' é formato padrão, isto é, caso não seja passado o parâmetro --format, será retornado o resultado em text (tabular)
