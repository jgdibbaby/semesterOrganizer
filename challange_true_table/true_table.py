"""
TABELA VERDADE — Código comentado linha a linha
Cada comentário mostra o que acontece E como seria em TypeScript
"""

import re
from itertools import product

def split(expressao: str) -> list:

    separar_expressoes = re.compile(
        r'<->'       # tenta casar "<->" primeiro (bicondicional)
        r'|->'       # senão tenta "->" (condicional)
        r'|[A-Z]'   # senão tenta uma letra maiúscula (proposição)
        r'|[()^v!~]' # senão tenta um símbolo avulso
    )

    expressoes = separar_expressoes.findall(expressao)

    if not expressoes:
        raise ValueError("Expressao invalida ou vazia.")

    return expressoes

class No:
    # TS equivalente:
    # class No { ... }
    # Classe é classe nos dois. Mesma ideia.

    def __init__(self, tipo, *filhos, valor=None):
        # __init__ em Python == constructor() em TypeScript
        # TS equivalente:
        # constructor(tipo: string, filhos: No[] = [], valor: string | null = null)

        self.tipo = tipo
        # TS: this.tipo = tipo
        # "self" em Python == "this" em TypeScript. Sempre.

        self.filhos = filhos
        # TS: this.filhos = filhos
        # Guarda os nós filhos (ex: lado esquerdo e direito de um ^)

        self.valor = valor
        # TS: this.valor = valor
        # Usado só quando o nó é uma variável (ex: 'A', 'B')

    def avaliar(self, valores: dict) -> bool:

        if self.tipo == 'VAR':
            return valores[self.valor]

        if self.tipo == 'NEG':
            return not self.filhos[0].avaliar(valores)

        # Daqui pra baixo todos os operadores têm dois filhos (esq e dir)
        esq = self.filhos[0].avaliar(valores)

        dir = self.filhos[1].avaliar(valores)

        if self.tipo == 'E':
            return esq and dir

        if self.tipo == 'OU':
            return esq or dir

        if self.tipo == 'COND':
            return (not esq) or dir

        if self.tipo == 'BICOND':
            return esq == dir

# ─────────────────────────────────────────────────────────────
# PARTE 3 — PARSER RECURSIVO
# Objetivo: ler a lista de expressões e montar a árvore de Nós
# A ordem dos métodos define a prioridade dos operadores
# ─────────────────────────────────────────────────────────────

