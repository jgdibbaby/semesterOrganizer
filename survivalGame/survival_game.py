# ============================================================
#   JOGO DO EMPREENDEDOR
#   Ferramentas usadas: if, elif, else, while, variaveis
# ============================================================

print("=" * 50)
print("       BEM-VINDO AO JOGO DO EMPREENDEDOR!")
print("=" * 50)
print("Voce tem R$10.000 para comecar sua jornada.")
print("Cada decisao muda tudo. Pense bem!\n")

dinheiro = 10000
titulo = "Aprendiz"  # titulo padrao, vai mudando conforme o jogo

# ============================================================
#   PRIMEIRA DECISAO — Lavanderia ou Bolsa de Valores
# ============================================================

print("-" * 50)
print("PRIMEIRA DECISAO")
print("-" * 50)
print("O que voce quer fazer com seus R$10.000?")
print("  [1] Abrir uma Lavanderia (investimento fisico)")
print("  [2] Investir na Bolsa de Valores (mercado)")

escolha1 = ""
while escolha1 != "1" and escolha1 != "2":
    escolha1 = input("\nDigite 1 ou 2: ")
    if escolha1 != "1" and escolha1 != "2":
        print("Opcao invalida! Digite apenas 1 ou 2.")


# ============================================================
#   CAMINHO 1 — LAVANDERIA
# ============================================================

if escolha1 == "1":
    dinheiro = dinheiro - 10000  # investiu tudo
    print("\n>> Voce abriu sua lavanderia! Investiu R$10.000.")
    print(">> Mes 1: O negocio esta lucrando R$2.000/mes!")
    print("   Voce quer reinvestir o lucro?")
    print("  [1] Comprar maquinas novas (-R$2.000 agora, mais retorno depois)")
    print("  [2] Pegar emprestimo no banco (-R$500/mes de juros)")
    print("  [3] Nao fazer nada (guardar o dinheiro)")

    escolha2 = ""
    while escolha2 != "1" and escolha2 != "2" and escolha2 != "3":
        escolha2 = input("\nDigite 1, 2 ou 3: ")
        if escolha2 != "1" and escolha2 != "2" and escolha2 != "3":
            print("Opcao invalida! Digite 1, 2 ou 3.")

    if escolha2 == "1":
        lucro_mensal = 2000 - 2000   # gastou na maquina no mes 1
        ganho_4_meses = (2000 * 4) - 2000  # retorno nos 4 meses ja com desconto
        dinheiro = dinheiro + ganho_4_meses
        print("\n>> Voce comprou maquinas! Custou R$2.000 agora.")
        print(">> Nos proximos 4 meses você lucrou: R$" + str(ganho_4_meses))

    elif escolha2 == "2":
        ganho_4_meses = (2000 * 4) - (500 * 4)  # lucro menos juros
        dinheiro = dinheiro + ganho_4_meses
        print("\n>> Voce pegou emprestimo no banco (-R$500/mes de juros).")
        print(">> Nos proximos 4 meses voce lucrou: R$" + str(ganho_4_meses))

    else:
        ganho_4_meses = 2000 * 4  # sem gastos extras
        dinheiro = dinheiro + ganho_4_meses
        print("\n>> Voce nao fez nada. Guardou o lucro.")
        print(">> Nos proximos 4 meses voce lucrou: R$" + str(ganho_4_meses))

    # Venda da lavanderia (acontece sempre no caminho lavanderia)
    dinheiro = dinheiro + 10000
    print("\n>> Voce vendeu a lavanderia por R$10.000 extra!")
    print(">> Seu dinheiro agora: R$" + str(dinheiro))

    if dinheiro >= 20000:
        titulo = "Empreendedor"
    if dinheiro >= 25000:
        titulo = "Magnata"


# ============================================================
#   CAMINHO 2 — BOLSA DE VALORES
# ============================================================

