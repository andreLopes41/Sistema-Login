from model.User import User
from repository.user_repository import UserRepository
import bcrypt
import re


class UserController:

    usuario_logado = None

    def __init__(self) -> None:
        self.repository = UserRepository()

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> None:
        """Cadastra um novo usuário no sistema.

        Args:
            nome (str): Nome do usuário
            email (str): Email do usuário
            senha (str): Senha do usuário

        Raises:
            ValueError: Se os dados forem inválidos ou email já existir
        """
        if not nome or not email or not senha:
            raise ValueError('Nome, E-mail e Senha são obrigatórios')

        if len(nome) < 3 or len(nome) > 50:
            raise ValueError('O nome deve ter entre 3 e 50 caracteres')

        if len(email) < 6 or len(email) > 50:
            raise ValueError('O E-mmail deve ter entre 6 e 50 caracteres')

        if not self.validar_email(email):
            raise ValueError(
                f'Email inválido! \n   * Formato aceito: usuario@exemplo.com'
            )

        if not self.validar_senha(senha):
            raise ValueError(
                f'Senha inválida! \n   * Deve ter no mínimo 8 caracteres, \n   * Uma letra maiúscula, \n   * Um número, \n   * Um caractere especial'
            )

        if self.repository.find_user(email):
            raise ValueError('Já existe um usuário cadastrado com este E-mail')

        senha_hash = bcrypt.hashpw(
            senha.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        self.repository.create(User(nome=nome, email=email, senha=senha_hash))

    def realizar_login(self, email: str, senha: str) -> bool:
        """Realiza o login do usuário no sistema.

        Args:
            email (str): Email do usuário
            senha (str): Senha do usuário

        Returns:
            bool: True se login bem sucedido, False caso contrário
        """
        user = self.repository.find_user(email)

        if not user:
            return False

        if bcrypt.checkpw(senha.encode('utf-8'), user.senha.encode('utf-8')):
            UserController.usuario_logado = user
            return True
        return False

    def definir_status_login(self, valor: bool) -> None:
        """Define o status de login do usuário.

        Args:
            valor (bool): True para logado, False para deslogado
        """
        if UserController.usuario_logado:
            self.repository.atualizar_status_login(
                UserController.usuario_logado.id, valor
            )

        if not valor:
            UserController.usuario_logado = None

    def validar_email(self, email: str) -> bool:
        """Valida se o email está em formato correto.

        Args:
            email (str): Email para validar

        Returns:
            bool: True se email válido, False caso contrário
        """
        return bool(
            re.match('^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$', email)
        )

    def validar_senha(self, senha: str) -> bool:
        """Valida se a senha atende aos requisitos mínimos.

        Args:
            senha (str): Senha para validar

        Returns:
            bool: True se senha válida, False caso contrário
        """
        if len(senha) < 8:
            return False

        return all(
            [
                bool(re.search(r'[A-Z]', senha)),
                bool(re.search(r'[0-9]', senha)),
                bool(re.search(r'[!@#$%&*]', senha)),
            ]
        )

    def buscar_usuarios(self) -> list[User]:
        """Retorna lista de todos os usuários cadastrados.

        Returns:
            list[User]: Lista de usuários
        """
        return self.repository.find_all_users()

    def atualizar_usuario(
        self,
        email_atual: str,
        novo_nome: str,
        novo_email: str,
        nova_senha: str,
    ) -> None:
        """Atualiza os dados de um usuário existente.

        Args:
            email_atual (str): Email atual do usuário
            novo_nome (str): Novo nome
            novo_email (str): Novo email
            nova_senha (str): Nova senha

        Raises:
            ValueError: Se os dados forem inválidos ou novo email já existir
        """
        if not novo_nome or not novo_email or not nova_senha:
            raise ValueError('Nome, E-mail e Senha são obrigatórios')

        if len(novo_nome) < 3 or len(novo_nome) > 50:
            raise ValueError('O nome deve ter entre 3 e 50 caracteres')

        if len(novo_email) < 6 or len(novo_email) > 50:
            raise ValueError('O E-mmail deve ter entre 6 e 50 caracteres')

        if not self.validar_email(novo_email):
            raise ValueError(
                f'Email inválido! \n   * Formato aceito: usuario@exemplo.com'
            )

        if not self.validar_senha(nova_senha):
            raise ValueError(
                f'Senha inválida! \n   * Deve ter no mínimo 8 caracteres, \n   * Uma letra maiúscula, \n   * Um número, \n   * Um caractere especial'
            )

        user: User = self.repository.find_user(novo_email)

        if user:
            raise ValueError('Já existe um usuário cadastrado com este E-mail')

        senha_hash = bcrypt.hashpw(
            nova_senha.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        self.repository.update(email_atual, novo_nome, novo_email, senha_hash)

    def excluir_usuario(self, email: str) -> None:
        """Exclui um usuário do sistema.

        Args:
            email (str): Email do usuário a ser excluído

        Raises:
            ValueError: Se o usuário estiver logado
        """
        if self.repository.verificar_usuario_logado(email):
            raise ValueError('O usuário logado não pode ser excluído')
        self.repository.delete(email)
