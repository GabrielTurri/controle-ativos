import os #importa a biblioteca para manipulação do S.O.
import re #Importa a biblioteca re para trabalhar com expressão regulares
import mysql.connector #Importa o conector mySQL para o python
from mysql.connector import Error #Importa o módulo de erro do mySQL
import time #Importa a biblioteca para manipulação de tempo

# CRUD - Create, Read, Update, Delete

# Esta função criará nosso banco de dados de controle de ativos do nosso cliente
# Recebe como parâmetros o host, usuário, senha e o nome do banco de dados
# Retorna True se o banco de dados já existe e False se o banco de dados ainda não foi criado

def criarBD(host, usuario, senha, DB):
    # verificando se o banco de dados já existe
    try:
        connection=mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
            database = DB #Nome do database utilizado
        )
        print("Banco de dados já existe!")
        return True
    except Error as err:
        print("Banco de dados não existe, criando banco de dados...")
        pass
    connection = mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
        )
    cursor = connection.cursor() #Cursor para comunicação com o banco
    cursor.execute("CREATE DATABASE "+ DB) #Executa o comando SQL
    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão
    print(f"Banco de dados '{DB}' criado com sucesso!")
    return False


# Esta função recebe os dados de conexão com o banco de dados
# e o nome do banco de dados que será utilizado
# Cria todas as tabelas do nosso banco de dados

def criarTabelas(host, usuario, senha, DB):
    connection = conectarBD(host, usuario, senha, DB)
    try:
        cursor = connection.cursor()

        # Dicionário com todas as definições SQL necessárias para a criação das nossas tabelas
        tabelas = {
    "grupo_patrimonial": """
        CREATE TABLE grupo_patrimonial (
            id_grupo_patrimonial INT AUTO_INCREMENT PRIMARY KEY,
            nome_grupo VARCHAR(30) NOT NULL
        )
    """,
    "departamento": """
        CREATE TABLE departamento (
            id_departamento INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(40) NOT NULL
        )
    """,
    "modelo_ativo": """
        CREATE TABLE modelo_ativo (
            id_modelo_ativo INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            nome_modelo_ativo VARCHAR(45),
            descricao_modelo_ativo VARCHAR(200)
        )
    """,
    "ativo": """
        CREATE TABLE ativo (
            id_ativo INT AUTO_INCREMENT PRIMARY KEY,
            id_grupo_patrimonial INT NOT NULL,
            id_modelo_ativo INT NOT NULL,
            id_departamento INT NOT NULL,
            patrimonio_ativo CHAR(9) NOT NULL,
            data_aquisicao_ativo DATE NOT NULL,
            data_desativacao_ativo DATE,
            data_vencimento_garantia_ativo DATE,
            valor_aquisicao_ativo DECIMAL(7,2) NOT NULL,
            FOREIGN KEY (id_grupo_patrimonial) REFERENCES grupo_patrimonial (id_grupo_patrimonial),
            FOREIGN KEY (id_modelo_ativo) REFERENCES modelo_ativo (id_modelo_ativo),
            FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento)
        )
    """,
    "licencas_software": """
        CREATE TABLE licencas_software (
            id_software INT AUTO_INCREMENT PRIMARY KEY,
            id_ativo INT NOT NULL,
            nome_software VARCHAR(50) NOT NULL,
            versao_software VARCHAR(30),
            valor_aquisicao_software DECIMAL(7,2) NOT NULL,
            data_aquisicao_software DATE,
            data_expiracao_software DATE,
            FOREIGN KEY (id_ativo) REFERENCES ativo (id_ativo)
        )
    """,
    "manutencao": """
        CREATE TABLE manutencao (
            id_manutencao INT AUTO_INCREMENT PRIMARY KEY,
            data_manutencao DATE NOT NULL,
            data_proxima_manutencao DATE,
            id_ativo INT NOT NULL,
            id_departamento INT NOT NULL,
            FOREIGN KEY (id_ativo) REFERENCES ativo (id_ativo),
            FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento)
        )
    """
}

        # Itera todos os pares do dicionário 'tabelas'
        for tabela_nome, tabela_sql in tabelas.items():
            cursor.execute(tabela_sql) #Executa o comando SQL
            print(f"Tabela {tabela_nome} criada com sucesso.")

    except Error as err:
        print("Erro ao criar as tabelas.", err)
    finally:
        if connection.is_connected(): # Verifica se a conexão está aberta
            cursor.close() #Fecha o cursor
            connection.close() #Fecha a conexão
            print("Todas as tabelas foram criada com sucesso!")


