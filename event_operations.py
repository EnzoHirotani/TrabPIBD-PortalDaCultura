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
    """Lista todos os eventos cadastrados no sistema."""
    print("\n--- Listar Eventos ---")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 
                    e.id_evento,
                    e.titulo,
                    e.descricao,
                    e.data_inicio,
                    e.data_fim,
                    e.faixa_etaria,
                    e.preco,
                    l.nome as local_nome,
                    c.nome as categoria_nome
                FROM Evento e
                JOIN LocalCultural l ON e.id_local = l.id_local
                JOIN CategoriaEvento c ON e.id_categoria_evento = c.id_categoria_evento
                ORDER BY e.data_inicio
            """)

        eventos = cursor.fetchall()

        if not eventos:
            print("Nenhum evento cadastrado.")
            return

        print(f"{'ID':<5} {'Título':<25} {'Data/Hora':<20} {'Local':<20} {'Categoria':<15} {'Preço':<10}")
        print("-" * 95)

        for evento in eventos:
            id_evento, titulo, descricao, data_inicio, data_fim, faixa_etaria, preco, local_nome, categoria_nome = evento

            data_formatada = data_inicio.strftime('%d/%m/%Y %H:%M')

            titulo_truncado = titulo[:22] + "..." if len(titulo) > 25 else titulo
            local_truncado = local_nome[:17] + "..." if len(local_nome) > 20 else local_nome
            categoria_truncada = categoria_nome[:12] + "..." if len(categoria_nome) > 15 else categoria_nome

            print(f"{id_evento:<5} {titulo_truncado:<25} {data_formatada:<20} {local_truncado:<20} {categoria_truncada:<15} R$ {preco:<7.2f}")

        print(f"\nTotal de eventos: {len(eventos)}")

    except Error as e:
        print(f"Erro ao listar eventos: {e}")

def visualizar_evento(conn):
    """Visualiza os detalhes completos de um evento específico."""
    print("\n--- Visualizar Detalhes do Evento ---")

    try:
        id_evento = int(input("Digite o ID do evento: "))

        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id_evento,
                e.titulo,
                e.descricao,
                e.data_inicio,
                e.data_fim,
                e.faixa_etaria,
                e.preco,
                l.nome as local_nome,
                l.logradouro,
                l.bairro,
                l.cep,
                l.capacidade,
                l.acessibilidade,
                c.nome as categoria_nome
            FROM Evento e
            JOIN LocalCultural l ON e.id_local = l.id_local
            JOIN CategoriaEvento c ON e.id_categoria_evento = c.id_categoria_evento
            WHERE e.id_evento = %s
        """, (id_evento,))

        evento = cursor.fetchone()

        if not evento:
            print("Evento não encontrado.")
            return

        cursor.execute("""
            SELECT u.nome, org.cpf_cnpj
            FROM Organiza_Evento oe
            JOIN Organizador org ON oe.id_usuario_organizador = org.id_usuario
            JOIN Usuario u ON org.id_usuario = u.id_usuario
            WHERE oe.id_evento = %s
        """, (id_evento,))

        organizadores = cursor.fetchall()

        cursor.execute("SELECT fn_ContarInscritos(%s)", (id_evento,))
        total_inscritos = cursor.fetchone()[0]

        cursor.execute("SELECT fn_VerificarVagasDisponiveis(%s)", (id_evento,))
        vagas_disponiveis = cursor.fetchone()[0]

        print("\n" + "="*60)
        print(f"EVENTO: {evento[1]}")
        print("="*60)
        print(f"ID: {evento[0]}")
        print(f"Descrição: {evento[2] if evento[2] else 'Não informada'}")
        print(f"Data de Início: {evento[3].strftime('%d/%m/%Y às %H:%M')}")
        print(f"Data de Fim: {evento[4].strftime('%d/%m/%Y às %H:%M')}")
        print(f"Faixa Etária: {evento[5] if evento[5] else 'Não informada'}")
        print(f"Preço: R$ {evento[6]:.2f}")
        print(f"Categoria: {evento[13]}")

        print("\n--- INFORMAÇÕES DO LOCAL ---")
        print(f"Local: {evento[7]}")
        print(f"Endereço: {evento[8] if evento[8] else 'Não informado'}")
        print(f"Bairro: {evento[9] if evento[9] else 'Não informado'}")
        print(f"CEP: {evento[10] if evento[10] else 'Não informado'}")
        print(f"Capacidade: {evento[11]} pessoas")
        print(f"Acessibilidade: {evento[12] if evento[12] else 'Não informada'}")

        print("\n--- INFORMAÇÕES DE PARTICIPAÇÃO ---")
        print(f"Inscritos: {total_inscritos}")
        print(f"Vagas Disponíveis: {vagas_disponiveis}")

        print("\n--- ORGANIZADORES ---")
        if organizadores:
            for org in organizadores:
                print(f"- {org[0]} (CPF/CNPJ: {org[1]})")
        else:
            print("Nenhum organizador cadastrado.")

        print("="*60)

    except ValueError:
        print("ID do evento deve ser um número.")
    except Error as e:
        print(f"Erro ao visualizar evento: {e}")

