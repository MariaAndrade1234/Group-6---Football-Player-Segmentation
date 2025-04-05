# Integridade e Estrutura dos Dados
# Verificar o formato das imagens (JPEG, PNG, etc.)
import os
import pandas as pd
import json
# inserir os nomes em um dataframe usando lsita de dicionarios
ficheiros = []
# os.listdir retorna uma lista com todos os filenames no diretorio, e o loop percorre cada um
for nome_ficheiro in os.listdir('./images/'):
    # verifica se é um arquivo
    if os.path.isfile(os.path.join('./images/', nome_ficheiro)):
        # os.path.sliptext separa o nome da extensão,
        nome, extensao = os.path.splitext(nome_ficheiro)
        ficheiros.append({'nome_ficheiro': nome_ficheiro, 'extensao': extensao})

df = pd.DataFrame(ficheiros)

# contar a ocorrência de cada extensão no formato series
contagem_extensoes = df['extensao'].value_counts()

print("DataFrame original:")
print(df)

print("\nContagem de cada extensao:")
print(contagem_extensoes)

# de Series para dicionario python
contagem_dict = contagem_extensoes.to_dict()
print("\nDicionario de contagens:")
print(contagem_dict)

resultado = {
    "formatos:": contagem_dict
}

with open('./output/formato_arquivos.json', 'w') as json_file:
    json.dump(resultado, json_file)