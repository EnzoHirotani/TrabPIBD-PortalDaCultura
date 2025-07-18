from event_operations import cadastrar_evento, listar_eventos, verificar_disponibilidade, visualizar_evento, editar_evento

def homepage(conn):
    while True:
        print("\n--- Portal da Cultura de São Carlos ---")
        print("1 - Cadastrar Evento")
        print("2 - Listar Eventos")
        print("3 - Visualizar Detalhes do Evento")
        print("4 - Editar Evento")
        print("5 - Verificar disponibilidade de vagas em evento")
        print("0 - Sair")

        option = input("Escolha uma opção: ")

        if option == '0':
            print("Saindo...")
            break

        if option == '1':
            cadastrar_evento(conn)
        elif option == '2':
            listar_eventos(conn)
        elif option == '3':
            visualizar_evento(conn)
        elif option == '4':
            editar_evento(conn)
        elif option == '5':
            verificar_disponibilidade(conn)
        else:
            print("Opção inválida. Tente novamente.")