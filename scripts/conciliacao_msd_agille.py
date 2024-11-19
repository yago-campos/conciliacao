import pandas as pd
import os
import openpyxl
import time
import numpy as np
import re

# Função para remover as aspas simples do CNPJ
def remover_aspas_cnpj(cnpj):
    # Remover aspas simples do CNPJ
    return re.sub(r'[./-]', '', str(cnpj))

# Funções de formatação e remoção de sufixo decimal
def format_cnpj(value):
    if pd.isna(value):
        return '00000000000000'
    value = str(value) if isinstance(value, str) else str(value)
    return value.zfill(14)

def remove_decimal_suffix(value):
    if isinstance(value, str) and value.endswith('.0'):
        return value[:-2]
    return value

# Definição dos arquivos de origem e destino
arquivo_origem = 'Agille_BaseDistribuidor.xlsx'
arquivo_destino = 'Template.xlsx'

# Cria um arquivo de destino vazio se ele não existir
if not os.path.exists(arquivo_destino):
    with pd.ExcelWriter(arquivo_destino, engine='openpyxl') as writer:
        pd.DataFrame().to_excel(writer, index=False)
        
# Leitura das bases de dados
dados_origem = pd.read_excel(arquivo_origem)
dados_destino = pd.read_excel(arquivo_destino)

# Define as colunas de interesse e suas renomeações
colunas_interesse = {
    "NOTA": "NOTA",
    "RAZAO": "RAZAO",
    "CODPROD": "CODPROD",
    "DESCRICAO": "DESCRICAO",
    "DATANF": "DATANF",
    "QTDE": "QTDE",
    "VALOR":"VALOR",
    "QTDE_VLR": "QTDE_VLR",
    "EAN": "EAN",
    "CNPJ": "CNPJ",
    "SPEDIDO": "SPEDIDO",
    "CIDADE": "CIDADE",
    "UF": "UF",
    "FORNE": "FORNE",
    "PFABRICA": "PFABRICA",
    "PEDIDO": "PEDIDO"
}

# Seleção e renomeação das colunas de interesse
dados_interesse = dados_origem[list(colunas_interesse.keys())].rename(columns=colunas_interesse)

# Concatenar os dados de interesse ao arquivo destino (vazio neste caso)
dados_destino = pd.concat([dados_destino, dados_interesse], axis=1)

# Salvar a concatenação no arquivo Distribuidor.xlsx
dados_destino.to_excel('Distribuidor.xlsx', index=False)
os.remove(arquivo_destino)
print("As colunas foram copiadas com sucesso para o arquivo Distribuidor.xlsx.")

#########################################################################################

# Início do processamento adicional
print('Lendo a base Funcional...')
caminho_arquivo = 'Agille_BaseFuncional.xlsx'

print('Carregando a base Funcional...')
arquivo = openpyxl.load_workbook(caminho_arquivo)

print('Selecionando a aba ativa...')
planilha = arquivo.active

arquivo.save('Funcional_pode_excluir.xlsx')

print('Lendo as bases...')
base_funcional = pd.read_excel('Funcional_pode_excluir.xlsx')
base_distribuidor = pd.read_excel('Distribuidor.xlsx')

# Formatar CNPJ nas bases
base_funcional['CNPJ'] = base_funcional['CNPJ'].apply(remover_aspas_cnpj).apply(format_cnpj)
base_funcional['CNPJ'] = base_funcional['CNPJ'].apply(format_cnpj)
base_distribuidor['CNPJ'] = base_distribuidor['CNPJ'].apply(remove_decimal_suffix).apply(remover_aspas_cnpj)
base_distribuidor['CNPJ'] = base_distribuidor['CNPJ'].apply(format_cnpj).apply(remover_aspas_cnpj)
base_distribuidor['CNPJ'] = base_distribuidor['CNPJ'].apply(remove_decimal_suffix).apply(remover_aspas_cnpj)
base_distribuidor['CNPJ'] = base_distribuidor['CNPJ'].apply(format_cnpj).apply(remover_aspas_cnpj)

# Criar colunas específicas combinadas nas bases
print('Criando as colunas combinadas nas bases...')
base_funcional['CNPJ+NF'] = base_funcional['CNPJ'] + '-' + base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix)
base_funcional['CNPJ+NF+EAN'] = base_funcional['CNPJ+NF'] + '-' + base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) 
base_distribuidor['CNPJ+NF'] = base_distribuidor['CNPJ'] + '-' + base_distribuidor['NOTA'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['CNPJ+NF+EAN'] = base_distribuidor['CNPJ+NF'] + '-' + base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix)

    # Criar colunas específicas combinadas nas bases
print('Criando as colunas combinadas nas bases...')
base_funcional['CNPJ+NF'] = base_funcional['CNPJ'] + '-' + base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix)
base_funcional['CNPJ+NF+EAN'] = base_funcional['CNPJ+NF'] + '-' + base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['CNPJ+NF'] = base_distribuidor['CNPJ'] + '-' + base_distribuidor['NOTA'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['CNPJ+NF+EAN'] = base_distribuidor['CNPJ+NF'] + '-' + base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix)

# Criar as chaves e colunas adicionais nas bases
print('Criando as chaves nas bases...')