def editar_evento(conn):
    """Simboliza a edição de um evento."""
    print("\n--- Editar Evento (Funcionalidade em desenvolvimento) ---")
    print("Esta função permitirá editar os dados de um evento existente futuramente.")
    # Não faz nada real, apenas imprime uma mensagem
    pass

def verificar_disponibilidade(conn):
    """Verifica a disponibilidade de vagas em um evento específico."""
    print("\n--- Verificar Disponibilidade de Vagas ---")

    try:
        id_evento = int(input("Digite o ID do evento: "))

        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                e.titulo, 
                e.data_inicio, 
                e.data_fim,
                l.nome as local_nome,
                l.capacidade
            FROM Evento e
            JOIN LocalCultural l ON e.id_local = l.id_local
            WHERE e.id_evento = %s
        """, (id_evento,))

        evento = cursor.fetchone()

        if not evento:
            print("Evento não encontrado.")
            return

        titulo, data_inicio, data_fim, local_nome, capacidade = evento

        cursor.execute("SELECT fn_ContarInscritos(%s)", (id_evento,))
        total_inscritos = cursor.fetchone()[0]

        cursor.execute("SELECT fn_VerificarVagasDisponiveis(%s)", (id_evento,))
        vagas_disponiveis = cursor.fetchone()[0]

        percentual_ocupacao = (total_inscritos / capacidade) * 100 if capacidade > 0 else 0

        print("\n" + "="*50)
        print(f"DISPONIBILIDADE DE VAGAS")
        print("="*50)
        print(f"Evento: {titulo}")
        print(f"Local: {local_nome}")
        print(f"Data: {data_inicio.strftime('%d/%m/%Y às %H:%M')} até {data_fim.strftime('%d/%m/%Y às %H:%M')}")
        print("-"*50)
        print(f"Capacidade Total: {capacidade} pessoas")
        print(f"Inscritos: {total_inscritos} pessoas")
        print(f"Vagas Disponíveis: {vagas_disponiveis} pessoas")
        print(f"Percentual de Ocupação: {percentual_ocupacao:.1f}%")

        if vagas_disponiveis > 0:
            if percentual_ocupacao < 70:
                status = "🟢 DISPONÍVEL - Muitas vagas"
            elif percentual_ocupacao < 90:
                status = "🟡 DISPONÍVEL - Poucas vagas"
            else:
                status = "🟠 DISPONÍVEL - Vagas limitadas"
        else:
            status = "🔴 LOTADO - Sem vagas"

        print(f"Status: {status}")
        print("="*50)

        if vagas_disponiveis <= 0:
            print("\nEste evento está lotado. Não é possível realizar novas inscrições.")
        elif vagas_disponiveis <= 10:
            print(f"\nATENÇÃO: Restam apenas {vagas_disponiveis} vagas!")

        mostrar_participantes = input("\nDeseja ver a lista de participantes? (s/n): ").lower()
        if mostrar_participantes == 's':
            cursor.execute("""
                SELECT 
                    u.nome,
                    c.cpf,
                    pe.data_inscricao,
                    pe.presenca_confirmada
                FROM Participa_Evento pe
                JOIN Cidadao c ON pe.id_usuario_cidadao = c.id_usuario
                JOIN Usuario u ON c.id_usuario = u.id_usuario
                WHERE pe.id_evento = %s
                ORDER BY pe.data_inscricao
            """, (id_evento,))

            participantes = cursor.fetchall()

            if participantes:
                print(f"\n--- LISTA DE PARTICIPANTES ({len(participantes)}) ---")
                print(f"{'Nome':<25} {'CPF':<15} {'Data Inscrição':<20} {'Presença':<10}")
                print("-" * 70)
                for participante in participantes:
                    nome, cpf, data_inscricao, presenca = participante
                    presenca_status = "Confirmada" if presenca else "Pendente"
                    data_formatada = data_inscricao.strftime('%d/%m/%Y %H:%M')
                    print(f"{nome[:22]:<25} {cpf:<15} {data_formatada:<20} {presenca_status:<10}")
            else:
                print("\nNenhum participante inscrito ainda.")

    except ValueError:
        print("ID do evento deve ser um número.")
    except Error as e:
        print(f"Erro ao verificar disponibilidade: {e}")