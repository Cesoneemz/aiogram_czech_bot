import psycopg2


class LLHelperDatabase:

    def __init__(self):
        self.connection = psycopg2.connect(dbname='users', host='localhost', user='postgres')
        self.cursor = self.connection.cursor()

    def get_subscribed(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            result = self.cursor.fetchone()
            return result

    def get_word(self, word):
        with self.connection:
            self.cursor.execute('SELECT * FROM words WHERE word = %s', (word,))
            result = self.cursor.fetchone()
            return result

    def get_words_count(self):
        with self.connection:
            self.cursor.execute('SELECT COUNT(*) FROM words')
            (result,) = self.cursor.fetchone()
            return result

    def add_user_to_database(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (user_id) VALUES (%s)', (user_id,))

    def add_new_word(self, category, word, translate, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO words (category, word, translate, user_id) VALUES (%s, %s, %s, %s)',
                                       (category, word, translate, user_id))
