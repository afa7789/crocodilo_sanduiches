import json

def update_json(arquivo_antigo, arquivo_novo, arquivo_atualizado):
    # Passo 1: Ler os arquivos JSON
    with open(arquivo_antigo, 'r', encoding='utf-8') as f:
        crocodilo_json = json.load(f)
    
    with open(arquivo_novo, 'r', encoding='utf-8') as f:
        new_ingredients_json = json.load(f)
        new_ingredients = new_ingredients_json["ingredients"]  # Access the "ingredients" array

    # Passo 2: Criar mapeamento de índices antigos para novos com base na posição no novo JSON
    index_mapping = {}
    for old_ing in crocodilo_json["ingredients"]:
        old_index = old_ing["index"]
        old_name = old_ing["name"]
        # Encontrar a posição do ingrediente no novo JSON
        for new_pos, new_ing in enumerate(new_ingredients):
            if new_ing["name"] == old_name:
                index_mapping[old_index] = new_pos  # Usar a posição como novo índice
                break
        else:
            raise ValueError(f"Ingrediente '{old_name}' não encontrado no novo JSON")

    # Passo 3: Atualizar os índices nos burgers
    for burger in crocodilo_json["burgers"]:
        burger["ingredients"] = [index_mapping[old_index] for old_index in burger["ingredients"]]

    # Passo 4: Reorganizar o array ingredients para seguir a ordem do novo JSON
    crocodilo_json["ingredients"] = [
        {"index": i, "name": ing["name"]} for i, ing in enumerate(new_ingredients)
    ]

    # Passo 5: Ordenar os burgers pelo campo 'number'
    crocodilo_json["burgers"] = sorted(crocodilo_json["burgers"], key=lambda x: x["number"])

    # Passo 6: Padronizar os preços para o formato "R$X,00"
    for burger in crocodilo_json["burgers"]:
        if isinstance(burger["price"], float):
            burger["price"] = f"R${burger['price']:.2f}".replace(".", ",")
        elif isinstance(burger["price"], int):
            burger["price"] = f"R${burger['price']},00"
        elif isinstance(burger["price"], str):
            # Remover "R$" e garantir formato "R$X,00"
            price_num = float(burger["price"].replace("R$", "").replace(",", "."))
            burger["price"] = f"R${price_num:.2f}".replace(".", ",")

    # Passo 7: Escrever o JSON atualizado no arquivo_atualizado
    with open(arquivo_atualizado, 'w', encoding='utf-8') as f:
        json.dump(crocodilo_json, f, indent=2, ensure_ascii=False)

    print(f"Arquivo atualizado salvo em: {arquivo_atualizado}")

# Exemplo de uso
if __name__ == "__main__":
    arquivo_antigo = "crocodilo_sanduiches.json"
    arquivo_novo = "new_ingredients_order.json"
    arquivo_atualizado = "updated_crocodilo_sanduiches.json"
    update_json(arquivo_antigo, arquivo_novo, arquivo_atualizado)