from dataclasses import dataclass
import random
import sqlite3
import numpy as np

@dataclass
class WordEntity:
    id: int  # primary key
    en: str
    ru: str
    compares: int = 0
    success: int = 0
    meaning: str = None
    weight: float = 0.0

@dataclass
class SettingEntity:
    name: str  # primary key
    value: str

class Storager:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')  # In-memory SQLite database
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                en TEXT NOT NULL,
                ru TEXT NOT NULL,
                compares INTEGER DEFAULT 0,
                success INTEGER DEFAULT 0,
                meaning TEXT,
                weight REAL DEFAULT 0.0
            )
        ''')
        self.cursor.execute('CREATE INDEX idx_en ON words (en)')
        self.cursor.execute('CREATE INDEX idx_ru ON words (ru)')
        self.conn.commit()

    def calculate_weight(self, success: int, compares: int) -> float:
        success_rate = success / compares if compares > 0 else 0
        weight = 1 / (success_rate + 1) * (1 / (compares + 1))
        return weight

    def store(self, en: str, ru: str, meaning: str = None) -> None:
        '''
        Stores new en-ru word pair in the database. Meaning is optional.
        '''
        weight = self.calculate_weight(0, 0)  # Initial weight
        self.cursor.execute('''
            INSERT INTO words (en, ru, compares, success, meaning, weight)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (en.lower(), ru.lower(), 0, 0, meaning, weight))
        self.conn.commit()

    def get(self, word: str) -> WordEntity:
        self.cursor.execute('''
            SELECT * FROM words WHERE en = ? OR ru = ?
        ''', (word.lower(), word.lower()))
        row = self.cursor.fetchone()
        if row:
            return WordEntity(*row)
        return None

    def delete(self, word: str) -> None:
        '''
        Deletes a word pair from the database by either the English or Russian word.
        '''
        self.cursor.execute('''
            DELETE FROM words WHERE en = ? OR ru = ?
        ''', (word.lower(), word.lower()))
        self.conn.commit()

    def update(self, updates: list) -> None:
        '''
        Updates a batch of word pairs. Each update is a tuple (id, success_status).
        Adds one to the compares field for all updates and adds one to the success field if success_status is True.
        '''
        for update in updates:
            id, success_status = update
            self.cursor.execute('''
                SELECT compares, success FROM words WHERE id = ?
            ''', (id,))
            row = self.cursor.fetchone()
            if row:
                compares, success = row
                compares += 1
                success += 1 if success_status else 0
                weight = self.calculate_weight(success, compares)
                self.cursor.execute('''
                    UPDATE words
                    SET compares = ?, success = ?, weight = ?
                    WHERE id = ?
                ''', (compares, success, weight, id))
        self.conn.commit()

    def random(self, size: int) -> list[WordEntity]:
        self.cursor.execute('''
            SELECT id, weight FROM words
        ''')
        rows = self.cursor.fetchall()
        if not rows:
            return []

        weights = [row[1] for row in rows]  # Fetch precomputed weights
        total_weight = sum(weights)
        probabilities = [weight / total_weight for weight in weights]

        selected_indices = set()
        selected_entities = []

        while len(selected_entities) < size and len(selected_indices) < len(rows):
            selected_index = np.random.choice(len(rows), p=probabilities)
            if selected_index not in selected_indices:
                selected_indices.add(selected_index)
                selected_id = rows[selected_index][0]
                self.cursor.execute('SELECT * FROM words WHERE id = ?', (selected_id,))
                row = self.cursor.fetchone()
                selected_entities.append(WordEntity(*row))

        return selected_entities

if __name__ == '__main__':
    import numpy as np  # Import numpy for weighted random selection

    S = Storager()

    # Add test data
    test_data = [
        ('word', 'слово', 'meaning1'),
        ('sentence', 'предложение', 'meaning2'),
        ('language', 'язык', 'meaning3'),
        ('book', 'книга', 'meaning4'),
        ('tree', 'дерево', 'meaning5')
    ]
    for en, ru, meaning in test_data:
        S.store(en, ru, meaning)

    # Print all entries before modifications
    print("Entries before modifications:")
    S.cursor.execute('SELECT * FROM words')
    for row in S.cursor.fetchall():
        print(WordEntity(*row))

    # Get a random batch
    batch_size = 3
    random_batch = S.random(batch_size)
    print("\nRandom batch:")
    for entity in random_batch:
        print(entity)

    # Example of update
    updates = [(1, True), (2, False)]
    S.update(updates)

    # Example of delete
    word_to_delete = 'tree'
    S.delete(word_to_delete)

    # Print all entries after modifications
    print("\nEntries after modifications:")
    S.cursor.execute('SELECT * FROM words')
    for row in S.cursor.fetchall():
        print(WordEntity(*row))