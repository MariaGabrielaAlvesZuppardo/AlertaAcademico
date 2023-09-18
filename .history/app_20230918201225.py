# Importa o framework Flask e o módulo 'merge' (presumivelmente um arquivo local).
from flask import Flask, render_template, request, redirect, url_for
from merge import *

# Inicializa o aplicativo Flask.
app = Flask(__name__)

# Classe Aula
class Aula:
    # Inicializa uma instância da classe Aula com atributos e valores padrão.
    def __init__(self, nome, carga_horaria, aulas_semana, semanas=None, total_aulas=None, aulas_faltadas=0, percentual_faltas=0):
        # Define os atributos da aula.
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.aulas_semana = aulas_semana
        self.semanas = semanas if semanas is not None else carga_horaria // aulas_semana
        self.total_aulas = total_aulas if total_aulas is not None else self.semanas * aulas_semana
        self.aulas_faltadas = aulas_faltadas
        self.percentual_faltas = percentual_faltas
        self.next = None  # Referência ao próximo objeto da lista ligada.

    # Método para registrar uma falta na aula e verificar a situação de faltas.
    def adicionar_falta(self):
        self.aulas_faltadas += 1
        self.verificar_situacao()

    # Método para verificar a situação de faltas e exibir alertas, se necessário.
    def verificar_situacao(self):
        percentual_faltas = (self.aulas_faltadas / self.total_aulas) * 100
        if percentual_faltas > 25:
            print(f"Alerta! Você ultrapassou o limite de faltas na disciplina {self.nome}. Percentual de faltas: {percentual_faltas:.2f}%")
        else:
            faltas_restantes = (self.total_aulas * 0.25) - self.aulas_faltadas
            print(f"Você pode faltar mais {faltas_restantes:.0f} aulas na disciplina {self.nome} sem ser reprovado por falta.")

    # Método para retornar o número de aulas faltadas.
    def mostrar_faltas(self):
        return self.aulas_faltadas

# Classe ListaAulas
class ListaAulas:
    # Inicializa a lista de aulas como vazia.
    def __init__(self):
        self.head = None  # Cabeça da lista ligada de aulas.

    # Método para adicionar uma nova aula à lista.
    def adicionar_aula(self, nome, carga_horaria, aulas_semana):
        nova_aula = Aula(nome, carga_horaria, aulas_semana)
        nova_aula.next = self.head
        self.head = nova_aula

    # Método para retornar uma lista de aulas.
    def mostrar_aulas(self):
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append(aula_atual)
            aula_atual = aula_atual.next
        return aulas

    # Método para ordenar as aulas por nome e retornar a lista ordenada.
    def ordenar_por_nome(self):
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append(aula_atual)
            aula_atual = aula_atual.next
        aulas.sort(key=lambda aula: aula.nome)
        return aulas

    # Método para buscar uma aula pelo nome e retornar a primeira correspondência encontrada.
    def buscar_aula_por_nome(self, nome):
        aula_atual = self.head
        while aula_atual is not None:
            if aula_atual.nome == nome:
                return aula_atual
            aula_atual = aula_atual.next
        return None

# Classe Fila
class Fila:
    # Inicializa a fila como uma lista vazia.
    def __init__(self):
        self.items = []

    # Método para adicionar um item ao final da fila.
    def enfileirar(self, item):
        self.items.append(item)

    # Método para remover e retornar o item do início da fila.
    def desenfileirar(self):
        if not self.esta_vazia():
            return self.items.pop(0)
        else:
            return None

    # Método para verificar se a fila está vazia.
    def esta_vazia(self):
        return len(self.items) == 0

# Classe Pilha
class Pilha:
    # Inicializa a pilha como uma lista vazia.
    def __init__(self):
        self.items = []

    # Método para adicionar um item ao topo da pilha.
    def empilhar(self, item):
        self.items.append(item)

    # Método para remover e retornar o item do topo da pilha.
    def desempilhar(self):
        if not self.esta_vazia():
            return self.items.pop()
        else:
            return None

    # Método para verificar se a pilha está vazia.
    def esta_vazia(self):
        return len(self.items) == 0

