import psycopg2
import configparser
import os
from datetime import datetime

def conectar():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        conn = psycopg2.connect(
            host=config['postgresql']['host'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password']
        )
        return conn
    except FileNotFoundError:
        print("Erro: Arquivo 'config.ini' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
