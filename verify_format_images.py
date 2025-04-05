import pandas as pd
import os

# Função para puxar arquivo por arquivo e retornar em um dataframe com Formato e Quantidade
def obter_formatos(diretorio):
    dados = []
    
    for arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, arquivo)
        
        if os.path.isfile(caminho):
            extensao = arquivo.split(".")[-1].upper()  # Obtém a extensão do arquivo
            dados.append({"arquivo": arquivo, "formato": extensao}) 

    df = pd.DataFrame(dados)
    
    # Contar quantos arquivos existem por formato
    contagem_formatos = df["formato"].value_counts().reset_index()
    contagem_formatos.columns = ["Formato", "Quantidade"]
    
    return df, contagem_formatos


diretorio = "./data/raw/images"
contagem_formatos = obter_formatos(diretorio)

# Exibir o total de arquivos para garantir que todos estão sendo lidos
print("\nTotal de arquivos na pasta:", len(os.listdir(diretorio)))

# Exibir a contagem de formatos automaticamente
print("\nResumo dos formatos encontrados:")
print(contagem_formatos)