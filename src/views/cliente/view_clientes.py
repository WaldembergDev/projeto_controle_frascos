import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque
import pandas as pd
import time

# carregando o dataframe no cache
@st.cache_data
def carregar_dataframe(tipo, verificar_pendencia = None):
    if tipo == 1: # carrega todos os clientes
        return ControllerCliente.carregar_dataframe_clientes()
    else: # carrega apenas os clientes sem movimentacao
        return ControllerCliente.carregar_dataframe_clientes_sem_movimentacao(verificar_pendencia)
    

# --- caixas de diálogo ---
# editar o cliente selecionado
@st.dialog(title='Editar Cliente / Visualizar Cliente')
def editar_cliente(dados_cliente):
    st.text(f'Id: {dados_cliente['id']}')
    nome_cliente = st.text_input('Nome do Cliente', value=dados_cliente['nome'])
    identificacao = st.text_input('Identificação', value=dados_cliente['identificacao'])
    email = st.text_input('Email', value=dados_cliente['email'])
    telefone = st.text_input('Telefone', value=dados_cliente['telefone'])
    valor_status = 0 if dados_cliente['status'] == 'ativo' else 1
    
    status = st.selectbox('Status', options=['ativo', 'inativo'], index=valor_status)
    # botão atualizar dados
    atualizar_dados = st.button('Atualizar Dados')

    if atualizar_dados:
        cliente_atualizado = ControllerCliente.atualizar_cliente_pelo_id(int(dados_cliente['id']), nome_cliente, identificacao, email, telefone, status)
        if cliente_atualizado == True:
            st.success('Cliente atualizado com sucesso!')
            carregar_dataframe.clear() # limpando os dados do cache para recarregar os dados
            time.sleep(3)
            st.rerun()

# criar um cliente
@st.dialog(title='Criar Cliente')
def criar_cliente():
    nome = st.text_input('Nome do cliente')
    identificacao = st.text_input('CPF/CNPJ')
    telefone = st.text_input('Telefone')
    email = st.text_input('Email')
    botao_cadastrar_cliente = st.button('Cadastrar Cliente', key='')

    if botao_cadastrar_cliente:
        cliente_salvo = ControllerCliente.cadastrar_cliente(nome=nome,
                                                            identificacao=identificacao,
                                                            telefone=telefone,
                                                            email=email)
        if cliente_salvo == True:
            st.success('Cliente cadastrado com sucesso!')
            carregar_dataframe.clear() # limpando os dados do cache para recarregar os dados
            time.sleep(3)
            st.rerun()
        else:
            st.error(f'Erro ao cadastrar o cliente. {cliente_salvo}')

# visualizar frascos do cliente
@st.dialog(title='Frascos do Cliente')
def consultar_frascos(id_cliente):
    st.divider()
    st.text('Datas importantes:')
    # Obtendo o empréstimo mais recente
    emprestimo_mais_recente = ControllerMovimentacaoEstoque.obter_emprestimo_mais_recente_id_cliente(int(id_cliente))
    # verificando se o cliente já solicitou frasco
    st.text(f'Empréstimo mais recente: {emprestimo_mais_recente if emprestimo_mais_recente else 'Não existem solicitações para este cliente'}')
    # Obtendo a devolução mais recente
    devolucao_mais_recente = ControllerMovimentacaoEstoque.obter_devolucao_mais_recente_id_cliente(int(id_cliente))
    # verificando se o cliente já devolveu frasco
    st.text(f'Devolução mais recente: {devolucao_mais_recente if devolucao_mais_recente else 'Não existem devoluções para este cliente'}')
    
    st.divider()
    st.text('Frascos em posse do cliente:')    
    detalhes_frascos = ControllerCliente.obter_detalhes_frascos_pelo_id_cliente(int(id_cliente))
    if detalhes_frascos:
        st.dataframe(ControllerCliente.criar_dataframe_frascos_cliente(int(id_cliente)))
    if not detalhes_frascos:
        st.text('Não existes frascos emprestados a esse cliente!')
    if st.button('Fechar visualização'):
        st.rerun()

# função que cria uma interface e carrega o dataframe de acordo com a aba selecionada
def renderizar_tela(dataframe, tipo):
    col1, col2 = st.columns(2)

    with col1:
        # exibe a tabela de clientes
        linhas = st.data_editor(dataframe, use_container_width=True, key=f'data_editor_{tipo}')

        # Obtendo o índices das linhas selecionadas
        linhas_selecionadas = linhas[linhas["Selecionado"] == True]

    with col2:
        cadastrar_cliente = st.button('Cadastrar Cliente', key=f'cadastrar_{tipo}')
        if cadastrar_cliente:
            criar_cliente()
        if len(linhas_selecionadas) == 1:
            botao_editar = st.button('Editar / Visualizar dados', key=f'editar_{tipo}')
            botao_visualizar_frascos = st.button('Consultar frascos', key=f'visualizar_{tipo}')
            if botao_editar:
                dados_cliente = ControllerCliente.transformar_linha_dicionario(linhas_selecionadas)
                editar_cliente(dados_cliente) 
            if botao_visualizar_frascos:
                dados_cliente = ControllerCliente.transformar_linha_dicionario(linhas_selecionadas)
                consultar_frascos(dados_cliente['id'])

# --- Interface Principal ---
st.header('Lista de Clientes', divider=True)

# ajustando para ter três abas
tab1, tab2, tab3 = st.tabs(['Todos', 'Com pendência', 'Sem atividade'])

# Carregando os datraframes
dataframe_todos = carregar_dataframe(1, False)
dataframe_pendentes = carregar_dataframe(2, True)
dataframe_sem_ativida = carregar_dataframe(2, False)

with tab1:
    renderizar_tela(dataframe_todos, tipo='todos')

with tab2:
    renderizar_tela(dataframe_pendentes, tipo='pendentes')

with tab3:
    renderizar_tela(dataframe_sem_ativida, tipo='sem_atividade')