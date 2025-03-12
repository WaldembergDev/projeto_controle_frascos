# from src.models.usuario import Usuario

# class DaoUsuario:
#     @classmethod
#     def criar_usuario(cls, session, login, senha, nome):
#         usuario = Usuario(login = login, senha=senha, nome=nome)
#         session.add(usuario)
#         return usuario
    
#     @classmethod
#     def obter_usuario_pelo_id(cls, session, id_usuario):
#         usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
#         return usuario
        
