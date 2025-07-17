from src.dao.dao_usuario import DaoUsuario
from src.database.db import create_session
import bcrypt

class ControllerUsuario:
  @classmethod
  def criar_usuario(cls, login, senha, nome, permissao):
    session = create_session()
    try:
      senha_byte = senha.encode('utf-8')  # Convertendo a senha em bytes
      salt = bcrypt.gensalt()  # Gerando um salt aleatório
      hash_senha = bcrypt.hashpw(senha_byte, salt)      
      DaoUsuario.criar_usuario(session, login, hash_senha, nome, permissao)
      session.commit()
      return True
    except Exception as e:
      session.rollback()
      return False
    finally:
      session.close()

  @classmethod
  def verificar_login(cls, login, senha):
    session = create_session()
    try:
        usuario = DaoUsuario.obter_usuario_pelo_login(session, login)

        if not usuario:
            print("Usuário não encontrado.")
            return False

        hash_armazenado = usuario.senha
        if isinstance(hash_armazenado, str):
            hash_armazenado = hash_armazenado.encode('utf-8')

        if bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado):
            print("Senha correta!")
            return True
        else:
            print("Senha incorreta.")
            return False

    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return False

    finally:
        session.close()  
  