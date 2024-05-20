# Programa: Conta Bancária v2
# Autor: [Marcos Belo]
# Data: [27/04/2024]
# Descrição: Este programa permite ao usuário realizar operações básicas de gerenciamento de finanças, como depósito, saque e visualização de extrato.

# Função para realizar um depósito
def deposito(saldo, extrato, valor,/):
    saldo += valor
    extrato += f"- Deposito de R$ {valor:.2f} realizado.\n"  # Adiciona o depósito ao extrato
    return saldo, extrato

# Função para realizar um saque
def saque(**kwargs):

    kwargs['saldo'] -= kwargs['valor']
    kwargs['extrato'] += f"- Saque de R$ {kwargs['valor']:.2f} realizado.\n"     # Adiciona o saque ao extrato
    return kwargs['saldo'], kwargs['extrato']

# Função para exibir o extrato
def exibir_extrato(saldo, /, **kwargs):
    print(kwargs['extrato'])
    print(f"saldo = {saldo:.2f}")
    print()

# Função para exibir o menu de opções
def menu():
    print("\n______________MENU_______________\n")
    print("Informe a operação desejada:")
    print("1 - DEPOSITO")
    print("2 - EXTRATO")
    print("3 - SAQUE")
    print("4 - CADASTRAR NOVO USUÁRIO")
    print("5 - CRIAR NOVA CONTA")
    print("6 - LISTAR CONTAS")
    print("7 - LISTAR USUÁRIOS")
    print("0 - ENCERRAR")
    print("_________________________________\n")

# Função para verificar se um CPF está na lista de usuários
def cpf_consta(lista,cpf):
    for usuario in lista:
        if cpf in usuario.values():
            return True
    return False

# Função para criar um novo usuário
def criar_usuario(usuarios, /, **kwargs):
    usuarios.append({'cpf': kwargs['cpf'], 'nome': kwargs['nome'], 'data': kwargs['data'], 'endereco': kwargs['endereco']})
    return usuarios

# Função para criar uma nova conta bancária
def criar_conta(contas, registro_contas, /,**kwargs):
    if (kwargs['contador'] < 10):
        kwargs['numero_conta'] = f"0{kwargs['contador']}"
    else:
        kwargs['numero_conta'] = kwargs['contador']

    if(cpf_consta(contas, kwargs['cpf'])):
        for i in range(len(contas)):
            if kwargs['cpf'] in contas[i].values():
                posicao = i
                break
        contas[posicao]['contas'].append(kwargs['numero_conta'])
    else:
        contas.append({'cpf': kwargs['cpf'], 'agencia': kwargs['agencia'], 'contas': [kwargs['numero_conta']]})

    registro_contas.update({kwargs['numero_conta']: {'saldo': 0, 'extrato': "", 'saque_diario': 0}})
    kwargs['contador'] += 1
    return registro_contas, contas, kwargs['contador']

# Função para listar os elementos de uma lista de dicionários
def listar(lista):
    for i in lista:
        for chave,valor in i.items():
            print(chave, "- ", valor)
        print()
    print()

# Função para buscar uma conta no registro de contas
def buscar(registro_conta, conta, contas):
    if conta in registro_conta.keys():
        for i in contas:
            if conta in i['contas']:
                proprietario = i['cpf']
        print(f"conta - {conta}\nProprietario - {proprietario}\n")
        return True
    return False

# Função principal do programa
def main():
    # Inicialização de variáveis
    usuarios = []
    contas = []
    registro_contas = {}
    numero_conta = "0"
    contador = 1

    while True:
        menu()
        escolha = int(input())

        # Realiza a operação escolhida pelo usuário
        if escolha == 1:  # Depósito
            conta = input("Informe o número da conta que será realizada a operação:\n")
            agencia = input("Digite a agência a qual a conta pertence:\n")
            if (buscar(registro_contas, conta, contas) and agencia == "0001"):
                valor = float(input("Informe o valor do depósito:\n"))
                if valor <= 0:
                    print("Valor inválido! (deve ser maior que zero)\n")
                    continue
                registro_contas[conta]['saldo'], registro_contas[conta]['extrato'] = deposito(registro_contas[conta]['saldo'], registro_contas[conta]['extrato'], valor)
            else:
                print("A conta informada ainda não foi criada!")
                continue

        elif escolha == 2:  # Extrato
            conta = input("Informe a conta que deseja exibir o extrato:\n")
            agencia = input("Digite a agência a qual a conta pertence:\n")
            if(buscar(registro_contas, conta, contas) and agencia == "0001"):
                if registro_contas[conta]['extrato'] == "":
                    print("Não foram realizadas movimentações.")
                    continue
                exibir_extrato(registro_contas[conta]['saldo'], extrato=registro_contas[conta]['extrato'])
                continue
            else:
                print("A conta informada ainda não foi criada!")
                continue

        elif escolha == 3:  # Saque
            conta = input("Informe a conta que deseja realizar o saque:\n")
            agencia = input("Digite a agência a qual a conta pertence:\n")
            if(buscar(registro_contas,conta, contas) and agencia == "0001"):
                if registro_contas[conta]['saque_diario'] < 3:
                    print("Informe o valor do saque:")
                    valor = float(input())  # Agora a entrada será tratada como float
                    if valor <= 0:
                        print("Valor inválido! (deve ser maior que zero)")
                        continue
                    elif valor > 500:
                        print("Valor máximo permitido para saque: R$ 500")
                        continue
                    elif valor > registro_contas[conta]['saldo']:
                        print("Saldo insuficiente!")
                        continue
                    registro_contas[conta]['saldo'], registro_contas[conta]['extrato'] = saque(saldo=registro_contas[conta]['saldo'], extrato=registro_contas[conta]['extrato'], valor=valor)
                    registro_contas[conta]['saque_diario'] += 1  # Incrementa o contador de saques diários
                else:
                    print("Limite de saques em um único dia atingidos.")
                    continue
            else:
                print("A conta informada ainda não foi criada!")
                continue

        elif escolha == 4:  # Cadastrar novo usuário
            cpf = input("informe o cpf do novo usuário:\n")

            if not(cpf_consta(usuarios, cpf)):
                nome = input("Informe o nome do usuário:\n")
                data = input("Informe a data de nascimento:\n")
                endereco = input("Infome o endereço: (logradouro, numero - bairro - cidade/sigla estado:\n")
                usuarios = criar_usuario(usuarios, cpf=cpf, nome=nome, data=data, endereco=endereco)
            else:
                print("Usuário já cadastrado!")
                continue

        elif escolha == 5:  # Criar nova conta
            cpf = input("Informe o cpf do usuário:\n")
            registro_contas, contas, contador = criar_conta(contas, registro_contas, cpf=cpf, agencia='0001', conta=numero_conta, contador=contador)

        elif escolha == 6:  # Listar contas
            listar(contas)
        elif escolha == 7:  # Listar usuários
            listar(usuarios)
        elif escolha == 8:  # Exibir registro de contas
            print(registro_contas)
        elif escolha == 0:  # Encerrar
            break

main()