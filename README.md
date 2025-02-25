# mlops_ufscar_esbd4_2
3. Unidade 2 - Desenvolvimento de Aplicação Utilizando TDD
3.1. Situação Problema da Unidade 2
Para a execução da atividade, abaixo é apresentada a proposta da história de usuário a ser implementada. Observa-se que ela é semelhante a que desenvolvemos durante a aula mas, suas diferenças implicarão na implementação de uma aplicação ligeiramente diferente.

 

Segue abaixo o esboço da classe de teste functional_test.py que irá guiar todo o processo de implementação da to-do list com prioridades.

 

############################## INICIO ####################################

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

import time

import unittest

 

class NewVsitorTest(unittest.TestCase):

 

def setUp(self):

self.browser = webdriver.Firefox()

 

def tearDown(self):

self.browser.quit()

 

# Edith ouviu falar que agora a aplicação online de lista de tarefas

# aceita definir prioridades nas tarefas do tipo baixa, média e alta

# Ela decide verificar a homepage

 

# Ela percebe que o título da página e o cabeçalho mencionam

# listas de tarefas com prioridade (priority to-do)

 

# Ela é convidada a inserir um item de tarefa e a prioridade da 

# mesma imediatamente

 

# Ela digita "Comprar anzol" em uma nova caixa de texto

# e assinala prioridade alta no campo de seleção de prioridades

 

# Quando ela tecla enter, a página é atualizada, e agora

# a página lista "1 - Comprar anzol - prioridade alta"

# como um item em uma lista de tarefas

 

# Ainda continua havendo uma caixa de texto convidando-a a 

# acrescentar outro item. Ela insere "Comprar cola instantâne"

# e assinala prioridade baixa pois ela ainda tem cola suficiente

# por algum tempo

 

# A página é atualizada novamente e agora mostra os dois

# itens em sua lista e as respectivas prioridades

 

# Edith se pergunta se o site lembrará de sua lista. Então

# ela nota que o site gerou um URL único para ela -- há um 

# pequeno texto explicativo para isso.

 

# Ela acessa essa URL -- sua lista de tarefas continua lá.

 

################################# FIM ####################################
