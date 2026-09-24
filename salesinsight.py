import csv
import json
import os
import random
import re
from datetime import datetime, timedelta


def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset de vendas com alguns dados propositalmente inconsistentes."""
    random.seed(seed)

    produtos = [
        "Notebook",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse",
        "Headset",
    ]

    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Periféricos",
        "Teclado": "Periféricos",
        "Mouse": "Periféricos",
        "Headset": "Periféricos",
    }

    precos = {
        "Notebook": 4500.00,
        "Smartphone": 2800.00,
        "Tablet": 1900.00,
        "Monitor": 1500.00,
        "Teclado": 250.00,
        "Mouse": 120.00,
        "Headset": 350.00,
    }

    regioes = ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"]
    data_inicial = datetime(2025, 1, 1)

    campos = [
        "id_venda",
        "data",
        "cliente",
        "produto",
        "categoria",
        "regiao",
        "quantidade",
        "preco_unitario",
    ]

    registros = []

    for i in range(1, n_registros + 1):
        produto = random.choice(produtos)
        data = data_inicial + timedelta(days=random.randint(0, 364))

        cliente = f"Cliente_{random.randint(1, 50):03d}"

        # Dados propositalmente "sujos".
        if random.random() < 0.10:
            cliente = f"  {cliente}  "
        if random.random() < 0.06:
            produto = f"  {produto}  "

        data_texto = data.strftime("%Y-%m-%d")
        if random.random() < 0.03:
            data_texto = "2025-99-99"

        quantidade = random.randint(1, 10)
        if random.random() < 0.05:
            quantidade = ""

        preco = round(precos[produto.strip()] * random.uniform(0.90, 1.10), 2)
        if random.random() < 0.04:
            preco = ""

        registros.append(
            {
                "id_venda": i,
                "data": data_texto,
                "cliente": cliente,
                "produto": produto,
                "categoria": categorias[produto.strip()],
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            }
        )

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)

    print(f"Dataset gerado com sucesso: {caminho_csv}")
    print(f"Quantidade de registros: {n_registros}")


def carregar_dataset(caminho_csv="vendas.csv"):
    """Carrega o dataset CSV e retorna uma lista de dicionários."""
    with open(caminho_csv, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        registros = list(leitor)

    print(f"\nDataset carregado: {caminho_csv}")
    print(f"Registros carregados: {len(registros)}")

    return registros


def inspecionar_dados(registros):
    """Apresenta uma inspeção inicial do dataset."""
    print("\n=== INSPEÇÃO DO DATASET ===")
    print(f"Total de registros: {len(registros)}")

    if not registros:
        print("Dataset vazio.")
        return

    print(f"Colunas: {list(registros[0].keys())}")

    print("\nValores ausentes:")
    for coluna in registros[0].keys():
        ausentes = sum(
            1 for registro in registros
            if str(registro.get(coluna, "")).strip() == ""
        )
        print(f"- {coluna}: {ausentes}")

    print("\nPrimeiros 5 registros:")
    for registro in registros[:5]:
        print(registro)


def limpar_dados(registros):
    """Limpa e valida os dados utilizando strip, datetime e regex."""
    registros_limpos = []
    removidos_data = 0
    removidos_quantidade = 0
    removidos_preco = 0
    removidos_cliente = 0

    padrao_cliente = re.compile(r"^Cliente_\d{3}$")

    for registro in registros:
        registro = {
            chave: str(valor).strip() if valor is not None else ""
            for chave, valor in registro.items()
        }

        # Validação da data.
        try:
            data_validada = datetime.strptime(registro["data"], "%Y-%m-%d")
        except (ValueError, TypeError):
            removidos_data += 1
            continue

        # Validação da quantidade.
        try:
            quantidade = int(registro["quantidade"])
            if quantidade <= 0:
                raise ValueError
        except (ValueError, TypeError):
            removidos_quantidade += 1
            continue

        # Validação do preço.
        try:
            preco = float(registro["preco_unitario"])
            if preco <= 0:
                raise ValueError
        except (ValueError, TypeError):
            removidos_preco += 1
            continue

        # Limpeza do cliente com regex.
        cliente = re.sub(r"[^A-Za-z0-9_]", "", registro["cliente"])

        if not padrao_cliente.fullmatch(cliente):
            removidos_cliente += 1
            continue

        registro["data"] = data_validada.strftime("%Y-%m-%d")
        registro["quantidade"] = quantidade
        registro["preco_unitario"] = preco
        registro["cliente"] = cliente
        registro["produto"] = registro["produto"].strip()
        registro["categoria"] = registro["categoria"].strip()
        registro["regiao"] = registro["regiao"].strip()

        registros_limpos.append(registro)

    print("\n=== LIMPEZA DOS DADOS ===")
    print(f"Registros recebidos: {len(registros)}")
    print(f"Registros mantidos: {len(registros_limpos)}")
    print(f"Removidos por data inválida: {removidos_data}")
    print(f"Removidos por quantidade inválida/ausente: {removidos_quantidade}")
    print(f"Removidos por preço inválido/ausente: {removidos_preco}")
    print(f"Removidos por cliente inválido: {removidos_cliente}")

    return registros_limpos


def criar_colunas_derivadas(registros):
    """Cria receita, mês, trimestre, ano e faixa de receita."""
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    for registro in registros:
        data = datetime.strptime(registro["data"], "%Y-%m-%d")
        receita = registro["quantidade"] * registro["preco_unitario"]

        mes = data.month
        trimestre = f"Q{((mes - 1) // 3) + 1}"

        if receita < 500:
            faixa = "Baixa"
        elif receita < 5000:
            faixa = "Média"
        else:
            faixa = "Alta"

        registro["receita_total"] = round(receita, 2)
        registro["mes"] = mes
        registro["mes_nome"] = meses[mes]
        registro["trimestre"] = trimestre
        registro["ano"] = data.year
        registro["faixa_receita_item"] = faixa

    print("\nColunas derivadas criadas com sucesso.")
    return registros


def calcular_metricas(registros):
    """Calcula métricas agregadas por mês, produto, categoria e região."""
    por_mes = {}
    por_produto = {}
    por_categoria = {}
    por_regiao = {}

    for registro in registros:
        receita = registro["receita_total"]
        quantidade = registro["quantidade"]
        mes = f'{registro["ano"]}-{registro["mes"]:02d}'
        produto = registro["produto"]
        categoria = registro["categoria"]
        regiao = registro["regiao"]

        por_mes[mes] = por_mes.get(mes, 0) + receita
        por_produto[produto] = por_produto.get(produto, 0) + receita
        por_categoria[categoria] = por_categoria.get(categoria, 0) + receita

        if regiao not in por_regiao:
            por_regiao[regiao] = {
                "receita_total": 0,
                "quantidade_vendas": 0,
                "quantidade_itens": 0,
            }

        por_regiao[regiao]["receita_total"] += receita
        por_regiao[regiao]["quantidade_vendas"] += 1
        por_regiao[regiao]["quantidade_itens"] += quantidade

    top_5_produtos = sorted(
        por_produto.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    for dados in por_regiao.values():
        dados["ticket_medio"] = round(
            dados["receita_total"] / dados["quantidade_vendas"], 2
        )

    metricas = {
        "por_mes": dict(sorted(por_mes.items())),
        "top_5_produtos": top_5_produtos,
        "por_categoria": dict(
            sorted(por_categoria.items(), key=lambda item: item[1], reverse=True)
        ),
        "por_regiao": por_regiao,
    }

    print("\n=== MÉTRICAS ===")
    print("Receita por mês:")
    for mes, receita in metricas["por_mes"].items():
        print(f"- {mes}: ${receita:,.2f}")

    print("\nTop 5 produtos por receita:")
    for produto, receita in top_5_produtos:
        print(f"- {produto}: ${receita:,.2f}")

    print("\nReceita por categoria:")
    for categoria, receita in metricas["por_categoria"].items():
        print(f"- {categoria}: ${receita:,.2f}")

    print("\nReceita e ticket médio por região:")
    for regiao, dados in por_regiao.items():
        print(
            f"- {regiao}: receita ${dados['receita_total']:,.2f} | "
            f"ticket médio ${dados['ticket_medio']:,.2f}"
        )

    return metricas


def segmentar_clientes(registros):
    """Calcula o gasto dos clientes e classifica em Bronze, Silver ou Gold."""
    gastos_clientes = {}

    for registro in registros:
        cliente = registro["cliente"]
        gastos_clientes[cliente] = (
            gastos_clientes.get(cliente, 0) + registro["receita_total"]
        )

    classificar = lambda valor: (
        "Bronze" if valor < 5000
        else "Silver" if valor <= 15000
        else "Gold"
    )

    clientes = []
    for cliente, valor in gastos_clientes.items():
        clientes.append(
            {
                "cliente": cliente,
                "valor_total": round(valor, 2),
                "segmento": classificar(valor),
            }
        )

    clientes.sort(key=lambda item: item["valor_total"], reverse=True)

    distribuicao = {}
    for cliente in clientes:
        segmento = cliente["segmento"]
        distribuicao[segmento] = distribuicao.get(segmento, 0) + 1

    top_10 = clientes[:10]

    print("\n=== SEGMENTAÇÃO DE CLIENTES ===")
    print("Top 10 clientes:")
    for cliente in top_10:
        print(
            f"- {cliente['cliente']}: "
            f"${cliente['valor_total']:,.2f} "
            f"({cliente['segmento']})"
        )

    print("\nDistribuição:")
    for segmento, quantidade in distribuicao.items():
        print(f"- {segmento}: {quantidade} clientes")

    return {
        "clientes": clientes,
        "top_10": top_10,
        "distribuicao": distribuicao,
    }


def processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None):
    """Higher-Order Function: recebe outra função e transforma uma coluna."""
    if nome_saida is None:
        nome_saida = f"{coluna}_transformada"

    for registro in registros:
        registro[nome_saida] = funcao_transformacao(registro[coluna])

    print(
        f"\nHigher-Order Function aplicada: "
        f"{coluna} -> {nome_saida}"
    )

    return registros


def exportar_metricas_csv(metricas, caminho="metricas_por_mes.csv"):
    """Exporta as métricas mensais para CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["mes", "receita_total"])

        for mes, receita in metricas["por_mes"].items():
            writer.writerow([mes, round(receita, 2)])

    print(f"Arquivo exportado: {caminho}")


