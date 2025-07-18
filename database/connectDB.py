import psycopg2
import configparser
import os

def conectar():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, 'config.ini')

        config = configparser.ConfigParser()
        config.read(config_path)

        password = config['postgresql'].get('password')
        if password == '':
            password = None
        conn = psycopg2.connect(
            host=config['postgresql']['host'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=password,
            client_encoding='UTF8'
        )

        return conn
    except FileNotFoundError:
        print("Erro: Arquivo 'config.ini' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None