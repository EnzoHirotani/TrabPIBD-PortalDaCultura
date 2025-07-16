from home import homepage
from database.connectDB import conectar

if __name__ == "__main__":
    print("Tentando conectar ao banco de dados...")
    conexao = conectar()

    if conexao:
        print("Conexão estabelecida com sucesso!")
        print("Versão do PostgreSQL:", conexao.server_version)
        homepage(conexao)
        conexao.close()
    else:
        print("Falha na conexão.")