def exportar_segmentacao_csv(segmentacao, caminho="segmentacao_clientes.csv"):
    """Exporta a segmentação de clientes para CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(
            arquivo,
            fieldnames=["cliente", "valor_total", "segmento"]
        )
        writer.writeheader()

        for cliente in segmentacao["clientes"]:
            writer.writerow(cliente)

    print(f"Arquivo exportado: {caminho}")


def calcular_estatisticas_gerais(registros):
    """Calcula estatísticas gerais do dataset limpo."""
    total_registros = len(registros)
    receita_total = sum(r["receita_total"] for r in registros)
    quantidade_total = sum(r["quantidade"] for r in registros)
    clientes = len(set(r["cliente"] for r in registros))

    ticket_medio = (
        receita_total / total_registros
        if total_registros else 0
    )

    receita_media_venda = ticket_medio

    vendas_acima_media = sum(
        1 for r in registros
        if r["receita_total"] > receita_media_venda
    )

    return {
        "total_registros": total_registros,
        "receita_total": round(receita_total, 2),
        "quantidade_total": quantidade_total,
        "quantidade_clientes": clientes,
        "ticket_medio": round(ticket_medio, 2),
        "receita_media_por_venda": round(receita_media_venda, 2),
        "vendas_acima_da_media": vendas_acima_media,
    }


def exportar_estatisticas_json(estatisticas, caminho="estatisticas_gerais.json"):
    """Exporta estatísticas gerais para JSON."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(estatisticas, arquivo, ensure_ascii=False, indent=4)

    print(f"Arquivo exportado: {caminho}")


