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
        self.aulas_faltadas += 1
        self.verificar_situacao()

    def verificar_situacao(self):
        percentual_faltas = (self.aulas_faltadas / self.total_aulas) * 100
        if percentual_faltas > 25:
            print(f"Alerta! Você ultrapassou o limite de faltas na disciplina {self.nome}. Percentual de faltas: {percentual_faltas:.2f}%")
        else:
            faltas_restantes = (self.total_aulas * 0.25) - self.aulas_faltadas
            print(f"Você pode faltar mais {faltas_restantes:.0f} aulas na disciplina {self.nome} sem ser reprovado por falta.")

    def mostrar_faltas(self):
        return self.aulas_faltadas


class ListaAulas:
    def __init__(self):
        self.head = None 

    def adicionar_aula(self, nome, carga_horaria, aulas_semana):
        nova_aula = Aula(nome, carga_horaria, aulas_semana)
        nova_aula.next = self.head  
        self.head = nova_aula  

    def mostrar_aulas(self):
        aula_atual = self.head  
        while aula_atual is not None:  
            print(f'Nome da aula: {aula_atual.nome}, Faltas: {aula_atual.mostrar_faltas()}')
            aula_atual = aula_atual.next 



lista_de_aulas = ListaAulas()

while True:
    print("\n1. Adicionar Aula")
    print("2. Mostrar Aulas")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        nome = input("Nome da aula: ")
        carga_horaria = int(input("Carga horária: "))
        aulas_semana = int(input("Aulas por semana: "))
        lista_de_aulas.adicionar_aula(nome, carga_horaria, aulas_semana)
    elif opcao == "2":
        lista_de_aulas.mostrar_aulas()
    elif opcao == "3":
        break
    else:
        print("Opção inválida. Escolha novamente.")
