# Programa: Conta Bancária v3
# Autor: Marcos Belo
# Data: 27/04/2024
# Descrição: Resolução do desafio de código utilizando o paradigma orientado a objetos como forma de concretizar o conhecimento adquirido previamente em aula.

# Importações necessárias
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime, time
import bcrypt

# Função para converter string em objeto datetime
def converter_para_data(data_str: str, formato: str = "%d %m %Y"):
    try:
        data = datetime.strptime(data_str, formato)
        return data
    except ValueError:
        print("Formato de data incorreto. Certifique-se de que a data está no formato especificado.")
        return None

# Função para gerar um hash de senha com salt
def gerar_hash(senha:str):
    salt = bcrypt.gensalt()
    palavra_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return salt, palavra_hash

# Definição da classe Cliente
class Cliente:
    def __init__(self, endereco:str, senha:str):
        self.endereco = endereco
        self.contas = []
        self.salt ,self._hash_senha = gerar_hash(senha)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def verificar_senha(self, palavra: str):
        palavra_hash = bcrypt.hashpw(palavra.encode('utf-8'), self.salt)
        if palavra_hash == self._hash_senha:
            return True
        return False

# Definição da classe PessoaFisica, subclasse de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf:str, nome:str, data_nascimento:datetime, endereco:str, hash_senha:str):
        super().__init__(endereco, hash_senha)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def get_nome(self):
        return self.nome

# Definição da classe Conta
class Conta:
    numero = 0
    def __init__(self, cliente:Cliente):
        Conta.incrementar_quantidade()
        self._saldo = 0.0
        self._numero = Conta.numero
        self._agencia = "0001"
        self._cliente = cliente
        self._extrato = Historico()
        self._saque_diario = 0

    # Método de classe para incrementar o número da conta
    @classmethod
    def incrementar_quantidade(cls):
        cls.numero +=1

    # Método para obter o saldo da conta
    def get_saldo(self):
        return self._saldo

    # Método de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, cliente:Cliente):
        return cls(cliente, cls.numero)

    # Método para realizar um saque na conta
    def sacar(self, valor:float):
        if (valor > self._saldo):
            print("Saldo insuficiente!\n")
            return False
        elif valor > 0:
            self._saldo -= valor
            self._extrato.adicionar_transacao(Saque, valor)
            self._saque_diario += 1
            return True
        else:
            print("Valor inválido, deve ser maior que zero!\n")
            return False

    # Método para realizar um depósito na conta
    def depositar(self, valor:float):
        if valor > 0:
            self._saldo += valor
            self._extrato.adicionar_transacao(Deposito, valor)
            return True
        else:
            print("Valor inválido, deve ser maior que zero!\n")
            return False

# Definição da classe ContaCorrente, subclasse de Conta
class ContaCorrente(Conta):
    def __init__(self,cliente:Cliente):
        super().__init__(cliente)

# Definição da classe Historico
class Historico:
    def __init__(self):
        self.historico = ""

    # Método para adicionar uma transação ao histórico
    def adicionar_transacao(self, transacao, valor):
        operacao = transacao.__name__
        hora_atual = datetime.now().strftime('%H:%M')
        self.historico += (f"{operacao} de {valor:.2f} realizado às {hora_atual}\n")

# Definição da classe Transacao (classe abstrata)
class Transacao(ABC):
    @abstractmethod
    def registrar(conta:Conta):
        pass

# Definição da classe Saque, subclasse de Transacao
class Saque(Transacao):
    extrato_saque = Historico()

    @classmethod
    def registrar(cls,conta:Conta, valor:float):
        cls.extrato_saque.adicionar_transacao(Saque, valor)

# Definição da classe Deposito, subclasse de Transacao
class Deposito(Transacao):
    extrato_deposito = Historico()

    @classmethod
    def registrar(cls,conta: Conta, valor: float):
        cls.extrato_deposito.adicionar_transacao(Deposito, valor)

# Função para exibir o menu principal
def menu(opcao=0):
    if not opcao:
        print("\n______________MENU_______________\n")
        print("Informe a operação desejada:")
        print("1 - DEPOSITO")
        print("2 - SAQUE")
        print("3 - EXTRATO")
        print("4 - CADASTRAR NOVO USUÁRIO")
        print("5 - CRIAR NOVA CONTA")
        print("0 - ENCERRAR")
        print("_________________________________\n")
    else:
        print("\n___________MENU DE EXTRATOS___________\n")
        print("Informe a operação desejada:")
        print("1 - EXTRATO DE CONTAS")
        print("2 - EXTRATO DE TODOS OS DEPÓSITOS")
        print("3 - EXTRATO DE TODOS OS SAQUES\n")

    escolha = int(input())
    print()
    return escolha

# Função para buscar uma conta pelo número
def buscar_conta(registro_conta, numero_conta):
    if len(registro_conta) > 0:
        for conta in registro_conta:
            if conta._numero == numero_conta:
                return conta
    return False

