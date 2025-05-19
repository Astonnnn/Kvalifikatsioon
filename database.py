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

    cursor.execute('UPDATE websites SET staatus = not(staatus) WHERE veebileht = ?', (url,))

    connection.commit()
    connection.close()

def lisa_veebileht(veebileht, ajalimiit):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO websites (veebileht, ajalimiit, staatus, jaanud_aega) VALUES (?, ?, ?, ?)', (veebileht, ajalimiit, False, ajalimiit*60))

    connection.commit() #salvestab muutused andmebaasi
    connection.close() #sulgeb ühenduse, et see jooksma ei jääks


def muuda_aega(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT jaanud_aega FROM websites WHERE veebileht = ?', (veebileht,))
    result = cursor.fetchone()
    uus_aeg = result[0] - 5
    cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ? ', (uus_aeg, veebileht))
    connection.commit()
    connection.close()
    return uus_aeg

def taasta_aeg(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT ajalimiit from websites WHERE veebileht =?', (veebileht,))
    result = cursor.fetchone()
    cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ?', (result[0], veebileht))
    connection.commit()
    connection.close()

#andmete kogumine
def kuva_veebilehed():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM websites') #Käivitab sql käsklusi ning muudab andmebaasi
    andmed = cursor.fetchall()


    connection.close()
    return andmed