# Esta função recebe os dados de conexão com o banco de dados   
# e o nome do banco de dados que será utilizado
# Retorna a conexão estabelecida com o banco de dados

def conectarBD (host, usuario, senha, DB):
    try:
        connection = mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
            database = DB #Nome do database utilizado
        )
        return connection
    except Error as err:
        print("Erro ao estabelecer conexão com o banco de dados.",err)
        exit()

# Esta função recebe os dados de conexão com o banco de dados
# e os dados do cliente que será cadastrado
# Insere os dados do cliente na tabela Cliente
# E imprime o ID do cliente cadastrado

def inserirRegistro(conn, tabela, dados):
    """
    Insere um registro em uma tabela específica do banco de dados.
        tabela: Nome da tabela onde o registro será inserido.
        dados: Dicionário com pares de coluna e valor correspondentes.
    """
    try:
        cursor = conn.cursor()

        # Preparando a consulta SQL para inserção
        colunas = ', '.join(dados.keys())
        placeholders = ', '.join(['%s'] * len(dados))
        valores = tuple(dados.values())
        insert_query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
        
        # Executando a consulta
        cursor.execute(insert_query, valores)
        conn.commit()
        print(f"\nRegistro inserido com sucesso na tabela {tabela}")

    except Error as err:
        print("Erro ao inserir registro.", err)
    finally:
        cursor.close()

# Esta função recebe os dados de conexão com o banco de dados
# Realiza um select na tabela selecionada
# E imprime todos os registros da tabela

def imprimirRegistrosFormatados(conn, tabela):
    try:
        connection = conn
        cursor = connection.cursor()

        # Executando a consulta
        cursor.execute(f"SELECT * FROM {tabela}")
        registros = cursor.fetchall()

        # Obtendo os nomes das colunas
        colunas = [coluna[0] for coluna in cursor.description]

        # Calculando a largura de cada coluna
        larguras = [len(coluna) for coluna in colunas]
        for registro in registros:
            for i, valor in enumerate(registro):
                larguras[i] = max(larguras[i], len(str(valor)))

        # Imprimindo o cabeçalho
        linha_cabecalho = '+-' + '-+-'.join('-' * largura for largura in larguras) + '-+'
        print(linha_cabecalho)
        cabecalho = '| ' + ' | '.join(f"{coluna.ljust(larguras[i])}" for i, coluna in enumerate(colunas)) + ' |'
        print(cabecalho)
        print(linha_cabecalho)

        # Imprimindo os registros
        for registro in registros:
            linha = '| ' + ' | '.join(f"{str(valor).ljust(larguras[i])}" for i, valor in enumerate(registro)) + ' |'
            print(linha)
        
        # Imprimindo a linha final
        print(linha_cabecalho)

    except Error as err:
        print("Erro ao imprimir tabela.", err)
    finally:
        if connection.is_connected():
            cursor.close()

# Esta função recebe os dados de conexão com o banco de dados
# e os dados da tabela que será atualizado
# Atualiza os registros na dada tabela
# E imprime a quantidade de registros atualizados