# Função para buscar um cliente pelo CPF
def buscar_cliente(cpf, registro_usuarios):
    if len(registro_usuarios) > 0:
        for cliente in registro_usuarios:
            if cliente.cpf == cpf:
                return cliente
    return False

# Função principal do programa
def main():
    registro_saque = Saque()
    registro_deposito = Deposito()
    registro_usuarios = []
    registro_contas = []
    contador = 0

    # Loop principal do programa
    while True:
        escolha = menu(0)
        match(escolha):
            case 1:  # Depósito
                if contador < 10:
                    cliente = input("Informe o cpf do cliente:\n")
                    if buscar_cliente(cliente, registro_usuarios):
                        conta = int(input("Insira o número da conta que receberá o valor:\n"))
                        conta_obj = buscar_conta(registro_contas, conta)
                        if (conta_obj):
                            valor = float(input("Informe o valor do depósito:\n"))
                            conta_obj.depositar(valor)
                            registro_deposito.registrar(conta_obj, valor)
                            contador += 1
                            continue
                        else:
                            print("A conta informada ainda não foi criada!\n")
                            continue
                    else:
                        print("Cpf informado não é associado a nenhum usuário!\n")
                        continue
                else:
                    print("Limite de transações diárias atingido.\n")
                    continue

            case 2:  # Saque
                conta = int(input("Informe a conta que deseja realizar o saque:\n"))
                conta_obj = buscar_conta(registro_contas, conta)
                if conta_obj:
                    senha = input("Insira a senha de usuário:\n")
                    if conta_obj._cliente.verificar_senha(senha):
                        if conta_obj._saque_diario < 3 and contador < 10:
                            print("Informe o valor do saque:\n")
                            valor = float(input())  # Agora a entrada será tratada como float
                            if valor <= 0:
                                print("Valor inválido! (deve ser maior que zero)\n")
                                continue
                            elif valor > 500:
                                print("Valor máximo permitido para saque: R$ 500\n")
                                continue
                            elif valor > conta_obj.get_saldo():
                                print("Saldo insuficiente!\n")
                                continue
                            conta_obj.sacar(valor)
                            registro_saque.registrar(conta_obj, valor)
                            contador+=1
                            continue
                        else:
                            print("Limite de saques em um único dia atingidos.\n")
                            continue
                    else:
                        print("Senha incorreta!\n")
                else:
                    print("A conta informada ainda não foi criada!\n")
                    continue

            case 3:
                tipo = menu(1)
                match(tipo):
                    case 1:
                        conta = int(input("Informe a conta que você deseja ver o extrato:\n"))
                        conta_obj = buscar_conta(registro_contas, conta)
                        if conta_obj:
                            senha = input("Insira a senha do usuário proprietário da conta:\n")
                            if conta_obj._cliente.verificar_senha(senha):
                                print(f"________EXTRATO DA CONTA {conta_obj._numero}_______\n\n")
                                print(f"SALDO = {conta_obj.get_saldo():.2f}")
                                print(f"AGÊNCIA = {conta_obj._agencia}")
                                print(f"CLIENTE = {conta_obj._cliente.get_nome().upper()}")
                                if len(conta_obj._extrato.historico):
                                    print(f"\n_____MOVIMENTAÇÕES______")
                                    print(conta_obj._extrato.historico)
                                else:
                                    print(f"\n_____SEM MOVIMENTAÇÕES______")
                                print()
                            else:
                                print("Senha incorreta!\n")

                    case 2:
                        print(f"__________EXTRATO DE DEPÓSITOS_________\n\n")
                        print(registro_deposito.extrato_deposito.historico)
                        print()

                    case 3:
                        print(f"___________EXTRATO DE SAQUES__________\n\n")
                        print(registro_saque.extrato_saque.historico)
                        print()

            case 4:  # Cadastrar novo usuário
                cpf = input("informe o cpf do novo usuário:\n")
                if not (buscar_cliente(cpf, registro_usuarios)):
                    nome = input("Informe o nome do usuário:\n")
                    data = input("Informe a data de nascimento:\n")
                    endereco = input("Infome o endereço: (logradouro, numero - bairro - cidade/sigla estado:\n")
                    senha = input("Insira a senha de usuário:\n")
                    usuario = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=converter_para_data(data), endereco=endereco, hash_senha=senha)
                    registro_usuarios.append(usuario)
                    continue
                else:
                    print("Usuário já cadastrado!")
                    continue

            case 5:  # Criar nova conta
                cpf = input("Informe o cpf do usuário:\n")
                cliente = buscar_cliente(cpf, registro_usuarios)
                if cliente:
                    senha = input("Insira a senha de usuário:\n")
                    if cliente.verificar_senha(senha):
                        conta = ContaCorrente(cliente)
                        registro_contas.append(conta)
                        print(f"Conta número: {Conta.numero} criada.\n")
                        continue
                    else:
                        print("Senha incorreta!\n")
                else:
                    print("Cpf informado não é associado a nenhum usuário!\n")
                    continue

            case 0:
                break

main()
