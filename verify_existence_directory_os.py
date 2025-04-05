# Integridade e Estrutura dos Dados
# Verificar se todas as imagens listadas existem no diretório
# vou começar abrindo o json que contém as anotações do autor do data set
# usando como auxilio https://medium.com/lets-data/working-with-json-files-with-python-291fbdd8b41e

import json
import pandas as pd
import os
import re


with open('./annotations/instances_default.json', 'r') as f:
    dados = json.load(f)

#print(dados["images"])

# vou colocar os dados em um dataframe para ficar mais facil
# https://stackoverflow.com/questions/21104592/json-to-pandas-dataframe
#  "images": [{"id": 1, "width": 1920, "height": 1080, "file_name": "0.jpg", "license": 0, "flickr_url": "", "coco_url": "", "date_captured": 0}
# criar um dataframa usando a chave images do json dados
df_images = pd.DataFrame(dados['images'])

# uma coluna 'existe' booleana, se o nome da chave filename das imagens bater com algum item no diretorio /images
# apply, como já diz aplica a regra para cada valor da coluna
df_images['existe'] = df_images['file_name'].apply(
    # essa regra é um lambda, uma função temporaria onde nome_arquivo é o nome do arquivo atual 'file_name' do dataframe
    # então é .images/nome_arquivo
    # para verificar se o arquivo/caminho existe https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/
    # para concatenar caminhos https://awari.com.br/python-aprenda-a-usar-o-metodo-join-do-modulo-os-path/
    lambda nome_arquivo: os.path.isfile(os.path.join('./images/', nome_arquivo))
)

# vamos verificar o numero de arquivos
total_imagens = len(df_images)
# as imagens com true vão ser contabilizadas pelo metodo sum()
imagem_encontradas = df_images['existe'].sum()

# as faltantes é o resultado da subtração do total cedido por len() - a soma da contabilização de existe = true
imagens_faltantes = total_imagens - imagem_encontradas

# criar dataframes separados caso seja interessante analisar detalhes, nesse caso não parece necessário mas fica o exemplo
df_encontradas = df_images[df_images['existe'] == True]
df_faltantes = df_images[df_images['existe'] == False]


# fazer aqui

# Verificação de sequência quebrada
# https://pt.stackoverflow.com/questions/486258/por-que-utilizar-uma-express%C3%A3o-regular-compilada-re-compile-em-python
# padrao procura por numeros
padrao = re.compile(r'(\d+)')
numeros = []

for arquivo in df_images['file_name']:
    # .findall procura o padrao que é numeros
    resultado = padrao.findall(arquivo)
    # se tiver algum item = true
    if resultado:
        # pega o último número encontrado no nome (geralmente o que importa na sequência)
        numeros.append(int(resultado[-1]))

# ordenar os números e remover duplicatas numéricas
numeros_unicos = sorted(list(set(numeros)))

# encontrar lacunas na sequência
lacunas = []
# este loop percorre todos os índices da lista numeros_unicos, exceto o último (por isso o -1).
for i in range(len(numeros_unicos) - 1):
    # inicio como o número atual e fim como o próximo número na sequência.
    inicio = numeros_unicos[i]
    fim = numeros_unicos[i + 1]
    
    # verifica a lacuna
    if fim - inicio > 1:
        # existem números faltando entre inicio e fim
        # inicio = 5 e fim = 10, então list(range(6, 10)) resulta em [6, 7, 8, 9]
        numeros_faltantes = list(range(inicio + 1, fim))
        lacunas.append({
            "inicio": inicio,
            "fim": fim,
            "tamanho_lacuna": fim - inicio - 1,
            "numeros_faltantes": numeros_faltantes
        })


    

print(f'Total de imagens declaradas: {total_imagens}')
print(f'Total de imagens encontradas no sistema: {imagem_encontradas}')
print(f'Total de imagens que se ausentam no sistema: {imagens_faltantes}')
print(f'Total de lacunas na sequencia numerica: {len(lacunas)}')

# int() para converter os valores numpy que são oriuntados de manipulação direto do pandas
resultado = {
    "total_imagens_declaradas": int(total_imagens),
    "total_imagens_encontradas": int(imagem_encontradas),
    "total_imagens_ausentes": int(imagens_faltantes),
    "analise_sequencia": {
        "menor_numero": min(numeros_unicos) if numeros_unicos else None,
        "maior_numero": max(numeros_unicos) if numeros_unicos else None,
        "total_lacunas": len(lacunas),
        "detalhes_lacunas": lacunas
    }
}

with open('./output/existencia_arquivos.json', 'w') as json_file:
    json.dump(resultado, json_file)