import os
import sys
import questionary

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller.user_controller import UserController
from repository.session import create_table


def limpar_tela():
    """Limpa a tela do console"""

    os.system('cls' if os.name == 'nt' else 'clear')


def pressionar_enter():
    """Aguarda a tecla ENTER ser pressionada para liberar a interface"""

    print('\n')
    input('Pressione ENTER para continuar...')


def exibir_logo():
    """Exibe a logo do sistema"""

    print(
        '███████╗██╗                   ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗'
    )
    print(
        '██╔════╝██║                   ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║'
    )
    print(
        '███████╗██║         █████╗    ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║'
    )
    print(
        '╚════██║██║         ╚════╝    ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║'
    )
    print(
        '███████║███████╗              ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║'
    )
    print(
        '╚══════╝╚══════╝              ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝'
    )
    print(
        '\n                                Sistema de Login                               \n'
    )


def menu_principal():
    """Exbibe o menu principal com as funcionalidades do sistema"""
    while True:
        limpar_tela()
        exibir_logo()

        print('╔════════════════════════════════════╗')
        print('║           MENU PRINCIPAL           ║')
        print('╠════════════════════════════════════╣')
        print('║ [1] ➕ Cadastrar Usuário           ║')
        print('║ [2] 🔒 Realizar Login              ║')
        print('║ [3] 📖 Guia do Sistema             ║')
        print('║ [0] 🚪 Sair                        ║')
        print('╚════════════════════════════════════╝')

        user_input: str = str(input('>> '))

        if user_input == '1':
            cadastrar_usuario()
        elif user_input == '2':
            realizar_login()
        elif user_input == '3':
            menu_guia_sistema()
        elif user_input == '0':
            break
        else:
            print('\n')
            print('⚠️  Opção inválida!')
            pressionar_enter()


def realizar_login():
    """Realiza o login de um Usuário no sistema"""

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║        🔒 REALIZAR LOGIN           ║')
    print('╚════════════════════════════════════╝\n')

    try:
        email: str = str(input('✉️  E-mail: '))
        senha: str = str(input('🔑 Senha: '))

        if usuario_controller.realizar_login(email, senha):
            usuario_controller.definir_status_login(True)
            print('\n')
            print('✅ Login realizado com sucesso.')
            pressionar_enter()
            carregar_sistema()
        else:
            raise ValueError('E-mail ou Senha Inválidos')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}')
        pressionar_enter()


def carregar_sistema():
    """Carrega o sistema após realizar o login"""
    usuario_controller = UserController()
    while True:
        limpar_tela()

        print('╔════════════════════════════════════╗')
        print('║       👥 GERENCIAR USUÁRIOS        ║')
        print('╠════════════════════════════════════╣')
        print('║ [1] ➕ Cadastrar Usuário           ║')
        print('║ [2] 📝 Alterar Usuário             ║')
        print('║ [3] 🗑️  Excluir Usuário             ║')
        print('║ [4] 👁️  Visualizar Usuário          ║')
        print('║ [5] 📜 Listar Usuários             ║')
        print('║ [0] 🔙 LogOut                      ║')
        print('╚════════════════════════════════════╝')

        user_input: str = str(input('>> '))

        if user_input == '1':
            cadastrar_usuario()
        elif user_input == '2':
            alterar_usuario()
        elif user_input == '3':
            excluir_usuario()
        elif user_input == '4':
            visualizar_usuario()
        elif user_input == '5':
            listar_usuarios()
        elif user_input == '0':
            usuario_controller.definir_status_login(False)
            print('\n')
            print('✅ Logout realizado com sucesso.')
            pressionar_enter()
            break
        else:
            print('\n')
            print('⚠️  Opção inválida!')
            pressionar_enter()


def cadastrar_usuario():
    """Faz a inclusão de um novo Usuário no sistema"""

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       ➕ CADASTRAR USUÁRIO         ║')
    print('╚════════════════════════════════════╝\n')

    try:
        nome: str = str(input('Nome: '))
        email: str = str(input('E-mail: '))
        senha: str = str(input('Senha: '))

        usuario_controller.cadastrar_usuario(nome, email, senha)
        print('\n')
        print('✅ Usuário cadastrado com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}')

    pressionar_enter()


