import os

saque_dia = 0
saldo = 0
extrato = ""

def deposito(saldo, extrato, valor):
    saldo += valor
    extrato += f"Deposito de R$ {valor} realizado.\n"

    return saldo, extrato

def saque(saldo, extrato, valor):
    saldo -= valor
    extrato += f"Saque de R$ {valor} realizado.\n"

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

    if escolha == 1:
        print("Informe o valor do depósito:")
        valor = int(input())
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
        if saque_dia < 3:
            print("Informe o valor do saque:")
            valor = int(input())
            if valor <= 500:
                if valor <= 0:
                    print("Valor inválido! (deve ser maior que zero)")
                    continue
                elif valor > saldo:
                    print("Saldo insuficiente!")
                    continue
                saldo, extrato = saque(saldo, extrato, valor)
                saque_dia += 1
            else:
                print("Limite máximo para saque: 500 R$")
        elif saque_dia >= 3:
            print("Limite de 3 saques diários atingido!")
            continue

    elif escolha == 4:
        print(f"Saldo = {saldo}")
        continue

    elif escolha == 0:
        break
