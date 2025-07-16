import psycopg2
import configparser

# A função que queremos testar é esta:
def conectar():
    """Lê o arquivo config.ini e tenta conectar ao banco de dados."""
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        print("[INFO] Lendo o arquivo config.ini...")
        print(f"[INFO] Tentando conectar ao host '{config['postgresql']['host']}' no banco '{config['postgresql']['dbname']}'...")

        conn = psycopg2.connect(
            host=config['postgresql']['host'],
            dbname=config['postgresql']['dbname'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password']
        )
        
        print("[SUCESSO] Conexão estabelecida com sucesso!")
        return conn

    except FileNotFoundError:
        print("[ERRO] O arquivo 'config.ini' não foi encontrado no mesmo diretório do script.")
        return None
    except psycopg2.OperationalError as e:
        print(f"[ERRO DE CONEXÃO] Não foi possível conectar ao servidor. Verifique se o servidor está rodando e se os dados estão corretos.")
        print(f"   Detalhe do erro: {e}")
        return None
    except Exception as e:
        print(f"[ERRO INESPERADO] Ocorreu um erro: {e}")
        return None

# --- Bloco Principal de Execução ---
# Este bloco é executado quando você roda o script diretamente.
# Em vez de chamar o menu, vamos chamar apenas a função conectar().
if __name__ == "__main__":
    print("--- INICIANDO TESTE DE CONEXÃO ---")
    
    # Chama a função e armazena o que ela retornar
    conexao_teste = conectar()
    
    # Imprime o resultado para análise
    print(f"\nO valor retornado pela função foi: {conexao_teste}")
    
    # Verifica o resultado de forma clara
    if conexao_teste:
        print("\n[RESULTADO FINAL]: ✅ SUCESSO! O script conseguiu se conectar ao banco de dados.")
        # É uma boa prática fechar a conexão depois de usá-la
        conexao_teste.close()
        print("[INFO] Conexão de teste fechada.")
    else:
        print("\n[RESULTADO FINAL]: ❌ FALHA! O script não conseguiu se conectar.")
        
    print("\n--- TESTE DE CONEXÃO FINALIZADO ---")