# Criação da pilha para registro de ações, lista de aulas e fila de notificações.
pilha_de_acoes = Pilha()
lista_de_aulas = ListaAulas()
fila_de_notificacoes = Fila()

# Função para registrar uma falta e empilhar a ação.
def registrarFalta(pilha_de_acoes, acao):
    pilha_de_acoes.empilhar(acao)

# Função para desfazer a última ação registrada e retornar a ação desfeita.
def desfazerRegistro(pilha_de_acoes):
    return pilha_de_acoes.desempilhar()

# Função para adicionar uma notificação à fila.
def adicionarNotificacao(fila_de_notificacoes, notificacao):
    fila_de_notificacoes.enfileirar(notificacao)

# Função para remover a primeira notificação da fila.
def removerNotificacao(fila_de_notificacoes):
    fila_de_notificacoes.desenfileirar()

# Função para gerar notificações com base no percentual de faltas nas disciplinas.
def gerarNotificacoes(fila_de_notificacoes, lista_de_aulas):
    for aula in lista_de_aulas.mostrar_aulas():
        percentual_faltas = (aula.aulas_faltadas / aula.total_aulas) * 100
        if percentual_faltas >= 20 and percentual_faltas < 25:
            mensagem = f"Atenção! Você está perto do limite de faltas em {aula.nome}. Percentual de faltas: {percentual_faltas:.2f}%"
            fila_de_notificacoes.enfileirar(mensagem)
        elif percentual_faltas >= 25:
            mensagem = f"Alerta! Você ultrapassou o limite de faltas em {aula.nome}. Percentual de faltas: {percentual_faltas:.2f}%"
            fila_de_notificacoes.enfileirar(mensagem)

