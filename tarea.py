import requests
import threading

class OpenTriviaDatabase:
    def __init__(self):
        self.base_url = 'https://opentdb.com/api.php?amount=10&type=multiple'

    def get_trivia_questions(self, category=None):
        """
        Obtiene preguntas de trivia de la API de Open Trivia Database.
        :param category: Categoría de las preguntas (opcional).
        :return: Lista de preguntas de trivia.
        """
        url = self.base_url
        if category:
            url += f'&category={category}'

        response = requests.get(url)
        trivia = response.json()
        return trivia['results']

def search_trivia_questions(category=None):
    """
    Realiza una búsqueda de preguntas de trivia en la API de Open Trivia Database.
    :param category: Categoría de las preguntas (opcional).
    :return: Lista de preguntas de trivia encontradas.
    """
    trivia_db = OpenTriviaDatabase()
    questions = trivia_db.get_trivia_questions(category)
    return questions

def handle_user_query(user_id, category=None):
    """
    Maneja la consulta de un usuario específico.
    :param user_id: ID del usuario.
    :param category: Categoría de las preguntas de trivia (opcional).
    """
    questions = search_trivia_questions(category)
    # Realizar acciones con las preguntas encontradas, como mostrarlas al usuario o procesarlas de alguna manera
    print(f'Usuario {user_id}: Preguntas encontradas: {questions}')

# Crear una lista de usuarios y categorías de consulta
users = ['Usuario1', 'Usuario2', 'Usuario3']
categories = ['9', '18', '21']  # Categorías de las preguntas de trivia (9: General Knowledge, 18: Science, 21: Sports)

# Realizar consultas de los usuarios en hilos separados
threads = []
for i, user in enumerate(users):
    category = categories[i % len(categories)]  # Seleccionar una categoría para cada usuario
    thread = threading.Thread(target=handle_user_query, args=(user, category))
    thread.start()
    threads.append(thread)

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()
