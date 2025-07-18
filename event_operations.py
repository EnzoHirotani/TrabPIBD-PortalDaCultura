from datetime import datetime
import psycopg2
from psycopg2 import Error

# --- Funções Auxiliares ---
def listar_locais_simples(conn):
    """Lista IDs, nomes e capacidade de locais culturais para seleção."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_local, nome, capacidade FROM LocalCultural ORDER BY nome")
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao listar locais: {e}")
        return []

def listar_categorias_simples(conn):
    """Lista IDs e nomes de categorias de eventos para seleção."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_categoria_evento, nome FROM CategoriaEvento ORDER BY nome")
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao listar categorias: {e}")
        return []

# --- Função de Cadastro de Eventos ---
def cadastrar_evento(conn):
    print("\n--- Cadastrar Novo Evento ---")
    titulo = input("Título do evento: ")
    descricao = input("Descrição: ")

    while True:
        try:
            data_inicio_str = input("Data e Hora de Início (DD/MM/YYYY HH:MM:SS): ")
            data_inicio = datetime.strptime(data_inicio_str, '%d/%m/%Y %H:%M:%S')
            data_fim_str = input("Data e Hora de Fim (DD/MM/YYYY HH:MM:SS): ")
            data_fim = datetime.strptime(data_fim_str, '%d/%m/%Y %H:%M:%S')
            if data_fim < data_inicio:
                print("Erro: Data de fim não pode ser anterior à data de início. Tente novamente.")
                continue
            break
        except ValueError:
            print("Formato de data e hora inválido. Use DD/MM/YYYY HH:MM:SS.")

    faixa_etaria = input("Faixa Etária (ex: Livre, +18): ")

    while True:
        try:
            preco = float(input("Preço (0.00 para gratuito): "))
            if preco < 0:
                print("Preço não pode ser negativo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Preço inválido. Use um número (ex: 50.00).")

    print("\nLocais Culturais Disponíveis:")
    locais = listar_locais_simples(conn)
    if not locais:
        print("Nenhum local cultural cadastrado. Por favor, cadastre um local primeiro no banco de dados.")
        return
    for local in locais:
        print(f"ID: {local[0]}, Nome: {local[1]}, Capacidade: {local[2]}")

    while True:
        try:
            id_local = int(input("ID do Local Cultural para o evento: "))
            cursor = conn.cursor()
            cursor.execute("SELECT id_local FROM LocalCultural WHERE id_local = %s", (id_local,))
            if not cursor.fetchone():
                print("ID de local inválido. Por favor, escolha um ID da lista.")
            else:
                break
        except ValueError:
            print("ID de local inválido. Digite um número.")
        except Error as e:
            print(f"Erro ao verificar local: {e}")
            return

    print("\nCategorias de Eventos Disponíveis:")
    categorias = listar_categorias_simples(conn)
    if not categorias:
        print("Nenhuma categoria de evento cadastrada. Por favor, cadastre uma categoria primeiro no banco de dados.")
        return
    for categoria in categorias:
        print(f"ID: {categoria[0]}, Nome: {categoria[1]}")

    while True:
        try:
            id_categoria = int(input("ID da Categoria do Evento: "))
            cursor = conn.cursor()
            cursor.execute("SELECT id_categoria_evento FROM CategoriaEvento WHERE id_categoria_evento = %s", (id_categoria,))
            if not cursor.fetchone():
                print("ID de categoria inválido. Por favor, escolha um ID da lista.")
            else:
                break
        except ValueError:
            print("ID de categoria inválido. Digite um número.")
        except Error as e:
            print(f"Erro ao verificar categoria: {e}")
            return

    print("\nInformação: Será associado ao Organizador de ID 4 (Produtora Eventos+).")
    id_organizador = 4

    try:
        cursor = conn.cursor()
        cursor.execute(
            "CALL sp_CadastrarEventoCompleto(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (titulo, descricao, data_inicio, data_fim, preco, faixa_etaria, id_local, id_categoria, id_organizador)
        )
        conn.commit()
        print("Evento cadastrado com sucesso!")
    except Error as e:
        conn.rollback()
        print(f"Erro ao cadastrar evento: {e}")

def listar_eventos(conn):
    """Simboliza a listagem de eventos."""
    print("\n--- Listar Eventos (Funcionalidade em desenvolvimento) ---")
    print("Esta função exibirá uma lista de todos os eventos futuramente.")
    # Não faz nada real, apenas imprime uma mensagem
    pass

def visualizar_evento(conn):
    """Simboliza a visualização detalhada de um evento."""
    print("\n--- Visualizar Detalhes do Evento (Funcionalidade em desenvolvimento) ---")
    print("Esta função permitirá visualizar detalhes de um evento específico futuramente.")
    # Não faz nada real, apenas imprime uma mensagem
    pass

def editar_evento(conn):
    """Simboliza a edição de um evento."""
    print("\n--- Editar Evento (Funcionalidade em desenvolvimento) ---")
    print("Esta função permitirá editar os dados de um evento existente futuramente.")
    # Não faz nada real, apenas imprime uma mensagem
    pass