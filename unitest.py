import unittest
from io import StringIO
import sys

# Reimplementação das classes fornecidas para facilitar os testes

class Fila:
    def __init__(self):
        self.items = []

    def enfileirar(self, item):
        self.items.append(item)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.items.pop(0)
        else:
            return None

    def esta_vazia(self):
        return len(self.items) == 0

    def tamanho(self):
        return len(self.items)


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
            return f"Alerta! Você ultrapassou o limite de faltas na disciplina {self.nome}. Percentual de faltas: {percentual_faltas:.2f}%"
        else:
            faltas_restantes = (self.total_aulas * 0.25) - self.aulas_faltadas
            return f"Você pode faltar mais {faltas_restantes:.0f} aulas na disciplina {self.nome} sem ser reprovado por falta."

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
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append((aula_atual.nome, aula_atual.mostrar_faltas()))
            aula_atual = aula_atual.next
        return aulas

    def ordenar_por_nome(self):
        aulas = []
        aula_atual = self.head
        while aula_atual is not None:
            aulas.append(aula_atual)
            aula_atual = aula_atual.next
        return sorted(aulas, key=lambda aula: aula.nome)

    def buscar_aula_por_nome(self, nome):
        aula_atual = self.head
        while aula_atual is not None:
            if aula_atual.nome == nome:
                return aula_atual
            aula_atual = aula_atual.next
        return None


class Pilha:
    def __init__(self):
        self.items = []

    def empilhar(self, item):
        self.items.append(item)

    def desempilhar(self):
        if not self.esta_vazia():
            return self.items.pop()
        else:
            return None

    def esta_vazia(self):
        return len(self.items) == 0


# Testes unitários

class TestFila(unittest.TestCase):
    def test_enfileirar(self):
        fila = Fila()
        fila.enfileirar(1)
        self.assertEqual(fila.items, [1])

    def test_desenfileirar(self):
        fila = Fila()
        fila.enfileirar(1)
        fila.enfileirar(2)
        item = fila.desenfileirar()
        self.assertEqual(item, 1)
        self.assertEqual(fila.items, [2])

    def test_esta_vazia(self):
        fila = Fila()
        self.assertTrue(fila.esta_vazia())
        fila.enfileirar(1)
        self.assertFalse(fila.esta_vazia())

    def test_tamanho(self):
        fila = Fila()
        self.assertEqual(fila.tamanho(), 0)
        fila.enfileirar(1)
        fila.enfileirar(2)
        self.assertEqual(fila.tamanho(), 2)


class TestAula(unittest.TestCase):
    def test_adicionar_falta(self):
        aula = Aula("Matemática", 20, 5)
        aula.adicionar_falta()
        self.assertEqual(aula.aulas_faltadas, 1)

    def test_verificar_situacao(self):
        aula = Aula("Matemática", 20, 5)
        self.assertEqual(aula.verificar_situacao(), "Você pode faltar mais 5 aulas na disciplina Matemática sem ser reprovado por falta.")
        for _ in range(6):
            aula.adicionar_falta()
        self.assertEqual(aula.verificar_situacao(), "Alerta! Você ultrapassou o limite de faltas na disciplina Matemática. Percentual de faltas: 30.00%")

    def test_mostrar_faltas(self):
        aula = Aula("Matemática", 20, 5)
        self.assertEqual(aula.mostrar_faltas(), 0)
        aula.adicionar_falta()
        self.assertEqual(aula.mostrar_faltas(), 1)

class TestListaAulas(unittest.TestCase):
    def test_adicionar_aula(self):
        lista = ListaAulas()
        lista.adicionar_aula("Matemática", 20, 5)
        self.assertEqual(lista.head.nome, "Matemática")

    def test_mostrar_aulas(self):
        lista = ListaAulas()
        lista.adicionar_aula("Matemática", 20, 5)
        lista.adicionar_aula("Física", 15, 3)
        aulas = lista.mostrar_aulas()
        self.assertEqual(aulas, [("Física", 0), ("Matemática", 0)])

    def test_ordenar_por_nome(self):
        lista = ListaAulas()
        lista.adicionar_aula("Matemática", 20, 5)
        lista.adicionar_aula("Física", 15, 3)
        aulas_ordenadas = lista.ordenar_por_nome()
        self.assertEqual([aula.nome for aula in aulas_ordenadas], ["Física", "Matemática"])

    def test_buscar_aula_por_nome(self):
        lista = ListaAulas()
        lista.adicionar_aula("Matemática", 20, 5)
        lista.adicionar_aula("Física", 15, 3)
        aula = lista.buscar_aula_por_nome("Matemática")
        self.assertIsNotNone(aula)
        self.assertEqual(aula.nome, "Matemática")
        self.assertIsNone(lista.buscar_aula_por_nome("História"))

        
class TestPilha(unittest.TestCase):
    def test_empilhar(self):
        pilha = Pilha()
        pilha.empilhar(1)
        self.assertEqual(pilha.items, [1])

    def test_desempilhar(self):
        pilha = Pilha()
        pilha.empilhar(1)
        pilha.empilhar(2)
        item = pilha.desempilhar()
        self.assertEqual(item, 2)
        self.assertEqual(pilha.items, [1])

    def test_esta_vazia(self):
        pilha = Pilha()
        self.assertTrue(pilha.esta_vazia())
        pilha.empilhar(1)
        self.assertFalse(pilha.esta_vazia())


# Executar os testes
unittest_result = StringIO()
runner = unittest.TextTestRunner(stream=unittest_result)
unittest.main(verbosity=2, exit=False, testRunner=runner)

# Retorna os resultados
unittest_result.getvalue()


if __name__ == '__main__':
    unittest.main()