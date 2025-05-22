### README

#### Arquivos

- **crocodilo_sanduiches.json**: JSON original com a lista de sanduíches e seus ingredientes.
- **new_ingredients_order.json**: JSON com a nova ordem dos ingredientes para reindexação.
- **updated_crocodilo_sanduiches.json**: JSON gerado com os sanduíches reindexados e ordenados.
- **reorder.py**: Script Python que atualiza os índices dos ingredientes nos sanduíches com base na nova ordem e salva o resultado.
- **crocodilo.py**: Script Python que analisa os sanduíches, calculando custo-benefício, comparando ingredientes e gerando estatísticas.

#### Como Rodar

1. Certifique-se de ter o Python 3 instalado.
2. Coloque os arquivos `crocodilo_sanduiches.json` e `new_ingredients_order.json` na mesma pasta dos scripts.
3. Para reindexar os sanduíches:
   ```bash
   python3 reorder.py
   ```
   - Gera `updated_crocodilo_sanduiches.json` com os índices atualizados.
4. Para analisar os sanduíches:
   ```bash
   python3 crocodilo.py
   ```
   - Gera um relatório com custo-benefício, comparação de ingredientes e estatísticas.


# README

## Arquivos

- **crocodilo_sanduiches.json**: JSON original com a lista de sanduíches e seus ingredientes.
- **new_ingredients_order.json**: JSON com a nova ordem dos ingredientes para reindexação.
- **updated_crocodilo_sanduiches.json**: JSON gerado com os sanduíches reindexados e ordenados.
- **reorder.py**: Script Python que atualiza os índices dos ingredientes nos sanduíches com base na nova ordem e salva o resultado.
- **crocodilo.py**: Script Python que analisa os sanduíches, calculando custo-benefício, comparando ingredientes e gerando estatísticas.

## Como Rodar

1. Certifique-se de ter o Python 3 instalado.
2. Coloque os arquivos `crocodilo_sanduiches.json` e `new_ingredients_order.json` na mesma pasta dos scripts.
3. Para reindexar os sanduíches:
   ```bash
   python3 reorder.py
   ```
   - Gera `updated_crocodilo_sanduiches.json` com os índices atualizados.
4. Para analisar os sanduíches:
   ```bash
   python3 crocodilo.py
   ```
   - Gera um relatório com custo-benefício, comparação de ingredientes e estatísticas.