class Parser:

    def __init__(self, expressoes: list):
        # TS: constructor(tokens: string[])

        self.expressoes = expressoes
        # TS: this.tokens = tokens
        # Guarda a lista completa de tokens

        self.cursor = 0
        # TS: this.pos = 0
        # É um "cursor" — aponta qual expressoes estamos lendo agora
        # Começa no 0 (primeiro expressoes)

    def atual(self):
        # TS equivalente:
        # atual(): string | null { ... }
        # Retorna o expressoes na posição atual do cursor

        if self.cursor < len(self.expressoes):
            return self.expressoes[self.cursor]
        # TS: if (this.pos < this.expressoes.length) return this.expressoes[this.pos]
        # Se ainda tem expressoes pra ler, retorna o atual

        return None
        # TS: return null
        # Se acabou os expressoes, retorna null (chegou no fim)

    def consumir(self, esperado=None):
        # TS: consumir(esperado: string | null = null): string
        # "Consome" a expressao atual: lê ele e avança o cursor

        expressao = self.atual()
        # TS: const expressao = this.atual()
        # Pega a expressao atual antes de avançar

        if esperado and expressao != esperado:
            raise ValueError(f"Esperava '{esperado}', encontrei '{expressao}'")
        # TS: if (esperado && token !== esperado) throw new Error(...)
        # Validação: se esperava um token específico e veio outro, erro
        # Ex: esperava ')' mas veio 'A' — expressão malformada

        self.pos += 1
        # TS: this.pos++
        # Avança o cursor pro próximo token

        return expressao
        # Retorna o token que foi consumido

    # ──────────────────────────────────────────
    # OS 5 MÉTODOS ABAIXO são o coração do parser
    # Cada um cuida de um operador, do menor pro maior prioridade
    # Cada um CHAMA O PRÓXIMO — isso é o que garante a prioridade
    # ──────────────────────────────────────────

    def parse_bicondicional(self):
        # TS: parseBicondicional(): No
        # Prioridade 4 — MENOR. Entra primeiro, processa por último.

        esq = self.parse_condicional()
        # TS: let esq = this.parseCondicional()
        # Antes de processar o <->, deixa o lado esquerdo ser resolvido
        # pela função de MAIOR prioridade (condicional)
        # Isso garante que tudo à esquerda do <-> já está "agrupado"

        while self.atual() == '<->':
            # TS: while (this.atual() === '<->') { ... }
            # Fica em loop enquanto tiver <-> na expressão
            # Isso permite encadear: A <-> B <-> C

            self.consumir('<->')
            # Avança o cursor passando o '<->'

            dir = self.parse_condicional()
            # TS: const dir = this.parseCondicional()
            # Resolve o lado direito também com prioridade maior

            esq = No('BICOND', esq, dir)
            # TS: esq = new No('BICOND', [esq, dir])
            # Cria um nó BICOND com esq e dir como filhos
            # E esse nó vira o novo "esq" — pronto pra encadear

        return esq

    def parse_condicional(self):
        # TS: parseCondicional(): No
        # Prioridade 3. Mesma lógica do bicondicional, mas para ->

        esq = self.parse_ou()
        # Antes de processar ->, deixa o lado esquerdo ir pro OU

        while self.atual() == '->':
            self.consumir('->')
            dir = self.parse_ou()
            esq = No('COND', esq, dir)
            # Cria nó COND e encadeia

        return esq

    def parse_ou(self):
        # TS: parseOu(): No
        # Prioridade 2. Para o operador "v"

        esq = self.parse_e()
        # Antes de processar v, deixa o lado esquerdo ir pro E

        while self.atual() == 'v':
            self.consumir('v')
            dir = self.parse_e()
            esq = No('OU', esq, dir)

        return esq

    def parse_e(self):
        # TS: parseE(): No
        # Prioridade 1 (maior entre os binários). Para o operador "^"

        esq = self.parse_negacao()
        # Antes de processar ^, deixa o lado esquerdo ir pra negação

        while self.atual() == '^':
            self.consumir('^')
            dir = self.parse_negacao()
            esq = No('E', esq, dir)

        return esq

    def parse_negacao(self):
        # TS: parseNegacao(): No
        # Prioridade máxima entre os operadores unários

        if self.atual() in ('!', '~'):
            # TS: if (this.atual() === '!' || this.atual() === '~')
            # Se o token atual é um símbolo de negação

            self.consumir()
            # Consome o ! ou ~

            filho = self.parse_negacao()
            # RECURSÃO: chama a si mesmo
            # Isso permite !!A, ~~~B — negações encadeadas
            # TS: const filho = this.parseNegacao()

            return No('NEG', filho)
            # Cria nó de negação com o filho

        return self.parse_atomico()
        # Se não tem negação, vai pro nível mais baixo: átomo

    def parse_atomico(self):
        # TS: parseAtomico(): No
        # O nível mais básico: uma variável (A, B...) ou (sub-expressão)

        token = self.atual()
        # Pega o token atual

        if token == '(':
            # Se for abre-parêntese, tem uma sub-expressão dentro

            self.consumir('(')
            # Consome o '('

            no = self.parse_bicondicional()
            # REINICIA do nível mais baixo de prioridade
            # Tudo dentro dos parênteses é tratado como expressão nova
            # TS: const no = this.parseBicondicional()

            self.consumir(')')
            # Consome o ')' — se não tiver, lança erro

            return no
            # Retorna o nó da sub-expressão

        if token and re.match(r'[A-Z]', token):
            # TS: if (token && /[A-Z]/.test(token))
            # Se for uma letra maiúscula, é uma proposição (A, B, C...)

            self.consumir()
            # Consome a letra

            return No('VAR', valor=token)
            # TS: return new No('VAR', [], token)
            # Cria um nó folha do tipo VAR com o nome da proposição

        raise ValueError(f"Token inesperado: '{token}'")
        # TS: throw new Error(`Token inesperado: '${token}'`)
        # Se não é nenhuma das opções acima, a expressão está errada

    def parse(self):
        # TS: parse(): No
        # Método público — é esse que você chama de fora

        arvore = self.parse_bicondicional()
        # Começa sempre pelo de menor prioridade
        # A árvore inteira é montada a partir daqui

        if self.atual() is not None:
            raise ValueError(f"Tokens nao consumidos: {self.tokens[self.pos:]}")
        # TS: if (this.atual() !== null) throw new Error(...)
        # Se depois de montar a árvore ainda sobrou token,
        # a expressão tem algum erro (ex: "A B" sem operador entre eles)

        return arvore




