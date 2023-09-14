from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Classe Aula
class Aula:
    def __init__(self, nome, carga_horaria, aulas_semana, semanas=None, total_aulas=None, aulas_faltadas=0, percentual_faltas=0):
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.aulas_semana = aulas_semana
        self.semanas = semanas if semanas is not None else carga_horaria // aulas_semana
        self.total_aulas = total_aulas if total_aulas is not None else self.semanas * aulas_semana
        self.aulas_faltadas = aulas_faltadas
        self.percentual_faltas = percentual_faltas
        self.next = None

    def adicionar_falta(self):
        """Registra uma falta na aula e verifica a situação de faltas."""
        self.aulas_faltadas += 1
        self.verificar_situacao()

    def verificar_situacao(self):
        """Verifica a situação de faltas e exibe alertas se necessário."""
        percentual_faltas = (self.aulas_faltadas / self.total_aulas) * 100
        if percentual_faltas > 25:
            print(f"Alerta! Você ultrapassou o limite de faltas na disciplina {self.nome}. Percentual de faltas: {percentual_faltas:.2f}%")
        else:
            faltas_restantes = (self.total_aulas * 0.25) - self.aulas_faltadas
            print(f"Você pode faltar mais {faltas_restantes:.0f} aulas na disciplina {self.nome} sem ser reprovado por falta.")

    def mostrar_faltas(self):
        """Retorna o número de aulas faltadas."""
        return self.aulas_faltadas

# Classe ListaAulas
class ListaAulas:
    def __init__(self):
        """Inicializa a lista de aulas como vazia."""
        self.head = None

    def adicionar_aula(self, nome, carga_horaria, aulas_semana):
        """Adiciona uma nova aula à lista."""
        nova_aula = Aula(nome, carga_horaria, aulas_semana)
        nova_aula.next = self.head
        self.head = nova_aula

    def mostrar_aulas(self):
        """Retorna uma lista de aulas."""
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append(aula_atual)
            aula_atual = aula_atual.next
        return aulas

    def ordenar_por_nome(self):
        """Ordena as aulas por nome e retorna a lista ordenada."""
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append(aula_atual)
            aula_atual = aula_atual.next
        aulas.sort(key=lambda aula: aula.nome)
        return aulas

    def buscar_aula_por_nome(self, nome):
        """Busca uma aula pelo nome e retorna a primeira correspondência encontrada."""
        aula_atual = self.head
        while aula_atual is not None:
            if aula_atual.nome == nome:
                return aula_atual
            aula_atual = aula_atual.next
        return None

# Classe Fila
class Fila:
    def __init__(self):
        """Inicializa a fila como uma lista vazia."""
        self.items = []

    def enfileirar(self, item):
        """Adiciona um item ao final da fila."""
        self.items.append(item)

    def desenfileirar(self):
        """Remove e retorna o item do início da fila."""
        if not self.esta_vazia():
            return self.items.pop(0)
        else:
            return None

    def esta_vazia(self):
        """Verifica se a fila está vazia."""
        return len(self.items) == 0

# Classe Pilha
class Pilha:
    def __init__(self):
        """Inicializa a pilha como uma lista vazia."""
        self.items = []

    def empilhar(self, item):
        """Adiciona um item ao topo da pilha."""
        self.items.append(item)

    def desempilhar(self):
        """Remove e retorna o item do topo da pilha."""
        if not self.esta_vazia():
            return self.items.pop()
        else:
            return None

    def esta_vazia(self):
        """Verifica se a pilha está vazia."""
        return len(self.items) == 0

# Criação da pilha para registro de ações, lista de aulas e fila de notificações.
pilha_de_acoes = Pilha()
lista_de_aulas = ListaAulas()
fila_de_notificacoes = Fila()

def registrarFalta(pilha_de_acoes, acao):
    """Registra uma falta e empilha a ação."""
    pilha_de_acoes.empilhar(acao)

def desfazerRegistro(pilha_de_acoes):
    """Desfaz a última ação registrada e retorna a ação desfeita."""
    return pilha_de_acoes.desempilhar()


def adicionarNotificacao(fila_de_notificacoes, notificacao):
    """Adiciona uma notificação à fila."""
    fila_de_notificacoes.enfileirar(notificacao)

def removerNotificacao(fila_de_notificacoes):
    """Remove a primeira notificação da fila."""
    fila_de_notificacoes.desenfileirar()

def gerarNotificacoes(fila_de_notificacoes, lista_de_aulas):
    """Gera notificações com base no percentual de faltas nas disciplinas."""
    for aula in lista_de_aulas.mostrar_aulas():
        percentual_faltas = (aula.aulas_faltadas / aula.total_aulas) * 100
        if percentual_faltas >= 20 and percentual_faltas < 25:
            mensagem = f"Atenção! Você está perto do limite de faltas em {aula.nome}. Percentual de faltas: {percentual_faltas:.2f}%"
            fila_de_notificacoes.enfileirar(mensagem)
        elif percentual_faltas >= 25:
            mensagem = f"Alerta! Você ultrapassou o limite de faltas em {aula.nome}. Percentual de faltas: {percentual_faltas:.2f}%"
            fila_de_notificacoes.enfileirar(mensagem)



@app.route('/')
def index():
    return render_template('index.html', aulas=lista_de_aulas.mostrar_aulas(), notificacoes=fila_de_notificacoes.items)

@app.route('/adicionar_aula', methods=['POST'])
def adicionar_aula():
    nome = request.form['nome']
    carga_horaria = int(request.form['carga_horaria'])
    aulas_semana = int(request.form['aulas_semana'])
    lista_de_aulas.adicionar_aula(nome, carga_horaria, aulas_semana)
    return redirect(url_for('index'))

@app.route('/registrar_falta', methods=['POST'])
def registrar_falta():
    aula_escolhida = request.form['aula_escolhida']
    registrarFalta(pilha_de_acoes, f"Registro de falta em {aula_escolhida}")
    aula_encontrada = lista_de_aulas.buscar_aula_por_nome(aula_escolhida)
    if aula_encontrada:
        aula_encontrada.adicionar_falta()
    return redirect(url_for('index'))

@app.route('/desfazer_registro', methods=['POST'])
def desfazer_registro():
    acao_desfeita = desfazerRegistro(pilha_de_acoes)
    if acao_desfeita:
        if "Registro de falta em" in acao_desfeita:
            aula_escolhida = acao_desfeita.split("em")[1].strip()
            aula_encontrada = lista_de_aulas.buscar_aula_por_nome(aula_escolhida)
            if aula_encontrada:
                aula_encontrada.aulas_faltadas -= 1  # Remove a falta
        return f'Ação desfeita: {acao_desfeita}'
    else:
        return 'Não há ações para desfazer.'

@app.route('/adicionar_notificacao', methods=['POST'])
def adicionar_notificacao():
    notificacao = request.form['notificacao']
    adicionarNotificacao(fila_de_notificacoes, notificacao)
    return redirect(url_for('index'))

@app.route('/remover_notificacao', methods=['POST'])
def remover_notificacao():
    removerNotificacao(fila_de_notificacoes)
    return redirect(url_for('index'))

@app.route('/gerar_notificacoes', methods=['POST'])
def gerar_notificacoes():
    gerarNotificacoes(fila_de_notificacoes, lista_de_aulas)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)