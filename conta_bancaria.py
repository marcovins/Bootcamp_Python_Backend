import os

saque_diario = 0
saldo = 0
extrato = ""

def deposito(saldo, extrato, valor):
    saldo += valor
    extrato += f"Deposito de R$ {valor:.2f} realizado.\n"
    return saldo, extrato

def saque(saldo, extrato, valor):
    saldo -= valor
    extrato += f"Saque de R$ {valor:.2f} realizado.\n"
    return saldo, extrato

while True:
    os.system("cls")
    print("Informe a operação desejada:")
    print("")
    print("1 - DEPOSITO")
    print("2 - EXTRATO")
    print("3 - SAQUE")
    print("0 - ENCERRAR")

    escolha = int(input())
    os.system("cls")

    if escolha == 1:
        print("Informe o valor do depósito:")
        valor = float(input())  # Agora a entrada será tratada como float
        if valor <= 0:
            print("Valor inválido! (deve ser maior que zero)")
            continue
        saldo, extrato = deposito(saldo, extrato, valor)

    elif escolha == 2:
        if extrato == "":
            print("Não foram realizadas movimentações.")
            continue
        print(extrato)
        continue

    elif escolha == 3:
        if saque_diario < 3:
            print("Informe o valor do saque:")
            valor = float(input())  # Agora a entrada será tratada como float
            if valor <= 0:
                print("Valor inválido! (deve ser maior que zero)")
                continue
            elif valor > 500:
                print("Valor máximo permitido para saque: R$ 500")
                continue
            elif valor > saldo:
                print("Saldo insuficiente!")
                continue
            saldo, extrato = saque(saldo, extrato, valor)
            saque_diario += 1  # Incrementando o contador de saques diários
        else:
            print("Limite de saques em um único dia atingidos.")
            continue

    elif escolha == 0:
        break
