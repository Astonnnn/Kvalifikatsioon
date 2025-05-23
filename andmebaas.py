import sqlite3

#Loob andmebaasi juhul, kui seda juba olemas pole
def loo_andmebaas():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor() #aitab andmebaasist asju võtta

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veebileht TEXT NOT NULL,
            ajalimiit INTEGER NOT NULL,
            staatus BOOLEAN DEFAULT FALSE,
            jaanud_aega FLOAT NOT NULL,
            kysimus_ees BOOLEAN DEFAULT FALSE
        );
    ''')

    connection.commit()
    connection.close()

#Muudab andmebaasis oleva veebilehe staatuse (blokeeritud/blokeerimata)
def muuda_staatus(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE websites SET staatus = not(staatus) WHERE veebileht = ?', (veebileht,))

    connection.commit()
    connection.close()

#Lisab andmebaasi rea
def lisa_veebileht_ja_aeg(veebileht, aeg):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM websites WHERE veebileht = ?', (veebileht,))
    eksisteerib = cursor.fetchone()

    if eksisteerib is not None:
        cursor.execute('UPDATE websites SET ajalimiit = ?, jaanud_aega = ? WHERE veebileht = ?', (aeg, aeg*60, veebileht))
        print(f'Uuendati andmebaasis veebilehte: {veebileht}')
    else:
        cursor.execute('INSERT INTO websites (veebileht, ajalimiit, staatus, jaanud_aega) VALUES (?, ?, ?, ?)', (veebileht, aeg, False, aeg*60))
        print(f'Lisati andmebaasi uus veebileht: {veebileht}')


    connection.commit() #salvestab muutused andmebaasi
    connection.close() #sulgeb ühenduse, et see jooksma ei jääks


#Võtab veebilehe järjeljäänud ajast 5 sekundit alla
def muuda_aeg(veebileht):
    try:
        connection = sqlite3.connect('andmed.db')
        cursor = connection.cursor()

        cursor.execute('SELECT jaanud_aega FROM websites WHERE veebileht = ?', (veebileht,))
        tulemus = cursor.fetchone()

        if tulemus is None:
            print(f'Veebisait puudub andmebaasist')
            return 0

        uus_aeg = tulemus[0] - 5

        cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ? ', (uus_aeg, veebileht,))
        connection.commit()
        connection.close()
        return uus_aeg

    except Exception as e:
        print(f'Probleem aja uuendamises: {e}')
        if connection:
            connection.close()
        return 0


#Taastab algselt määratud aja
def taasta_aeg(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ajalimiit from websites WHERE veebileht = ?', (veebileht,))
    tulemus = cursor.fetchone()

    if tulemus is not None:
        aeg = tulemus[0]*60
        cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ?', (aeg, veebileht,))
        connection.commit()
    else:
        print('Ei ole olemas')
    connection.close()

#Tagastab kõik andmebaasi andmed
def kuva_veebilehed():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM websites') #Käivitab sql käsklusi ning muudab andmebaasi
    andmed = cursor.fetchall()


    connection.close()
    return andmed

#kustutab andmebaasi rea, mille veebilehe tulbas on argument
def kustuta_veebileht(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM websites where veebileht = ?', (veebileht,))
    connection.commit()
    connection.close()

#muudab staatust tulbal, mis märgib, kas hetkel on küsimus ees või mitte
def muuda_küsimise_kuvamise_staatus(veebileht):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE websites SET kysimus_ees = not(kysimus_ees) where veebileht = ?', (veebileht,))
    connection.commit()
    connection.close()