# ─────────────────────────────────────────────────────────────
# PARTE 4 — EXTRAIR PROPOSIÇÕES
# Objetivo: da lista de tokens, pegar só as letras (A, B, C...)
# ─────────────────────────────────────────────────────────────

def extrair_proposicoes(tokens: list) -> list:
    # TS equivalente:
    # function extrairProposicoes(tokens: string[]): string[] { ... }

    return sorted(set(t for t in tokens if re.match(r'[A-Z]', t)))
    # Vamos por partes:

    # "t for t in tokens"
    # TS: tokens.filter(...) — percorre cada token

    # "if re.match(r'[A-Z]', t)"
    # TS: .filter(t => /[A-Z]/.test(t))
    # Filtra só os tokens que são letras maiúsculas

    # "set(...)"
    # TS: new Set([...])
    # Remove duplicatas — se A aparece 3x na expressão, fica só 1

    # "sorted(...)"
    # TS: [...new Set(...)].sort()
    # Ordena alfabeticamente: ['A', 'B', 'C']




# ─────────────────────────────────────────────────────────────
# PARTE 5 — IMPRIMIR TABELA
# Objetivo: montar e exibir a tabela no terminal
# ─────────────────────────────────────────────────────────────

def imprimir_tabela(expressao: str, arvore: No, proposicoes: list):
    # TS: function imprimirTabela(expressao: string, arvore: No, proposicoes: string[]): void

    col = 6
    # Largura de cada coluna (em espaços) para alinhar o texto

    cabecalho = "".join(p.ljust(col) for p in proposicoes) + "| " + expressao
    # TS equivalente:
    # const cabecalho = proposicoes.map(p => p.padEnd(col)).join('') + '| ' + expressao
    # .ljust(col) em Python == .padEnd(col) em TS
    # Coloca cada proposição com espaços à direita pra alinhar

    separador = "-" * len(cabecalho)
    # TS: const separador = '-'.repeat(cabecalho.length)
    # Linha de traços do tamanho exato do cabeçalho

    print()
    print(cabecalho)
    print(separador)
    # TS: console.log() / console.log(cabecalho) / console.log(separador)

    for combo in product([True, False], repeat=len(proposicoes)):
        # TS equivalente (manual):
        # for (const combo of gerarCombinacoes(proposicoes.length)) { ... }
        #
        # product([True,False], repeat=3) gera:
        # (T,T,T), (T,T,F), (T,F,T), (T,F,F), (F,T,T)...
        # São todas as combinações possíveis de V e F
        # repeat=len(proposicoes) → se tem 3 proposições, repeat=3

        valores = dict(zip(proposicoes, combo))
        # TS equivalente:
        # const valores: Record<string, boolean> = {}
        # proposicoes.forEach((p, i) => valores[p] = combo[i])
        #
        # zip() "costura" as duas listas:
        # ['A','B','C'] + (True,False,True) → {'A':True, 'B':False, 'C':True}
        # dict() transforma os pares em dicionário

        resultado = arvore.avaliar(valores)
        # TS: const resultado = arvore.avaliar(valores)
        # Avalia a expressão inteira com os valores desta linha

        linha = "".join(("V" if v else "F").ljust(col) for v in combo)
        # TS: const linha = combo.map(v => (v ? 'V' : 'F').padEnd(col)).join('')
        # Transforma True→'V' e False→'F', com espaços pra alinhar

        linha += "| " + ("V" if resultado else "F")
        # TS: linha += '| ' + (resultado ? 'V' : 'F')
        # Adiciona o resultado final da expressão no fim da linha

        print(linha)
        # TS: console.log(linha)
        # Imprime a linha — UMA POR VEZ (não carrega tudo na memória)

    print()
    # Linha em branco no final pra ficar organizado




