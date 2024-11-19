import pandas as pd
import openpyxl

def format_cnpj(value):
    if pd.isna(value):
        return '00000000000000'
    value = str(int(value)) if isinstance(value, (int, float)) else str(value)
    return value.zfill(14)

def remove_decimal_suffix(value):
    if isinstance(value, str) and value.endswith('.0'):
        return value[:-2]
    return value

print('Olá! Os arquivos Funcional.xlsx precisam estar na mesma pasta.')
pergunta_inicio = input('Deseja continuar? ')
if pergunta_inicio.lower() in ["sim", "s"]:
    print('Lendo a base Funcional...')
    caminho_arquivo = 'Funcional.xlsx'

    print('Carregando a base Funcional...')
    arquivo = openpyxl.load_workbook(caminho_arquivo)

    print('Selecionando a aba ativa...')
    planilha = arquivo.active

    print('Transformando a base Funcional em uma tabela...')
    tabela = openpyxl.worksheet.table.Table(displayName="TabelaSimples", ref=planilha.dimensions)
    planilha.add_table(tabela)

    arquivo.save('Funcional_pode_excluir.xlsx')
    
    print('Lendo a base Funcional...')
    base_funcional = pd.read_excel('Funcional_pode_excluir.xlsx')

    # Formatar CNPJ na base
    base_funcional['CNPJ'] = base_funcional['CNPJ'].apply(format_cnpj)
    
    # Criar colunas específicas combinadas na base
    print('Criando as colunas combinadas na base...')
    base_funcional['CNPJ+NF'] = base_funcional['CNPJ'] + '-' + base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix)
    base_funcional['CNPJ+NF+EAN'] = base_funcional['CNPJ+NF'] + '-' + base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix)
    
    # Criar as chaves e colunas adicionais na base
    print('Criando as chaves na base...')
    base_funcional['Chave1'] = (
        base_funcional['CNPJ'] + '-' +
        base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix) + '-' +
        base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) + '-' +
        base_funcional['Quantidade Faturada'].astype(str).apply(remove_decimal_suffix)
    )
    base_funcional['Quantidade Somada'] = base_funcional.groupby(['CNPJ', 'Número da nota', 'EAN do produto'])['Quantidade Faturada'].transform('sum')
    base_funcional['Chave2'] = (
        base_funcional['CNPJ'] + '-' +
        base_funcional['Número da nota'].astype(str).apply(remove_decimal_suffix) + '-' +
        base_funcional['EAN do produto'].astype(str).apply(remove_decimal_suffix) + '-' +
        base_funcional['Quantidade Somada'].astype(str).apply(remove_decimal_suffix)
    )

    # Salvar o arquivo com as alterações
    base_funcional.to_excel('Funcional_atualizado.xlsx', index=False)
    print('Processo concluído. As colunas de chave foram criadas e o arquivo foi salvo como Funcional_atualizado.xlsx.')