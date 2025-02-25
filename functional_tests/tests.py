from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	"""
    Functional tests simulating a new visitor's interactions with the web application using Selenium.
    """

	def setUp(self):
		"""
        Set up the test environment before each test case.

        This method initializes a new Firefox browser instance for Selenium tests.
        """
		self.browser = webdriver.Firefox()

	def tearDown(self):
		"""
        Clean up after each test case.

        This method quits the browser instance to ensure that no state carries over between tests.
        """
		self.browser.quit()

	# Auxiliary method 
	def wait_for_row_in_list_table(self, row_text):
		"""
        Wait for a specific row to appear in the list table.

        This helper method repeatedly checks the table with ID 'id_list_table'
        for a row that contains the provided text. If the row does not appear
        within MAX_WAIT seconds, the method raises an exception.

        Args:
            row_text (str): The text expected to be found in one of the table rows.

        Raises:
            AssertionError: If the row text is not found within the allowed time.
            WebDriverException: If there is an issue interacting with the browser.
        """
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)


	def test_can_start_a_list_for_one_user(self):
		"""
        Test that a user can start a new prioritized to-do list.

        The simulated user (Edith) performs the following actions:
          - Visits the homepage.
          - Checks that the page title and header contain "Priority-To-Do".
          - Enters a new to-do item ("Comprar anzol") into the input box.
          - Submits the item and verifies it appears in the list.
          - Adds a second item ("Comprar cola instantânea") and verifies both items appear.
          - Observes that the application assigns a unique URL to her list.
          - Finally, the browser is restarted to simulate a new user session.
        """
		# Edith ouviu falar de uma nova aplicação online interessante
		# para lista de tarefas. Ela decide verificar a homepage

		# Edith ouviu falar que agora a aplicação online de lista de tarefas
		# aceita definir prioridades nas tarefas do tipo baixa, média e alta
		# Ela decide verificar a homepage

		self.browser.get(self.live_server_url)

		# Ela percebe que o título da página e o cabeçalho mencionam
		# listas de tarefas (to-do)

		# Ela percebe que o título da página e o cabeçalho mencionam
		# listas de tarefas com prioridade (priority to-do)

		self.assertIn('Priority-To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Priority-To-Do', header_text)
		
		# Ela é convidada a inserir um item de tarefa imediatamente

		# Ela é convidada a inserir um item de tarefa e a prioridade da 
		# mesma imediatamente

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# Ela digita "Buy peacock feathers" (Comprar penas de pavão)
		# em uma nova caixa de texto (o hobby de Edith é fazer iscas
		# para pesca com fly)

		# Ela digita "Comprar anzol" em uma nova caixa de texto
		# e assinala prioridade alta no campo de seleção de prioridades

		inputbox.send_keys('Comprar anzol')

		# Quando ela tecla enter, a página é atualizada, e agora
		# a página lista "1 - Buy peacock feathers" como um item em 
		# uma lista de tarefas

		# Quando ela tecla enter, a página é atualizada, e agora
		# a página lista "1 - Comprar anzol - prioridade alta"
		# como um item em uma lista de tarefas

		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Comprar anzol')

		# Ainda continua havendo uma caixa de texto convidando-a a 
		# acrescentar outro item. Ela insere "Use peacock feathers 
		# to make a fly" (Usar penas de pavão para fazer um fly - 
		# Edith é bem metódica)

		# Ainda continua havendo uma caixa de texto convidando-a a 
		# acrescentar outro item. Ela insere "Comprar cola instantâne"
		# e assinala prioridade baixa pois ela ainda tem cola suficiente
		# por algum tempo
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys("Comprar cola instantânea")
		inputbox.send_keys(Keys.ENTER)

		# A página é atualizada novamente e agora mostra os dois
		# itens em sua lista

		# A página é atualizada novamente e agora mostra os dois
		# itens em sua lista e as respectivas prioridades

		self.wait_for_row_in_list_table('1: Comprar anzol')
		self.wait_for_row_in_list_table('2: Comprar cola instantânea')

		# Edith se pergunta se o site lembrará de sua lista. Então
		# ela nota que o site gerou um URL único para ela -- há um 
		# pequeno texto explicativo para isso.

		# Ela acessa essa URL -- sua lista de tarefas continua lá.

		# Satisfeita, ela volta a dormir

		# Edith se pergunta se o site lembrará de sua lista. Então
		# ela nota que o site gerou um URL único para ela -- há um 
		# pequeno texto explicativo para isso.
		# Ela acessa essa URL -- sua lista de tarefas continua lá.

		#Ela percebe que sua lista te um URL único
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#Agora um novo usuário, Francis, chega ao site

		## Usamos uma nova versão do nagegador para garantir que nenhuma 
		## informação de Edith está vindo de cookies, etc
		
		self.browser.quit()
		# Fim