elif escolha1 == "2":
    investido = 5000
    dinheiro = dinheiro - investido  # investiu metade
    valor_atual = 5000

    print("\n>> Voce investiu R$5.000 na bolsa. Ficou com R$5.000 guardado.")
    print(">> Mes 1: CRASH! Suas acoes caíram 50%.")
    print("   Agora valem apenas R$2.500.")
    print("   O que voce faz?")
    print("  [1] Vender agora e pegar R$2.500")
    print("  [2] Continuar e ver o que acontece...")

    valor_atual = 2500

    escolha2 = ""
    while escolha2 != "1" and escolha2 != "2":
        escolha2 = input("\nDigite 1 ou 2: ")
        if escolha2 != "1" and escolha2 != "2":
            print("Opcao invalida! Digite 1 ou 2.")

    if escolha2 == "1":
        dinheiro = dinheiro + valor_atual
        print("\n>> Voce vendeu! Recuperou R$2.500.")
        print(">> Seu dinheiro agora: R$" + str(dinheiro))

    else:
        # Mes 2
        valor_atual = valor_atual - (valor_atual * 50 // 100)  # cai mais 50%
        print("\n>> Mes 2: Caiu mais 50%! Suas acoes valem R$" + str(valor_atual) + " agora.")
        print("   O que voce faz?")
        print("  [1] Vender agora e pegar R$" + str(valor_atual))
        print("  [2] Continuar apostando na recuperacao...")

        escolha3 = ""
        while escolha3 != "1" and escolha3 != "2":
            escolha3 = input("\nDigite 1 ou 2: ")
            if escolha3 != "1" and escolha3 != "2":
                print("Opcao invalida! Digite 1 ou 2.")

        if escolha3 == "1":
            dinheiro = dinheiro + valor_atual
            print("\n>> Voce vendeu! Recuperou R$" + str(valor_atual) + ".")
            print(">> Seu dinheiro agora: R$" + str(dinheiro))

        else:
            # Mes 3 — recuperacao epica
            valor_atual = valor_atual + (valor_atual * 1000 // 100)  # +1000%
            print("\n>> Mes 3: RECUPERACAO EPICA! +1000%!")
            print("   Suas acoes valem R$" + str(valor_atual) + "!")
            print("   O que voce faz?")
            print("  [1] Vender agora — lucro garantido!")
            print("  [2] Continuar... quem sabe sobe mais?")

            escolha4 = ""
            while escolha4 != "1" and escolha4 != "2":
                escolha4 = input("\nDigite 1 ou 2: ")
                if escolha4 != "1" and escolha4 != "2":
                    print("Opcao invalida! Digite 1 ou 2.")

            if escolha4 == "1":
                dinheiro = dinheiro + valor_atual
                print("\n>> Voce vendeu na hora certa! R$" + str(valor_atual) + " no bolso!")
                titulo = "Magnata"
            else:
                # Mes 4 — perde tudo
                valor_atual = 0
                dinheiro = dinheiro + valor_atual
                print("\n>> Mes 4: COLAPSO TOTAL! As acoes viraram po. R$0.")
                print(">> Voce perdeu tudo que tinha investido na bolsa.")

    print(">> Seu dinheiro agora: R$" + str(dinheiro))

    if dinheiro >= 15000:
        titulo = "Empreendedor"
    if dinheiro >= 20000:
        titulo = "Magnata"


# ============================================================
#   SEGUNDA JORNADA — Igual para os dois caminhos
# ============================================================

print("\n" + "=" * 50)
print("       SEGUNDA JORNADA")
print("  Cansado, mas muito mais experiente...")
print("=" * 50)
print("\nVoce tem R$" + str(dinheiro) + " agora.")
print("O que voce decide fazer com sua vida?")
print("  [1] Abrir um novo negocio (risco e recompensa)")
print("  [2] Reinvestir com mais cautela (crescimento solido)")
print("  [3] Descansar (perda de oportunidade)")

escolha_final = ""
while escolha_final != "1" and escolha_final != "2" and escolha_final != "3":
    escolha_final = input("\nDigite 1, 2 ou 3: ")
    if escolha_final != "1" and escolha_final != "2" and escolha_final != "3":
        print("Opcao invalida! Digite 1, 2 ou 3.")

if escolha_final == "1":
    print("\n>> Voce abriu um novo negocio!")
    print("   Alto risco, mas o retorno pode ser enorme.")
    print("   RESULTADO VARIAVEL — pode ir muito bem ou muito mal.")
    dinheiro = dinheiro + (dinheiro * 50 // 100)  # +50% de retorno variavel
    print(">> Seu dinheiro final: R$" + str(dinheiro))
    if dinheiro >= 20000:
        titulo = "Magnata"

elif escolha_final == "2":
    print("\n>> Voce reinvestiu com cabeca fria!")
    print("   Crescimento solido. Retorno moderado, mas garantido.")
    dinheiro = dinheiro + (dinheiro * 20 // 100)  # +20% solido
    print(">> Seu dinheiro final: R$" + str(dinheiro))
    if dinheiro >= 15000 and titulo == "Aprendiz":
        titulo = "Empreendedor"

else:
    print("\n>> Voce decidiu descansar.")
    print("   Capital parado perde valor com o tempo.")
    print("   Estagnacao — nenhum crescimento.")
    print(">> Seu dinheiro final: R$" + str(dinheiro))


# ============================================================
#   RESULTADO FINAL
# ============================================================

print("\n" + "=" * 50)
print("            RESULTADO FINAL")
print("=" * 50)
print("Dinheiro acumulado: R$" + str(dinheiro))

if dinheiro < 5000:
    titulo = "Aprendiz"
    print("Resultado: Voce passou por muitas pedras...")
elif dinheiro < 15000:
    titulo = "Aprendiz"
    print("Resultado: Experiencia adquirida, capital conservado.")
elif dinheiro < 25000:
    if titulo == "Aprendiz":
        titulo = "Empreendedor"
    print("Resultado: Voce soube tomar boas decisoes!")
else:
    titulo = "Magnata"
    print("Resultado: Excelente! Voce dominou o jogo!")

print("\n  >> SEU TITULO: " + titulo + " <<")
print("=" * 50)
print("Obrigado por jogar o Jogo do Empreendedor!")
print("=" * 50)