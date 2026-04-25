import pickle
import os

db = 'database.pkl'
print ("Bem-vindo ao sistema bancario")

escolha = input("Selecione uma opcao:\n1 - Criar conta\n2 - Depositar\n3 - Sacar\n4 - Extrato\n0 - Sair\n")

while escolha != "0":
  if escolha == "1":
    print("Criar conta")
  elif escolha == "2":
    print("Depositar")
  elif escolha == "3":
    print("Sacar")
  elif escolha == "4":
    print("Extrato")
