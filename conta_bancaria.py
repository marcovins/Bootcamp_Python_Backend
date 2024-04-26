# Programa: Conta Bancária
# Autor: [Marcos Belo]
# Data: [26/04/2024]
# Descrição: Este programa permite ao usuário realizar operações básicas de gerenciamento de finanças, como depósito, saque e visualização de extrato.

import os

# Inicialização de variáveis
saque_diario = 0  # Contador de saques diários
saldo = 0         # Saldo inicial
extrato = ""      # Extrato inicial

# Função para realizar um depósito
def deposito(saldo, extrato, valor):
    saldo += valor
    extrato += f"Deposito de R$ {valor:.2f} realizado.\n"  # Adiciona o depósito ao extrato
    return saldo, extrato

# Função para realizar um saque
def saque(saldo, extrato, valor):
    saldo -= valor
    extrato += f"Saque de R$ {valor:.2f} realizado.\n"     # Adiciona o saque ao extrato
    return saldo, extrato

# Loop principal do programa
while True:
    os.system("cls")  # Limpa a tela do terminal (para Windows)
    print("Informe a operação desejada:")
    print("")
    print("1 - DEPÓSITO")
    print("2 - EXTRATO")
    print("3 - SAQUE")
    print("0 - ENCERRAR")

    escolha = int(input())
    os.system("cls")  # Limpa a tela do terminal (para Windows)

    # Realiza a operação escolhida pelo usuário
    if escolha == 1:  # Depósito
        print("Informe o valor do depósito:")
        valor = float(input())  # Agora a entrada será tratada como float
        if valor <= 0:
            print("Valor inválido! (deve ser maior que zero)")
            continue
        saldo, extrato = deposito(saldo, extrato, valor)

    elif escolha == 2:  # Extrato
        if extrato == "":
            print("Não foram realizadas movimentações.")
            continue
        print(extrato)
        continue

    elif escolha == 3:  # Saque
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
            saque_diario += 1  # Incrementa o contador de saques diários
        else:
            print("Limite de saques em um único dia atingidos.")
            continue

    elif escolha == 0:  # Encerrar
        break