def atualizarRegistros(conn, tabela, id_registro):
    try:
        cursor = conn.cursor()

        # Obtendo o nome da chave primária da tabela
        chave_primaria = obterChavePrimaria(conn, tabela)
        if not chave_primaria:
            print(f"Não foi possível encontrar a chave primária para a tabela {tabela}.")
            return

        # Obtendo colunas da tabela
        colunas = obterColunas(conn, tabela)
        dados_atualizacao = {}

        print("Digite os novos valores para as colunas a serem atualizadas:")
        for coluna in colunas:
            cursor.execute(f"SHOW COLUMNS FROM {tabela} LIKE '{coluna}'")
            tipo_coluna = cursor.fetchone()[1]
            valor = input(f"Novo valor para {coluna} (Tipo {tipo_coluna}): ")
            if validarDado(valor, tipo_coluna):
                dados_atualizacao[coluna] = valor

        if not dados_atualizacao:
            print("Nenhuma atualização a ser feita.")
            return

        # Preparando a consulta SQL para atualização
        atualizacoes = ', '.join([f"{coluna} = %s" for coluna in dados_atualizacao])
        valores = tuple(dados_atualizacao.values())

        update_query = f"UPDATE {tabela} SET {atualizacoes} WHERE {chave_primaria} = %s"
        valores += (id_registro,)

        # Executando a consulta
        cursor.execute(update_query, valores)
        conn.commit()

        registros_afetados = cursor.rowcount
        print(f"{registros_afetados} registro(s) atualizado(s) na tabela {tabela}")

    except Error as err:
        print("Erro ao atualizar registros.", err)
    finally:
        cursor.close()

# Esta função recebe os dados de conexão com o banco de dados
# e o ID do registro que será deletado
# Deleta o registro na tabela alvo
# E imprime a quantidade de registros deletados

def deletarRegistro(conn, tabela, id_registro):
    try:
        cursor = conn.cursor()

        # Obtendo o nome da chave primária da tabela
        chave_primaria = obterChavePrimaria(conn, tabela)
        if not chave_primaria:
            print(f"Não foi possível encontrar a chave primária para a tabela {tabela}.")
            return

        # Preparando e executando a consulta SQL para deleção
        delete_query = f"DELETE FROM {tabela} WHERE {chave_primaria} = %s"
        cursor.execute(delete_query, (id_registro,))
        conn.commit()

        registros_afetados = cursor.rowcount
        print(f"{registros_afetados} registro(s) deletado(s) na tabela {tabela}")

    except Error as err:
        print("Erro ao deletar registro.", err)
    finally:
        cursor.close()

# Esta função recebe os dados de conexão com o banco de dados
# e exibe todas as tabelas disponíveis, com o intuito de
# tornar a interface do usuário mais amigável e informativa.

def obterTabelas(conn):
    try:
        connection = conn
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")

        tabelas = [tabela[0] for tabela in cursor.fetchall()]
        return tabelas
    
    except Error as err:
        print("Erro ao obter tabelas.", err)
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Função para obter a chave primária de uma tabela
# para ser usada na função obterColunas e
# na função atualizarRegistros

def obterChavePrimaria(conn, tabela):
    """
    Obtém o nome da coluna da chave primária de uma tabela.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = '{tabela}' 
            AND CONSTRAINT_NAME = 'PRIMARY'
        """)

        resultado = cursor.fetchone()

        return resultado[0] if resultado else None
    
    except Error as err:
        print("Erro ao obter a chave primária.", err)
        return None

# Esta função retorna uma lista de colunas de uma tabela específica
# excluindo a chave primária. Foi pensada para ser usada junto com a função
# de obter tabelas, para tornar a interface do usuário mais amigável e informativa.

def obterColunas(conn, tabela):
    try:
        # Utilizando a função obterChavePrimaria para encontrar a chave primária
        primary_key = obterChavePrimaria(conn, tabela)

        cursor = conn.cursor()

        # Consulta para todas as colunas, excluindo a chave primária
        cursor.execute(f"SHOW COLUMNS FROM {tabela}")
        colunas = [coluna[0] for coluna in cursor.fetchall() if coluna[0] != primary_key]

        return colunas

    except Error as err:
        print("Erro ao obter as colunas.", err)
        return []
    finally:
        cursor.close()

# Função para validar os dados inseridos pelo usuário
# considerando o tipo de dado das tabelas

