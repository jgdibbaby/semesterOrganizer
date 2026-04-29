import pickle
import os
from datetime import datetime

db = "4. bank system/database.pkl"

gerente = {
  "login": "admin",
  "senha": "123"
}


tentativa = 0

if not os.path.exists(db):
    with open(db, 'wb') as f:
        dados = pickle.dump({}, f)
else:
    try:
        with open(db, 'rb') as f:
            dados = pickle.load(f)
        if not isinstance(dados, dict):
            raise ValueError("Banco de dados não é um dicionário!")
    except Exception:
        with open(db, 'wb') as f:
            dados = pickle.dump({}, f)

print ("Bem-vindo ao sistema bancario")

while True:

  escolha = input("Selecione uma opcao:\n1 - Cliente\n2 - Gerente\n3 - Salvar alteracoes em disco\n0 - Sair\n")

## ------------ MODO CLIENTE ------------ ##

  if escolha == "1": 
    cliente_opcoes = input("Selecione uma opcao:\n1 - Consultar saldo\n2 - Depositar valor\n3 - Sacar valor\n4 - Simular rendimento\n5 - Listar ultimas transacoes (extrato)\n6 - Sair\n")
    
    if cliente_opcoes == "1": 
      print("Consultar saldo")
      

    elif cliente_opcoes == "2":

      valor_deposito = float(input("Informe o valor a ser depositado: "))

      if valor_deposito != 0:
        dados["cliente"] = {
          "saldo": valor_deposito,
          "extrato": [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - Deposito: R$ " + str(valor_deposito)
          ]
        }

        try:
          with open(db, "wb") as f:
            pickle.dump(dados, f)
          print("Depósito realizado e salvo com sucesso!")
        except Exception as e:
          print(f"Erro ao salvar: {e}")

    elif cliente_opcoes == "3":
      print("Sacar valor")
    elif cliente_opcoes == "4":
      print("Simular rendimento")
    elif cliente_opcoes == "5":
      print("Listar ultimas transacoes (extrato)")
    elif cliente_opcoes == "6":
      continue
    else:
      print("Opcao invalida")

## ------------ MODO GERENTE ------------ ##

  elif escolha == "2":
    login_gerente = input("Informe o login:\t")
    senha_gerente = input("Informe a senha:\t")
    while login_gerente != gerente["login"] or senha_gerente != gerente["senha"]:
      print("Senha incorreta")
      login_gerente = input("Informe o login:\t")
      senha_gerente = input("Informe a senha:\t")
      tentativa += 1
      if tentativa == 3:
        print("Senha inválida...\tTente Novamente")
        break

    if login_gerente == gerente["login"] and senha_gerente == gerente["senha"]:
      print("Login bem-sucedido!")
    
    gerente_opcoes = input("Selecione uma opcao:\n1 - Cadastrar ou alterar o nome de um cliente\n2 - Corrigir Saldo\n3 - Consultar Dados de um Cliente\n4 - Listar ultimas transacoes (extrato)\n0 - Sair\n")
    
    if gerente_opcoes == "1":
        nome_cliente = input("Informe o nome do cliente:\t")
        saldo_cliente = float(input("Informe o saldo do cliente:\t"))

        if nome_cliente and saldo_cliente:
            dados["cliente"] = {
              "nome": nome_cliente,
              "saldo": saldo_cliente,
              "extrato": [
            datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - Saldo: R$ " + str(saldo_cliente)
          ]
            }

            with open(db, "wb") as f:
              pickle.dump(dados, f)
            print("Cliente cadastrado com sucesso!")
        else:
            print("Erro ao cadastrar cliente!")
    elif gerente_opcoes == "2":
      novo_saldo = input("Informe o novo saldo do cliente:\t")
      if novo_saldo:
        dados["cliente"] = {
          "saldo": float(novo_saldo),
          "extrato": []
        }
        with open(db, "wb") as f:
          pickle.dump(dados, f)

        print("Saldo corrigido com sucesso!")
    elif gerente_opcoes == "3":
      with open(db, "rb") as f:
        dados = pickle.load(f)

    elif gerente_opcoes == "4":
      with open(db, "rb") as f:
        dados = pickle.load(f)

    elif gerente_opcoes == "0":
        continue
    else:
        print("Opcao invalida")

## ------------ SALVAR OS DADOS, GARANTINDO A PERSISTÊNCIA DOS DADOS ------------ ##

  elif escolha == "3": 
    salvar_alteracoes = input("Deseja salvar as alteracoes em disco? (s/n)")
    if salvar_alteracoes == "s":
      with open(db, 'wb') as f:
        pickle.dump(dados, f)
      print("Alteracoes salvas com sucesso")
    else:
      print("Alteracoes nao salvas")

  elif escolha == "0": ## SAIR
    break
  else:
    print("Opcao invalida")
