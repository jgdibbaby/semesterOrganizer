import pickle
import os
import time

db = 'database.pkl'

senha_gerente = "admin123"
tentativa = 0

if not os.path.exists(db):
    with open(db, 'wb') as f:
        pickle.dump({}, f)
else:
    try:
        with open(db, 'rb') as f:
            dados = pickle.load(f)
        if not isinstance(dados, dict):
            raise ValueError("Banco de dados não é um dicionário!")
    except Exception:
        with open(db, 'wb') as f:
            pickle.dump({}, f)

print ("Bem-vindo ao sistema bancario")

while True:
  escolha = input("Selecione uma opcao:\n1 - Cliente\n2 - Gerente\n3 - Salvar alteracoes em disco\n0 - Sair\n")
  if escolha == "1": ## CLIENTE
    usuario_cliente = input("Informe o usuario:")
    senha_cliente = input("Informe a senha:")
    if usuario_cliente not in db:
      print("Usuário não encontrado")
      continue
    else:
      if senha_cliente != dados[usuario_cliente]["senha"]:
        print("Senha incorreta")
      else:
        print("Login realizado com sucesso")
    cliente_opcoes = input("Selecione uma opcao:\n1 - Consultar saldo\n2 - Depositar valor\n3 - Sacar valor\n4 - Simular rendimento\n5 - Listar ultimas transacoes (extrato)\n6 - Sair\n")
    if cliente_opcoes == "1":
      print("Consultar saldo")
    elif cliente_opcoes == "2":
      print("Depositar valor")
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
  elif escolha == "2": ## GERENTE 
    gerente_acesso = input("Informe a senha:\t")
    while gerente_acesso != senha_gerente:
      print("Senha incorreta")
      gerente_acesso = input("Informe a senha:\t")
      tentativa += 1
      if tentativa == 3:
        break
    gerente_opcoes = input("Selecione uma opcao:\n1 - Criar conta\n2 - Depositar valor\n3 - Sacar valor\n4 - Simular rendimento\n5 - Listar ultimas transacoes (extrato)\n6 - Sair\n")
  elif escolha == "3": ## SALVAR ALTERACOES EM DISCO
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
