import psycopg2
import configparser

def conectar():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        conn = psycopg2.connect(
            host=config['postgresql']['host'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=config['postgresql'].get('password', None)
        )

        return conn
    except FileNotFoundError:
        print("Erro: Arquivo 'config.ini' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

if __name__ == "__main__":
    print("Tentando conectar ao banco de dados...")
    conexao = conectar()

    if conexao:
        print("Conexão estabelecida com sucesso!")
        print("Versão do PostgreSQL:", conexao.server_version)
        conexao.close()
    else:
        print("Falha na conexão.")