def main():
    """Executa o fluxo completo do SalesInsight PY."""
    caminho_dataset = "vendas.csv"

    if not os.path.exists(caminho_dataset):
        print("vendas.csv não encontrado. Gerando dataset...")
        gerar_dataset_vendas(caminho_dataset)

    registros = carregar_dataset(caminho_dataset)

    inspecionar_dados(registros)

    registros_limpos = limpar_dados(registros)

    registros_completos = criar_colunas_derivadas(registros_limpos)

    processar_coluna(
        registros_completos,
        "receita_total",
        lambda valor: round(valor / 1000, 2),
        "receita_em_milhares",
    )

    processar_coluna(
        registros_completos,
        "quantidade",
        lambda valor: "Alto Volume" if valor > 5 else "Baixo Volume",
        "perfil_volume",
    )

    metricas = calcular_metricas(registros_completos)

    segmentacao = segmentar_clientes(registros_completos)

    estatisticas = calcular_estatisticas_gerais(registros_completos)

    exportar_metricas_csv(metricas)

    exportar_segmentacao_csv(segmentacao)

    exportar_estatisticas_json(estatisticas)

    with open("estatisticas_gerais.json", "r", encoding="utf-8") as arquivo:
        estatisticas_lidas = json.load(arquivo)

    print("\n=== ESTATÍSTICAS GERAIS ===")
    for chave, valor in estatisticas_lidas.items():
        print(f"{chave}: {valor}")

    print("\n=== ARQUIVOS GERADOS ===")
    for arquivo in [
        "vendas.csv",
        "metricas_por_mes.csv",
        "segmentacao_clientes.csv",
        "estatisticas_gerais.json",
    ]:
        if os.path.exists(arquivo):
            print(f"- {arquivo}")

    print("\nSalesInsight PY executado com sucesso!")


if __name__ == "__main__":
    main()
