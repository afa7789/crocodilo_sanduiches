import json
from collections import defaultdict

def create_bitmask(ingredients):
    """Cria bitmask para representar ingredientes de um sanduíche"""
    mask = 0
    for i in ingredients:
        if 0 <= i <= 18:
            mask |= (1 << i)
    return mask

def calculate_ingredient_weight(ingredients):
    """Calcula peso dos ingredientes de forma normalizada"""
    # Opção 1: Soma simples dos índices (ingredientes com índice maior = mais especiais)
    simple_sum = sum(ingredients) if ingredients else 0
    
    # Opção 2: Logarítmica - suaviza o crescimento exponencial do bitmask
    import math
    log_weight = sum(math.log2(i + 1) for i in ingredients) if ingredients else 0
    
    # Opção 3: Peso por "raridade" - ingredientes com índice maior são mais raros
    rarity_weight = sum((i + 1) * 0.1 for i in ingredients) if ingredients else 0
    
    return {
        'simple': simple_sum,
        'logarithmic': log_weight,
        'rarity': rarity_weight
    }

def normalize_price(price):
    """Normaliza preços que podem estar em diferentes formatos"""
    if isinstance(price, str):
        # Remove "R$" e vírgulas, converte para float
        price_clean = price.replace("R$", "").replace(",", ".").strip()
        return float(price_clean)
    return float(price)

def calculate_price_per_ingredient(sandwich):
    """Calcula preço por ingrediente de um sanduíche"""
    price = normalize_price(sandwich.get("price", 0))
    num_ingredients = len(sandwich.get("ingredients", []))
    
    if num_ingredients == 0:
        return float('inf')
    
    return price / num_ingredients

def get_ingredient_name(ingredient_index, ingredients_data):
    """Retorna o nome do ingrediente pelo índice"""
    for ingredient in ingredients_data:
        if ingredient.get("index") == ingredient_index:
            return ingredient.get("name", f"Ingrediente {ingredient_index}")
    return f"Ingrediente {ingredient_index}"

def format_ingredients_list(ingredients, ingredients_data):
    """Formata lista de ingredientes com nomes"""
    ingredient_names = []
    for idx in ingredients:
        name = get_ingredient_name(idx, ingredients_data)
        ingredient_names.append(name)
    return ", ".join(ingredient_names)

def compare_bitmasks(mask1, mask2, ingredients_data):
    """Compara dois bitmasks e mostra diferenças"""
    common = mask1 & mask2
    only_in_first = mask1 & ~mask2
    only_in_second = mask2 & ~mask1
    
    result = {
        'common_ingredients': [],
        'only_in_first': [],
        'only_in_second': []
    }
    
    # Ingredientes em comum
    for i in range(19):
        if common & (1 << i):
            result['common_ingredients'].append(get_ingredient_name(i, ingredients_data))
    
    # Apenas no primeiro
    for i in range(19):
        if only_in_first & (1 << i):
            result['only_in_first'].append(get_ingredient_name(i, ingredients_data))
    
    # Apenas no segundo
    for i in range(19):
        if only_in_second & (1 << i):
            result['only_in_second'].append(get_ingredient_name(i, ingredients_data))
    
    return result