def validarDado(valor, tipo):
    try:
        if 'int' in tipo:
            # Valida se é um inteiro
            int(valor)
        elif 'varchar' in tipo or 'char' in tipo:
            # Valida se é uma string e verifica o tamanho
            max_length = int(re.search(r'\((\d+)\)', tipo).group(1))
            if not (isinstance(valor, str) and len(valor) <= max_length):
                return False
        elif 'date' in tipo:
            # Valida se é uma data no formato YYYY-MM-DD
            time.strptime(valor, '%Y-%m-%d')
        elif 'decimal' in tipo:
            # Valida se é um decimal
            decimal_match = re.match(r'decimal\((\d+),(\d+)\)', tipo)
            if decimal_match:
                max_digits, decimal_places = map(int, decimal_match.groups())
                float_valor = float(valor)  # Converte para float
                integral, _, fractional = str(float_valor).partition('.')
                if len(integral) + len(fractional) > max_digits or len(fractional) > decimal_places:
                    return False
            else:
                return False
        else:
            return False
    except (ValueError, TypeError):
        return False
    
    return True


# Função para coletar e validar dados

def coletarDadosParaInsercao(conn, tabela):
    colunas = obterColunas(conn, tabela)
    dados = {}

    for coluna in colunas:
        while True:
            valor = input(f"Digite o valor para {coluna}: ")
            # Obtém o tipo da coluna para validação
            cursor = conn.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {tabela} LIKE '{coluna}'")
            tipo_coluna = cursor.fetchone()[1]
            cursor.close()

            if validarDado(valor, tipo_coluna):
                dados[coluna] = valor
                break
            else:
                print(f"Valor inválido para o tipo {tipo_coluna}. Tente novamente.")

    return dados



# Programa Principal
def main():
    # Substitua com suas credenciais do banco de dados 
    host = "18.230.83.138"
    usuario = input("Digite seu nome de usuário: ")
    senha = "abcd=1234"
    DB = "controle_ativex"


    # Inicialização do banco de dados, se necessário
    if not criarBD(host, usuario, senha, DB):
        criarTabelas(host, usuario, senha, DB)
    
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

    tabelas = obterTabelas(conectarBD(host, usuario, senha, DB))

    print("Bem-vindo ao sistema de gerenciamento do banco de dados!")
    print(f"Conectado ao banco de dados: {DB}")

    while True:
        print(":::::: GERENCIADOR DE CONTROLE DE ATIVOS ::::::")    
        print("1 - Inserir Registro")
        print("2 - Ler Registros")
        print("3 - Atualizar Registro")
        print("4 - Deletar Registro")
        print("5 - Sair")

        opcao = input("Digite a opção desejada: ")

        if tabelas:
            print("\nTabelas disponíveis no banco de dados:")
            for tabela in tabelas:
                print("\t", tabela)
        else:
            print("Não foi possível recuperar as tabelas do banco de dados.")         

        if opcao == "1":
            connection = conectarBD(host, usuario, senha, DB)            
            tabela = input("Deseja inserir registros em qual tabela? ")

            dados = coletarDadosParaInsercao(connection, tabela)
        
            inserirRegistro(connection, tabela, dados)
            time.sleep(5)

        elif opcao == "2":
            connection = conectarBD(host, usuario, senha, DB)
            
            tabela = input("Deseja ler os registro de qual tabela? ")
                    
            imprimirRegistrosFormatados(connection, tabela)
            connection.close()
            time.sleep(5)
    
        elif opcao == "3":
            connection = conectarBD(host, usuario, senha, DB)
            
            tabela = input("Digite o nome da tabela para atualização: ")
            imprimirRegistrosFormatados(connection, tabela)

            id_registro = int(input("Digite o valor da chave primária do registro a ser atualizado: "))

            atualizarRegistros(connection, tabela, id_registro)
            time.sleep(5)

        elif opcao == "4":
            connection = conectarBD(host, usuario, senha, DB)
            tabela = input("Digite o nome da tabela de onde deseja deletar o registro: ")

            imprimirRegistrosFormatados(connection, tabela)

            id_registro = input("Digite o valor da chave primária do registro a ser deletado: ")
        
            deletarRegistro(connection, tabela, id_registro)
            time.sleep(5)

        elif opcao == "5":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha um número entre 1 e 5.")


        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()