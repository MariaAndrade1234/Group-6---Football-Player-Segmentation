import os
from PIL import Image, ImageStat
import pandas as pd

def analisar_imagens(diretorio):
    dados = []

    for nome_arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome_arquivo)

        if not os.path.isfile(caminho):
            continue

        try:
            with Image.open(caminho) as img:
                # Detectar imagens corrompidas: se chegou aqui, abriu com sucesso
                img.verify()  # Valida sem carregar a imagem
            with Image.open(caminho) as img:
                largura, altura = img.size
                img = img.convert('L')  # Converte para escala de cinza
                stat = ImageStat.Stat(img)
                brilho = stat.mean[0]
                contraste = stat.stddev[0]

                problemas = []
                if brilho < 50:
                    problemas.append("brilho_baixo")

                elif brilho > 200:
                    problemas.append("brilho_alto")

                if contraste < 20:
                    problemas.append("contraste_baixo")

                dados.append({
                    "arquivo": nome_arquivo,
                    "largura": largura,
                    "altura": altura,
                    "brilho": round(brilho, 2),
                    "contraste": round(contraste, 2),
                    "corrompida": False,
                    "problemas": ", ".join(problemas) if problemas else "ok"
                })

        except Exception as e:
            # Imagem corrompida ou erro na leitura
            dados.append({
                "arquivo": nome_arquivo,
                "largura": None,
                "altura": None,
                "brilho": None,
                "contraste": None,
                "corrompida": True
            })

    return dados

diretorio = "./data/raw/images"
resultados = analisar_imagens(diretorio)

# Criar DataFrame principal
df = pd.DataFrame(resultados)

# Total de arquivos no diretório
print("\n Total de arquivos na pasta:", len(os.listdir(diretorio)))

# Separar válidas e corrompidas
df_corrompidas = df[df["corrompida"] == True]
df_validas = df[df["corrompida"] == False]

# Imagens corrompidas
print(f"\n Imagens corrompidas ({len(df_corrompidas)}):")
for arquivo in df_corrompidas["arquivo"]:
    print("-", arquivo)

# Total de imagens válidas
print(f"\n Total de imagens válidas: {len(df_validas)}")

# Soma pra validar
print(f"\n Soma de imagens válidas e corrompidas: {len(df_validas) + len(df_corrompidas)}")

# Criar coluna de resolução
df_validas["resolucao"] = df_validas[["largura", "altura"]].values.tolist()

# Contar resoluções
contagem_resolucoes = df_validas["resolucao"].value_counts().reset_index()
contagem_resolucoes.columns = ["Resolução", "Quantidade"]

print("\n Resumo das resoluções encontradas:")
print(contagem_resolucoes)

# Contar tipos de problemas
contagem_problemas = df_validas["problemas"].value_counts().reset_index()
contagem_problemas.columns = ["Tipo de Problema", "Quantidade"]

print("\n Resumo de problemas de qualidade:")
print(contagem_problemas)

# Listar as imagens que têm problemas (ou seja, diferente de "OK")
df_problemas = df_validas[df_validas["problemas"] != "ok"]

print("\n Imagens com problemas de qualidade:")
print(df_problemas[["arquivo", "problemas", "brilho", "contraste", "resolucao"]])