def main():
    # Carrega dados do arquivo JSON
    try:
        with open("crocodilo_sanduiches.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'crocodilo_sanduiches.json' não encontrado!")
        return
    
    if isinstance(data, dict):
        sandwiches = data.get("burgers", [])
        ingredients_data = data.get("ingredients", [])
    else:
        sandwiches = data
        ingredients_data = []
    
    print("=" * 80)
    print("RELATÓRIO DE ANÁLISE DOS SANDUÍCHES CROCODILO")
    print("=" * 80)
    
    # 1. Análise de preço por ingrediente
    print("\n📊 ANÁLISE DE CUSTO-BENEFÍCIO (Preço por Ingrediente)")
    print("-" * 60)
    
    sandwiches_with_ratio = []
    for sandwich in sandwiches:
        name = sandwich.get("name", "Sem nome")
        price = normalize_price(sandwich.get("price", 0))
        ingredients = sandwich.get("ingredients", [])
        ratio = calculate_price_per_ingredient(sandwich)
        
        sandwiches_with_ratio.append({
            'name': name,
            'price': price,
            'num_ingredients': len(ingredients),
            'price_per_ingredient': ratio,
            'ingredients': ingredients
        })
    
    # Ordena por melhor custo-benefício (menor preço por ingrediente)
    sandwiches_with_ratio.sort(key=lambda x: x['price_per_ingredient'])
    
    print(f"{'Posição':<3} {'Sanduíche':<25} {'Preço':<8} {'Ingred.':<7} {'R$/Ingred.':<10}")
    print("-" * 60)
    
    for i, sandwich in enumerate(sandwiches_with_ratio[:10], 1):
        print(f"{i:<3} {sandwich['name'][:24]:<25} "
              f"R${sandwich['price']:<7.2f} {sandwich['num_ingredients']:<7} "
              f"R${sandwich['price_per_ingredient']:<9.2f}")
    
    # Destaque do melhor custo-benefício
    best_value = sandwiches_with_ratio[0]
    print(f"\n🏆 MELHOR CUSTO-BENEFÍCIO: {best_value['name']}")
    print(f"   Preço: R${best_value['price']:.2f}")
    print(f"   Ingredientes: {best_value['num_ingredients']}")
    print(f"   Custo por ingrediente: R${best_value['price_per_ingredient']:.2f}")
    
    # 2. Análise de Bitmasks - Sanduíches ordenados por ingredientes
    print("\n🔍 SANDUÍCHES ORDENADOS POR BITMASK (Iguais ficam juntos)")
    print("-" * 60)
    
    # Cria lista com sanduíches e seus bitmasks
    sandwich_bitmasks = []
    for sandwich in sandwiches:
        name = sandwich.get("name", "Sem nome")
        ingredients = sandwich.get("ingredients", [])
        mask = create_bitmask(ingredients)
        price = normalize_price(sandwich.get("price", 0))
        
        sandwich_bitmasks.append({
            'name': name,
            'mask': mask,
            'ingredients': ingredients,
            'price': price,
            'num_ingredients': len(ingredients),
            'weights': calculate_ingredient_weight(ingredients)
        })
    
    # Ordena por bitmask - sanduíches iguais ficarão juntos automaticamente!
    sandwich_bitmasks.sort(key=lambda x: x['mask'])
    
    # Calcula ranking baseado em preço/ingrediente
    for sandwich in sandwich_bitmasks:
        sandwich['price_per_ingredient'] = sandwich['price'] / sandwich['num_ingredients'] if sandwich['num_ingredients'] > 0 else float('inf')
    
    # Cria ranking ordenado por melhor custo-benefício
    ranking_by_value = sorted(sandwich_bitmasks, key=lambda x: x['price_per_ingredient'])
    
    # Adiciona posição no ranking para cada sanduíche
    for i, sandwich in enumerate(ranking_by_value):
        sandwich['rank'] = i + 1
    
    print(f"{'Bitmask':<20} {'Valor':<8} {'PesoLog':<8} {'Sanduíche':<25} {'Preço':<8} {'Ingred.':<7} {'Rank':<5}")
    print("-" * 86)
    
    previous_mask = None
    
    for sandwich in sandwich_bitmasks:
        mask_str = f"{sandwich['mask']:019b}"
        mask_value = sandwich['mask']
        log_weight = sandwich['weights']['logarithmic']
        
        # Marca sanduíches com mesmo bitmask
        if previous_mask == sandwich['mask']:
            marker = " ⚠️ IGUAL!"
        else:
            marker = ""
        
        print(f"{mask_str:<20} {mask_value:<8} {log_weight:<8.2f} {sandwich['name'][:24]:<25} "
              f"R${sandwich['price']:<7.2f} {sandwich['num_ingredients']:<7} #{sandwich['rank']:<4}{marker}")
        
        previous_mask = sandwich['mask']
    
    # Adiciona análise dos pesos
    print("\n🔬 ANÁLISE DE PESOS DOS INGREDIENTES")
    print("-" * 50)
    print("💡 Peso Logarítmico: Normaliza o crescimento exponencial do bitmask")
    print("   - Ingredientes com índice maior = mais 'especiais'")
    print("   - log₂(ingrediente + 1) suaviza diferenças extremas")
    print()
    
    # Top 5 por peso logarítmico
    by_log_weight = sorted(sandwich_bitmasks, key=lambda x: x['weights']['logarithmic'], reverse=True)
    print("🏆 TOP 5 - Ingredientes mais 'especiais' (Peso Logarítmico):")
    for i, sandwich in enumerate(by_log_weight[:5], 1):
        weights = sandwich['weights']
        print(f"{i}. {sandwich['name'][:30]}: "
              f"Peso={weights['logarithmic']:.2f}, "
              f"Soma={weights['simple']:.0f}, "
              f"Raridade={weights['rarity']:.2f}")
    
    # 3. Comparação específica entre sanduíches populares
    print("\n🔄 COMPARAÇÃO ENTRE SANDUÍCHES POPULARES")
    print("-" * 60)
    
    # Pega alguns sanduíches para comparar
    popular_sandwiches = ["X TUDO", "CROCODILO", "HAMBURGÃO"]
    comparison_data = {}
    
    for sandwich in sandwiches:
        name = sandwich.get("name", "")
        if name in popular_sandwiches:
            comparison_data[name] = {
                'mask': create_bitmask(sandwich.get("ingredients", [])),
                'ingredients': sandwich.get("ingredients", []),
                'price': normalize_price(sandwich.get("price", 0))
            }
    
    if len(comparison_data) >= 2:
        sandwich_names = list(comparison_data.keys())
        for i in range(len(sandwich_names)):
            for j in range(i + 1, len(sandwich_names)):
                name1, name2 = sandwich_names[i], sandwich_names[j]
                
                print(f"\nComparando: {name1} vs {name2}")
                comparison = compare_bitmasks(
                    comparison_data[name1]['mask'],
                    comparison_data[name2]['mask'],
                    ingredients_data
                )
                
                print(f"Ingredientes em comum ({len(comparison['common_ingredients'])}): ")
                print(f"  {', '.join(comparison['common_ingredients']) if comparison['common_ingredients'] else 'Nenhum'}")
                
                print(f"Apenas em {name1} ({len(comparison['only_in_first'])}): ")
                print(f"  {', '.join(comparison['only_in_first']) if comparison['only_in_first'] else 'Nenhum'}")
                
                print(f"Apenas em {name2} ({len(comparison['only_in_second'])}): ")
                print(f"  {', '.join(comparison['only_in_second']) if comparison['only_in_second'] else 'Nenhum'}")
                
                print(f"Diferença de preço: R${abs(comparison_data[name1]['price'] - comparison_data[name2]['price']):.2f}")
    
    # 4. Estatísticas gerais
    print("\n📈 ESTATÍSTICAS GERAIS")
    print("-" * 60)
    
    total_sandwiches = len(sandwiches)
    prices = [normalize_price(s.get("price", 0)) for s in sandwiches]
    avg_price = sum(prices) / len(prices) if prices else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    
    ingredient_counts = [len(s.get("ingredients", [])) for s in sandwiches]
    avg_ingredients = sum(ingredient_counts) / len(ingredient_counts) if ingredient_counts else 0
    
    print(f"Total de sanduíches: {total_sandwiches}")
    print(f"Preço médio: R${avg_price:.2f}")
    print(f"Preço mínimo: R${min_price:.2f}")
    print(f"Preço máximo: R${max_price:.2f}")
    print(f"Média de ingredientes por sanduíche: {avg_ingredients:.1f}")
    print(f"Total de ingredientes únicos disponíveis: {len(ingredients_data)}")
    
    print("\n" + "=" * 80)
    print("FIM DO RELATÓRIO")
    print("=" * 80)

if __name__ == "__main__":
    main()