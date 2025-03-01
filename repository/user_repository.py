from model.User import User
from repository.session import get_session


class UserRepository:
    @classmethod
    def create(cls, user: User) -> None:
        """Cria um novo usuário no banco de dados.

        Args:
            user (User): Objeto usuário a ser criado
        """
        session = get_session()
        session.add(user)
        session.commit()

    @classmethod
    def find_user(cls, email: str) -> User | None:
        """Busca um usuário pelo email.

        Args:
            email (str): Email do usuário

        Returns:
            User | None: Usuário encontrado ou None
        """
        session = get_session()
        return session.query(User).filter(User.email == email).first()

    @classmethod
    def find_all_users(cls) -> list[User]:
        """Retorna todos os usuários cadastrados.

        Returns:
            list[User]: Lista de usuários
        """
        session = get_session()
        return session.query(User).all()

    @classmethod
    def atualizar_status_login(cls, id: int, valor: bool) -> None:
        """Atualiza o status de login de um usuário.

        Args:
            id (int): ID do usuário
            valor (bool): True para logado, False para deslogado
        """
        session = get_session()
        user = session.query(User).filter(User.id == id).first()
        user.is_logado = valor
        session.commit()

    @classmethod
    def verificar_usuario_logado(cls, email: str) -> bool:
        """Verifica se um usuário está logado no sistema.

        Args:
            email (str): Email do usuário

        Returns:
            bool: True se usuário está logado, False caso contrário
        """
        session = get_session()
        return bool(
            session.query(User).filter_by(email=email, is_logado=True).first()
        )

    @classmethod
    def update(
        cls, email_atual: str, novo_nome: str, novo_email: str, nova_senha: str
    ) -> None:
        """Atualiza os dados de um usuário existente no banco de dados.

        Args:
            email_atual (str): Email atual do usuário a ser atualizado
            novo_nome (str): Novo nome do usuário
            novo_email (str): Novo email do usuário
            nova_senha (str): Nova senha do usuário (já criptografada)
        """
        session = get_session()
        user = session.query(User).filter(User.email == email_atual).first()
        user.nome = novo_nome
        user.email = novo_email
        user.senha = nova_senha
        session.commit()

    @classmethod
    def delete(cls, email: str) -> None:
        """Remove um usuário do banco de dados.

        Args:
            email (str): Email do usuário a ser removido
        """
        session = get_session()
        session.query(User).filter(User.email == email).delete()
        session.commit()