# ─────────────────────────────────────────────────────────────
# PARTE 6 — MAIN (ponto de entrada do programa)
# ─────────────────────────────────────────────────────────────

def main():
    # TS: function main(): void
    # É o equivalente do seu index.ts ou app.ts — onde tudo começa

    print("=" * 50)
    print("  TABELA VERDADE — Parser Recursivo")
    print("  Operadores: ^ v -> <-> ! ~")
    print("  Proposicoes: letras maiusculas (A-Z)")
    print("=" * 50)
    # TS: console.log("=".repeat(50)) etc.

    while True:
        # TS: while (true) { ... }
        # Loop infinito — só sai quando o usuário digitar 'sair'

        try:
            # TS: try { ... } catch(e) { ... }
            # Captura qualquer erro sem travar o programa

            expressao = input("\nExpressao (ou 'sair'): ").strip()
            # TS: não tem input() nativo — em Node você usaria readline
            # .strip() em Python == .trim() em TS
            # Remove espaços do começo e fim do que o usuário digitou

            if expressao.lower() == 'sair':
                # TS: if (expressao.toLowerCase() === 'sair')
                print("Encerrando.")
                break
                # TS: break — sai do while

            if not expressao:
                continue
                # TS: if (!expressao) continue
                # Se o usuário só apertou Enter sem digitar nada,
                # volta pro início do loop

            tokens = split(expressao)
            # Quebra a expressão em tokens

            proposicoes = extrair_proposicoes(tokens)
            # Extrai as proposições únicas e ordenadas

            if not proposicoes:
                print("Nenhuma proposicao encontrada.")
                continue

            parser = Parser(tokens)
            # TS: const parser = new Parser(tokens)
            # Cria o parser com os tokens

            arvore = parser.parse()
            # TS: const arvore = parser.parse()
            # Monta a árvore de Nós a partir dos tokens

            print(f"\nProposicoes: {', '.join(proposicoes)}")
            print(f"Combinacoes: {2 ** len(proposicoes)}")
            # TS: console.log(`Proposicoes: ${proposicoes.join(', ')}`)
            # f"..." em Python == template literal `...` em TS

            imprimir_tabela(expressao, arvore, proposicoes)
            # Desenha a tabela no terminal

        except ValueError as e:
            print(f"\n[ERRO] {e}")
            # TS: catch(e) { console.log(`[ERRO] ${e.message}`) }
            # Erros de expressão inválida — mostra e continua o loop

        except Exception as e:
            print(f"\n[ERRO INESPERADO] {e}")
            # Qualquer outro erro inesperado — mostra e continua


if __name__ == "__main__":
    main()
# TS equivalente: main()
# Em Python, "__name__ == '__main__'" significa:
# "só executa o main() se este arquivo for rodado diretamente"
# (não executa se for importado por outro arquivo)
# Em TS/Node seria como checar if (require.main === module)