def alterar_usuario():
    """Altera um Usuário existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║        📝 ALTERAR USUÁRIO          ║')
    print('╚════════════════════════════════════╝\n')

    try:
        usuarios = usuario_controller.buscar_usuarios()

        menu_usuarios = []
        for usuario in usuarios:
            item = f'{usuario.nome} (E-mail: {usuario.email})'
            menu_usuarios.append(item)

        usuario_escolhido = create_terminal_menu(
            menu_usuarios, 'Selecione o usuário'
        )

        if usuario_escolhido is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_usuarios.index(usuario_escolhido)
        usuario = usuarios[index]

        nome: str = str(input('Novo nome: '))
        email: str = str(input('Novo E-mail: '))
        senha: str = str(input('Nova Senha: '))

        usuario_controller.atualizar_usuario(usuario.email, nome, email, senha)
        print('\n')
        print('✅ Usuário alterado com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def excluir_usuario():
    """Exclui um Usuário existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║        🗑️  EXCLUIR USUÁRIO        ║')
    print('╚════════════════════════════════════╝\n')

    try:
        usuarios = usuario_controller.buscar_usuarios()

        menu_usuarios = []
        for usuario in usuarios:
            item = f'{usuario.nome} (E-mail: {usuario.email})'
            menu_usuarios.append(item)

        usuario_escolhido = create_terminal_menu(
            menu_usuarios, 'Selecione o usuário'
        )

        if usuario_escolhido is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_usuarios.index(usuario_escolhido)
        usuario = usuarios[index]

        usuario_controller.excluir_usuario(usuario.email)
        print('\n')
        print('✅ Usuário excluído com sucesso.')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def visualizar_usuario():
    """Exibe as informações de um Usuário existente no sistema

    Raises:
        ValueError: Caso o usuário cancele a operação do Terminal Menu
    """

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║       👁️  VISUALIZAR USUÁRIO        ║')
    print('╚════════════════════════════════════╝\n')

    try:
        usuarios = usuario_controller.buscar_usuarios()

        menu_usuarios = []
        for usuario in usuarios:
            item = f'{usuario.nome} (E-mail: {usuario.email})'
            menu_usuarios.append(item)

        usuario_escolhido = create_terminal_menu(
            menu_usuarios, 'Selecione o usuário'
        )

        if usuario_escolhido is None:
            raise ValueError('Operação cancelada pelo usuário')

        index = menu_usuarios.index(usuario_escolhido)
        usuario = usuarios[index]

        print('╔════════════════════════════════════╗')
        print(f'  Nome: {usuario.nome}')
        print(f'  Email: {usuario.email}')
        print(f'  Senha: {usuario.senha}')
        print('╚════════════════════════════════════╝')

    except ValueError as e:
        print('\n')
        print(f'❌ {e}.')

    pressionar_enter()


def listar_usuarios():
    """Lista todos os Usuários cadastrados no sistema"""

    usuario_controller = UserController()
    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║        📜 LISTAR USUÁRIOS          ║')
    print('╚════════════════════════════════════╝\n')

    try:
        usuarios = usuario_controller.buscar_usuarios()

        for usuario in usuarios:
            print('╔════════════════════════════════════╗')
            print(f'  Nome: {usuario.nome}')
            print(f'  Email: {usuario.email}')
            print(f'  Senha: {usuario.senha}')
            print('╚════════════════════════════════════╝')
    except ValueError as e:
        print('\n')
        print(f'❌ {e}')

    pressionar_enter()


def menu_guia_sistema() -> None:
    """Exibe o menu com um guia e dicas de utilização do sistema"""

    limpar_tela()

    print('╔════════════════════════════════════╗')
    print('║         📖 GUIA DO SISTEMA         ║')
    print('╚════════════════════════════════════╝\n')

    print('📌 VISÃO GERAL')
    print('O sistema de login possui as seguintes funcionalidades principais:')
    print('• Cadastro de usuários')
    print('• Autenticação de usuários')
    print('• Gerenciamento de usuários\n')

    print('🔐 REQUISITOS DE SEGURANÇA')
    print('Para garantir a segurança, o sistema exige:')
    print('• Senha com no mínimo 8 caracteres')
    print('• Pelo menos uma letra maiúscula')
    print('• Pelo menos um número')
    print('• Pelo menos um caractere especial (!@#$%&*)\n')

    print('👤 GERENCIAMENTO DE USUÁRIOS')
    print('Após fazer login, você pode:')
    print('• Cadastrar novos usuários')
    print('• Alterar dados de usuários existentes')
    print('• Excluir usuários')
    print('• Visualizar informações de usuários')
    print('• Listar todos os usuários cadastrados\n')

    print('💡 DICAS DE NAVEGAÇÃO')
    print('• Use as teclas numéricas para selecionar as opções dos menus')
    print('• Em listas de seleção, use ↑↓ para navegar')
    print('• Pressione Enter para confirmar uma seleção')
    print('• Digite 0 para voltar ao menu anterior\n')

    print('⚠️  OBSERVAÇÕES IMPORTANTES')
    print('• Emails devem ser únicos no sistema')
    print('• Não é possível excluir um usuário que está logado')
    print('• As senhas são armazenadas de forma criptografada')
    print('• Mantenha suas credenciais em segurança\n')

    print('╔══════════════════════════════════════════╗')
    print('║    Desenvolvido por: André Davi Lopes    ║')
    print('║                                          ║')
    print('║  © Copyright 2025 - All Rights Reserved  ║')
    print('╚══════════════════════════════════════════╝\n')

    pressionar_enter()


def create_terminal_menu(itens: list, titulo: str) -> str:
    """Cria um menu interativo no terminal usando a biblioteca Questionary.

    Args:
        itens (list): Lista de opções para exibição no menu.
        titulo (str): Título do menu.

    Returns:
        str: A opção selecionada pelo usuário.
    """
    return questionary.select(
        message=f'{titulo} \n\n ↑↓: Navegar | Enter: Selecionar | CTRL + C: Cancelar \n',
        choices=itens,
        qmark='>>',
        pointer='>> ',
        style=questionary.Style(
            [
                ('pointer', 'fg:#1E90FF bold'),
                ('highlighted', 'fg:#000000 bg:#1E90FF bold'),
                ('selected', 'fg:#000000 bg:#1E90FF bold'),
                ('question', 'bold fg:#FFCC00'),
            ]
        ),
    ).ask()


try:
    create_table()
    menu_principal()
except Exception as e:
    print(f'❌ {e}')
