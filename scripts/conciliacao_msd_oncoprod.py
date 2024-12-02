import sys
import pandas as pd
import numpy as np

# Função para remover as aspas simples do CNPJ
def remover_aspas_CNPJ(CNPJ):
    # Remover aspas simples do CNPJ
    return str(CNPJ).replace("'", "")

# Funções de formatação e remoção de sufixo decimal
def format_CNPJ(value):
    if pd.isna(value):
        return '00000000000000'
    value = str(value) if isinstance(value, str) else str(value)
    return value.zfill(14)

def remove_decimal_suffix(value):
    if isinstance(value, str) and value.endswith('.0'):
        return value[:-2]
    return value

# Função para remover caracteres não numéricos (pontos, traços, barras) do CNPJ
def limpar_CNPJ(value):
    if pd.isna(value):
        return value
    return ''.join(filter(str.isdigit, str(value)))

# Definição dos arquivos de origem e destino
arquivo_funcional = sys.argv[1]
arquivo_distribuidor = sys.argv[2]
arquivo_pf_margem = sys.argv[3]

# 1. Carregar o arquivo baseDistribuidor
print('Lendo o arquivo do distribuidor...')
try:
    base_distribuidor = pd.read_excel(arquivo_distribuidor, skiprows=1)
except Exception as e:
    print(f"Erro ao carregar o arquivo baseDistribuidor: {e}")
    sys.exit(1)

# 2. Carregar o arquivo baseFuncional usando OpenPyxl
print('Lendo o arquivo baseFuncional...')
try:
    # Carregando o arquivo 
    base_funcional = pd.read_excel(arquivo_funcional)
    print('Arquivo CSV carregado com sucesso.')

    # Verificando as colunas e preparando a base de dados
    colunas = base_funcional.columns.tolist()  # Lista de colunas do 
    print(f'Colunas encontradas: {colunas}')

except Exception as e:
    print(f"Erro ao carregar o arquivo baseFuncional: {e}")
    sys.exit(1)

# Formatar CNPJ nas bases
base_funcional['CNPJ'] = base_funcional['CNPJ'].apply(remover_aspas_CNPJ)
base_funcional['CNPJ'] = base_funcional['CNPJ'].apply(format_CNPJ)
base_distribuidor['CPF/CNPJ'] = base_distribuidor['CPF/CNPJ'].apply(limpar_CNPJ)  # Limpa a coluna removendo pontos, traços e barras
base_distribuidor['CPF/CNPJ'] = base_distribuidor['CPF/CNPJ'].apply(format_CNPJ)

# Renomear a coluna 'CPF/CNPJ' para 'CNPJ'
base_distribuidor.rename(columns={'CPF/CNPJ': 'CNPJ'}, inplace=True)

# Criar colunas específicas combinadas nas bases
print('Criando as colunas combinadas nas bases...')
base_funcional['CNPJ+NF'] = base_funcional['CNPJ'] + '-' + base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix)
base_funcional['CNPJ+NF+EAN'] = base_funcional['CNPJ+NF'] + '-' + base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) 
base_distribuidor['CNPJ+NF'] = base_distribuidor['CNPJ'] + '-' + base_distribuidor['NR. NF'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['CNPJ+NF+EAN'] = base_distribuidor['CNPJ+NF'] + '-' + base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix)

# Criar as chaves e colunas adicionais nas bases
print('Criando as chaves nas bases...')

# Criar a quantidade somada antes de definir a chave para base funcional
base_funcional['Quantidade Somada'] = base_funcional.groupby(['CNPJ', 'Número da nota', 'EAN do produto'])['Quantidade Faturada'].transform('sum')

# Criar a chave com a quantidade somada
base_funcional['Chave'] = (
    base_funcional['CNPJ'] + '-' +
    base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_funcional['Quantidade Somada'].astype(str).apply(remove_decimal_suffix)
)

# Criar a quantidade somada antes de definir a chave para base distribuidor
base_distribuidor['Quantidade Somada'] = base_distribuidor.groupby(['CNPJ', 'NR. NF', 'EAN'])['QTDE FATURADA'].transform('sum')

# Criar a chave com a quantidade somada
base_distribuidor['Chave'] = (
    base_distribuidor['CNPJ'] + '-' +
    base_distribuidor['NR. NF'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_distribuidor['EAN'].astype(str).apply(remove_decimal_suffix) + '-' +
    base_distribuidor['Quantidade Somada'].astype(str).apply(remove_decimal_suffix)
)

base_funcional['Status'] = ''
base_distribuidor['Status'] = ''

# Comparando as bases
print('Comparando as bases...')
base_distribuidor['Status'] = base_distribuidor['Chave'].isin(base_funcional['Chave']).map({True: 'OK', False: 'Chave não localizada'})
base_funcional['Status'] = base_funcional['Chave'].isin(base_distribuidor['Chave']).map({True: 'OK', False: 'Chave só consta na Funcional'})

# Verifica se o argumento foi passado corretamente
if len(sys.argv) < 4:
    print("Erro: O caminho do arquivo pf_margem.xlsx não foi fornecido.")
    sys.exit(1)

# Lê o caminho do arquivo pf_margem do argumento fornecido
try:
    # Passa o caminho correto do arquivo para o pd.read_excel
    pf_margem = pd.read_excel(arquivo_pf_margem, sheet_name='Dados')
    print("Arquivo pf_margem carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o arquivo pf_margem: {e}")
    sys.exit(1)

# Formatar a coluna EAN na base pf_margem e na base_distribuidor
pf_margem['EAN'] = pf_margem['EAN'].astype(str).apply(remove_decimal_suffix)
base_distribuidor['Código EAN'] = base_distribuidor['Código EAN'].astype(str).apply(remove_decimal_suffix)

# Realiza o merge entre a base_distribuidor e a pf_margem usando o EAN
base_distribuidor = base_distribuidor.merge(
    pf_margem[['EAN', 'DESCONTO ENTRADA', 'MARGEM OL', 'PF']],
    left_on='Código EAN',
    right_on='EAN',
    how='left'
)

# Remover a coluna EAN após o merge
base_distribuidor.drop(columns=['EAN'], inplace=True)

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
    base_distribuidor['QTDE FATURADA'] *
    base_distribuidor['PF MSD'] < 0,  # Se o valor for negativo, substitui por 0
    0,  
    (100 - 18) / 100 * 
    (base_distribuidor['Desconto Funcional'] + base_distribuidor['Margem MSD'] - base_distribuidor['Desconto Entrada MSD']) / 100 * 
    base_distribuidor['QTDE FATURADA'] *
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


# salvar em duas abas diferentes do mesmo arquivo
with pd.ExcelWriter('Conciliacao_Finalizada_Santa_Cruz.xlsx', engine='openpyxl') as writer:
    base_distribuidor.to_excel(writer, sheet_name='Distribuidor', index=False)
    base_funcional.to_excel(writer, sheet_name='Funcional', index=False)

print('Finalizado!')
