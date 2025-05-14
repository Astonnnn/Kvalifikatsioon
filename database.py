import sqlite3

def loo_andmebaas():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor() #aitab andmebaasist asju võtta

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veebileht TEXT NOT NULL,
            ajalimiit INTEGER NOT NULL,
            staatus BOOLEAN DEFAULT FALSE,
            jaanud_aega FLOAT NOT NULL
        );
    ''')

    connection.commit()
    connection.close()

def muuda_staatust(url):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE websites SET staatus = not(staatus) WHERE url = ??', (url))

    connection.commit()
    connection.close()

def lisa_veebileht(veebileht, ajalimiit):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO websites (veebileht, ajalimiit, staatus, jaanud_aega) VALUES (?, ?, ?, ?)', (veebileht, ajalimiit, False, ajalimiit))

    connection.commit() #salvestab muutused andmebaasi
    connection.close() #sulgeb ühenduse, et see jooksma ei jääks


#andmete kogumine
def kuva_veebilehed():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM websites') #Käivitab sql käsklusi ning muudab andmebaasi
    andmed = cursor.fetchall()


    connection.close()
    return andmed