# Classe MergeSort para ordenação
class MergeSort:
    # Método estático para ordenar a lista de aulas com base no atributo fornecido usando o algoritmo Merge Sort.
    @staticmethod
    def merge_sort(aulas, attr):
        if len(aulas) > 1:
            mid = len(aulas) // 2
            left_half = aulas[:mid]
            right_half = aulas[mid:]

            MergeSort.merge_sort(left_half, attr)
            MergeSort.merge_sort(right_half, attr)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if getattr(left_half[i], attr) < getattr(right_half[j], attr):
                    aulas[k] = left_half[i]
                    i += 1
                else:
                    aulas[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                aulas[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                aulas[k] = right_half[j]
                j += 1
                k += 1

        return aulas

    # Métodos estáticos para ordenar aulas por diferentes atributos.
    @staticmethod
    def ordenar_por_nome(aulas):
        return MergeSort.merge_sort(aulas, 'nome')

    @staticmethod
    def ordenar_por_carga_horaria(aulas):
        return MergeSort.merge_sort(aulas, 'carga_horaria')

    @staticmethod
    def ordenar_por_percentual_faltas(aulas):
        return MergeSort.merge_sort(aulas, 'percentual_faltas')

# Classe Busca para buscar aulas
class Busca:
    # Método estático para buscar aulas pelo nome.
    @staticmethod
    def buscar_aulas_por_nome(lista_de_aulas, nome):
        return [aula for aula in lista_de_aulas.mostrar_aulas() if aula.nome == nome]

    # Método estático para buscar aulas pela carga horária.
    @staticmethod
    def buscar_aulas_por_carga_horaria(lista_de_aulas, carga_horaria):
        return [aula for aula in lista_de_aulas.mostrar_aulas() if aula.carga_horaria == carga_horaria]

    # Método estático para buscar aulas com percentual de faltas acima de um valor especificado.
    @staticmethod
    def buscar_aulas_com_faltas_acima_de(lista_de_aulas, percentual):
        return [aula for aula in lista_de_aulas.mostrar_aulas() if (aula.aulas_faltadas / aula.total_aulas) * 100 > percentual]

# Rota principal para exibir a página inicial.
@app.route('/')
def index():
    return render_template('index.html', aulas=lista_de_aulas.mostrar_aulas(), notificacoes=fila_de_notificacoes.items)

# Rota para adicionar uma nova aula.
@app.route('/adicionar_aula', methods=['POST'])
def adicionar_aula():
    nome = request.form['nome']
    carga_horaria = int(request.form['carga_horaria'])
    aulas_semana = int(request.form['aulas_semana'])
    lista_de_aulas.adicionar_aula(nome, carga_horaria, aulas_semana)
    return redirect(url_for('index'))

# Rota para registrar uma falta em uma aula.
@app.route('/registrar_falta', methods=['POST'])
def registrar_falta():
    aula_escolhida = request.form['aula_escolhida']
    registrarFalta(pilha_de_acoes, f"Registro de falta em {aula_escolhida}")
    aula_encontrada = lista_de_aulas.buscar_aula_por_nome(aula_escolhida)
    if aula_encontrada:
        aula_encontrada.adicionar_falta()
    return redirect(url_for('index'))

# Rota para desfazer a última ação registrada.
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

# Rota para adicionar uma notificação à fila.
@app.route('/adicionar_notificacao', methods=['POST'])
def adicionar_notificacao():
    notificacao = request.form['notificacao']
    adicionarNotificacao(fila_de_notificacoes, notificacao)
    return redirect(url_for('index'))

# Rota para remover a primeira notificação da fila.
@app.route('/remover_notificacao', methods=['POST'])
def remover_notificacao():
    removerNotificacao(fila_de_notificacoes)
    return redirect(url_for('index'))

# Rota para gerar notificações com base no percentual de faltas nas disciplinas.
@app.route('/gerar_notificacoes', methods=['POST'])
def gerar_notificacoes():
    gerarNotificacoes(fila_de_notificacoes, lista_de_aulas)
    return redirect(url_for('index'))

# Rota para buscar aulas por nome.
@app.route('/buscar_aulas_por_nome', methods=['POST'])
def buscar_aulas_por_nome():
    nome = request.form['nome']
    aulas_encontradas = Busca.buscar_aulas_por_nome(lista_de_aulas, nome)
    return render_template('index.html', aulas=aulas_encontradas, notificacoes=fila_de_notificacoes.items)

# Rota para buscar aulas por carga horária.
@app.route('/buscar_aulas_por_carga_horaria', methods=['POST'])
def buscar_aulas_por_carga_horaria():
    carga_horaria = int(request.form['carga_horaria'])
    aulas_encontradas = Busca.buscar_aulas_por_carga_horaria(lista_de_aulas, carga_horaria)
    return render_template('index.html', aulas=aulas_encontradas, notificacoes=fila_de_notificacoes.items)

# Rota para buscar aulas com percentual de faltas acima de um valor.
@app.route('/buscar_aulas_com_faltas_acima_de', methods=['POST'])
def buscar_aulas_com_faltas_acima_de():
    percentual = float(request.form['percentual'])
    aulas_encontradas = Busca.buscar_aulas_com_faltas_acima_de(lista_de_aulas, percentual)
    return render_template('index.html', aulas=aulas_encontradas, notificacoes=fila_de_notificacoes.items)

# Rota para ordenar aulas por nome.
@app.route('/ordenar_aulas_por_nome', methods=['GET'])
def ordenar_aulas_por_nome():
    aulas_ordenadas = MergeSort.ordenar_por_nome(lista_de_aulas.mostrar_aulas())
    return render_template('index.html', aulas=aulas_ordenadas, notificacoes=fila_de_notificacoes.items)

# Rota para ordenar aulas por carga horária.
@app.route('/ordenar_aulas_por_carga_horaria', methods=['GET'])
def ordenar_aulas_por_carga_horaria():
    aulas_ordenadas = MergeSort.ordenar_por_carga_horaria(lista_de_aulas.mostrar_aulas())
    return render_template('index.html', aulas=aulas_ordenadas, notificacoes=fila_de_notificacoes.items)

# Rota para ordenar aulas por percentual de faltas.
@app.route('/ordenar_aulas_por_percentual_faltas', methods=['GET'])
def ordenar_aulas_por_percentual_faltas():
    aulas_ordenadas = MergeSort.ordenar_por_percentual_faltas(lista_de_aulas.mostrar_aulas())
    return render_template('index.html', aulas=aulas_ordenadas, notificacoes=fila_de_notificacoes.items)

# Inicia o aplicativo Flask.
if __name__ == '__main__':
    app.run(debug=True)
