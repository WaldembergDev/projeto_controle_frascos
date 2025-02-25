import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco
import time

# caixas de diálogo
# cadastrar frasco
@st.dialog(title='Cadastrar frasco')
def cadastrar_frasco():
    identificacao = st.text_input('Identificação do Frasco')
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1)
    descricao = st.text_input('Descrição do frasco')
    estoque = st.number_input('Estoque real do frasco', step=1, min_value=0)
    estoque_minimo = st.number_input('Estoque mínimo do frasco', step=1, min_value=0)

    botao_cadastrar = st.button('Cadastrar frasco')
    
    if botao_cadastrar:
        frasco_cadastrado = ControllerFrasco.criar_frasco(1, identificacao, capacidade, estoque, estoque_minimo, descricao)
        if frasco_cadastrado:
            st.success('Frasco cadastrado com sucesso!')
            time.sleep(3)
            st.rerun()
        elif not frasco_cadastrado:
            st.error('Erro ao cadastrar o frasco! Reveja os dados!')            
    
# editar frasco
@st.dialog(title='Editar frasco')
def editar_frasco(dados_frasco):
    id = int(dados_frasco['id']) 
    st.text(f'Id: {id}')
    estoque = st.text(f'Estoque real do frasco: {dados_frasco['estoque']}')
    identificacao = st.text_input('Identificação do Frasco', value=dados_frasco['identificacao'])
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1, value=dados_frasco['capacidade'])
    estoque_minimo = st.number_input('Estoque mínimo do frasco', step=1, min_value=0, value=dados_frasco['estoque_minimo'])
    descricao = st.text_input('Descrição do frasco', value=dados_frasco['descricao'])
    valor_status = 0 if dados_frasco['status'] == 'ativo' else 1
    status = st.selectbox('Status', options=['ativo', 'inativo'], index=valor_status)
    
    botao_alterar = st.button('Salvar alterações')

    if botao_alterar:
        frasco_editado = ControllerFrasco.editar_frasco_pelo_id(id, identificacao, capacidade, estoque_minimo, descricao, status)
        if frasco_editado == True:
            st.success('Frasco editado com sucesso!')
            time.sleep(3)
            st.rerun()
        elif frasco_editado == False:
            st.error('Erro ao editar o frasco. Revise os dados digitados!')
            


# -- Tela principal -- 
st.header('Lista de Frascos', divider=True)

dataframe = ControllerFrasco.carregar_dataframe_frascos()

col1, col2 = st.columns(2)

with col1:
    linhas = st.data_editor(dataframe)

    # Obtendo o índices das linhas selecionadas
    linhas_selecionadas = linhas[linhas["Selecionado"] == True]

with col2:
    cadastro_frasco = st.button('Criar frasco')
    if cadastro_frasco:
        cadastrar_frasco()
    if len(linhas_selecionadas) == 1:
        botao_editar = st.button('Editar')
        if botao_editar:
            dados_frasco = {
                'id': linhas_selecionadas.iloc[0, 1],
                'identificacao': linhas_selecionadas.iloc[0, 2],
                'capacidade': linhas_selecionadas.iloc[0, 3],
                'estoque': linhas_selecionadas.iloc[0,4],
                'estoque_minimo': linhas_selecionadas.iloc[0,5],
                'descricao': linhas_selecionadas.iloc[0,6],
                'status': linhas_selecionadas.iloc[0,7],
            }
            editar_frasco(dados_frasco)