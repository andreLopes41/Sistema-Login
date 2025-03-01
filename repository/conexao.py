def get_conexao():
    """Retorna a string de conexão com o Banco de Dados

    Returns:
        str: string de conexão do Banco de Dados
    """
    HOST = ''       # Endereço do Servidor SQL
    DATABASE = ''   # Nome do Banco de Dados
    USER = ''       # Usuário do Banco de Dados
    PASSWORD = ''   # Senha de Acesso ao Banco de Dados
    PORT = ''       # Porta do Servidor SQL

    return f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
