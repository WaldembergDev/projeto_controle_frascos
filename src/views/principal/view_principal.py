import streamlit as st

class ViewPrincipal:
    @classmethod
    def menu_principal(cls):
        # paginas
        view_dashboard = st.Page(r'src\views\dashboard\view_dashboard.py', title='Dashboard')

        # Clientes
        # view_cadastro_cliente = st.Page(r'src\views\cliente\view_cadastro_cliente.py', title='Cadastro de Clientes')
        view_clientes = st.Page(r'src\views\cliente\view_clientes.py', title='Lista de Clientes')

        # frascos
        view_frascos = st.Page(r'src\views\frasco\view_frascos.py', title='Lista de Frascos')
        view_liberacao_frascos = st.Page(r'src\views\frasco\view_liberacao_frasco.py', title='Liberação de Frascos')
        view_devolucao = st.Page(r'src\views\frasco\view_devolucao.py', title='Devolução de Frascos')
        view_estoque_frascos = st.Page(r'src\views\estoque\view_historico.py', title='Histórico')
        view_relatorios = st.Page(r'src\views\relatorio\view_relatorio.py', title='Relatório de Frascos')
        view_solicitacao = st.Page(r'src\views\frasco\view_solicitacao.py', title='Solicitação de Frascos')

        pagina = st.navigation({
            'Menu Principal': [view_dashboard],
            'Cliente': [view_clientes],
            'Frasco': [view_frascos, view_liberacao_frascos, view_devolucao, view_solicitacao, view_estoque_frascos],
            'Relatórios': [view_relatorios]
        })

        with st.sidebar:
            if st.button('Logout'):
                st.logout()

        pagina.run()