# Criar a quantidade somada antes de definir a chave para base funcional
base_funcional['Quantidade Somada'] = base_funcional.groupby(['CNPJ', 'Número da nota', 'EAN do produto'])['Quantidade Faturada'].transform('sum')
# Substituir NaN na coluna 'Quantidade Somada' com o valor de 'QTDE'
base_funcional['Quantidade Somada'] = base_funcional['Quantidade Somada'].fillna(base_funcional['Quantidade Faturada'])
# Criar a chave com a quantidade somada
base_funcional['Chave'] = (
    base_funcional['CNPJ'] + '-' +
    base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_funcional['Quantidade Somada'].astype(str).apply(remove_decimal_suffix)
)

# Criar a quantidade somada antes de definir a chave para base distribuidor
base_distribuidor['Quantidade Somada'] = base_distribuidor.groupby(['CNPJ', 'NOTA', 'EAN'])['QTDE'].transform('sum')
# Substituir NaN na coluna 'Quantidade Somada' com o valor de 'QTDE'
base_distribuidor['Quantidade Somada'] = base_distribuidor['Quantidade Somada'].fillna(base_distribuidor['QTDE'])
# Criar a chave com a quantidade somada
base_distribuidor['Chave'] = (
    base_distribuidor['CNPJ'] + '-' +
    base_distribuidor['NOTA'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_distribuidor['Quantidade Somada'].astype(str).apply(remove_decimal_suffix)
)

base_funcional['Status'] = ''
base_distribuidor['Status'] = ''

# Comparando as bases
print('Comparando as bases...')
base_distribuidor['Status'] = base_distribuidor['Chave'].isin(base_funcional['Chave']).map({True: 'OK', False: 'Chave não localizada'})
base_funcional['Status'] = base_funcional['Chave'].isin(base_distribuidor['Chave']).map({True: 'OK', False: 'Chave só consta na Funcional'})

# Lê a base pf_margem
pf_margem = pd.read_excel('pf_margem.xlsx', sheet_name='Dados')

# Formatar a coluna EAN na base pf_margem e na base_distribuidor
pf_margem['EAN'] = pf_margem['EAN'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['EAN'] = base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix)

# Realiza o merge entre a base_distribuidor e a pf_margem usando o EAN
base_distribuidor = base_distribuidor.merge(
    pf_margem[['EAN', 'DESCONTO ENTRADA', 'MARGEM OL', 'PF']],
    left_on='EAN',
    right_on='EAN',
    how='left'
)

# Renomear as colunas conforme solicitado
base_distribuidor.rename(columns={
    'DESCONTO ENTRADA': 'Desconto Entrada MSD',
    'MARGEM OL': 'Margem MSD',
    'PF': 'PF MSD'
}, inplace=True)

# Continuar pegando o 'Desconto Funcional' da base_funcional
base_distribuidor = base_distribuidor.merge(
    base_funcional[['Chave', 'Desconto pedido']],
    on='Chave',
    how='left'
)

base_distribuidor.rename(columns={'Desconto pedido': 'Desconto Funcional'}, inplace=True)

#=(100-ICMS)%*(Desc. Pedido+MargemOL-Desc Entrada)%*Qnt Faturada* Preço Fábrica
# Adicionar a coluna 'Ressarcimento Funcional' com o cálculo fornecido usando a 'Qtd'
base_distribuidor['Ressarcimento Funcional'] = np.where(
    (100 - 18) / 100 * 
    (base_distribuidor['Desconto Funcional'] + base_distribuidor['Margem MSD'] - base_distribuidor['Desconto Entrada MSD']) / 100 * 
    base_distribuidor['QTDE'] *
    base_distribuidor['PF MSD'] < 0, 
    0,  # Se o valor for negativo, substitui por 0
    (100 - 18) / 100 * 
    (base_distribuidor['Desconto Funcional'] + base_distribuidor['Margem MSD'] - base_distribuidor['Desconto Entrada MSD']) / 100 * 
    base_distribuidor['QTDE'] *
    base_distribuidor['PF MSD']  # Caso contrário, mantém o valor calculado
)

# Reordenando colunas - Colocando as novas colunas no início
novas_colunas_funcional = [
    'Chave','Status'
]
outras_colunas_funcional = [col for col in base_funcional.columns if col not in novas_colunas_funcional]
base_funcional = base_funcional[novas_colunas_funcional + outras_colunas_funcional]

novas_colunas_distribuidor = [
    'Chave', 'Status'
]
outras_colunas_distribuidor = [col for col in base_distribuidor.columns if col not in novas_colunas_distribuidor]
base_distribuidor = base_distribuidor[novas_colunas_distribuidor + outras_colunas_distribuidor]

print('Exibindo uma simples amostra de como ficou...')
time.sleep(1)
print("\nBase Funcional:\n", base_funcional.head())
print("\nBase Distribuidor:\n", base_distribuidor.head())
print('Salvando...')

# Apagar as colunas CNPJ+NF, CNPJ+NF+EAN, e Quantidade Somada
base_distribuidor.drop(columns=['CNPJ+NF', 'CNPJ+NF+EAN', 'Quantidade Somada'], inplace=True)
# salvar em duas abas diferentes do mesmo arquivo

with pd.ExcelWriter('Conciliação Finalizada Agille.xlsx', engine='openpyxl') as writer:
    base_distribuidor.to_excel(writer, sheet_name='Distribuidor', index=False)
    base_funcional.to_excel(writer, sheet_name='Funcional', index=False)

print('Finalizado!')

os.remove('Funcional_pode_excluir.xlsx')
os.remove('Distribuidor.xlsx')