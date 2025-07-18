from event_operations import cadastrar_evento, listar_eventos, visualizar_evento, editar_evento

def homepage(conn): # Passe o objeto de conexão para a homepage
    while True:
        print("\n--- Portal da Cultura de São Carlos ---")
        print("1 - Cadastrar Evento")
        print("2 - Listar Eventos")
        print("3 - Visualizar Detalhes do Evento")
        print("4 - Editar Evento")
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
        else:
            print("Opção inválida. Tente novamente.")