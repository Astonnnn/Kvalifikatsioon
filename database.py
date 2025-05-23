import sqlite3

def create_database():
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

def change_status(website):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE websites SET staatus = not(staatus) WHERE veebileht = ?', (website,))

    connection.commit()
    connection.close()

def add_website_and_time(website, time):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM websites WHERE veebileht = ?', (website,))
    existing = cursor.fetchone()
    print(existing)

    if existing is not None:
        cursor.execute('UPDATE websites SET ajalimiit = ?, jaanud_aega = ? WHERE veebileht = ?', (time, time*60, website))
        print(f'Uuendati andmebaasis veebilehte: {website}')
    else:
        cursor.execute('INSERT INTO websites (veebileht, ajalimiit, staatus, jaanud_aega) VALUES (?, ?, ?, ?)', (website, time, False, time*60))
        print(f'Lisati andmebaasi uus veebileht: {website}')


    connection.commit() #salvestab muutused andmebaasi
    connection.close() #sulgeb ühenduse, et see jooksma ei jääks


def change_time(website):
    try:
        connection = sqlite3.connect('andmed.db')
        cursor = connection.cursor()

        cursor.execute('SELECT jaanud_aega FROM websites WHERE veebileht = ?', (website,))
        result = cursor.fetchone()

        if result is None:
            print(f'Veebisait puudub andmebaasist')
            return 0

        new_time = result[0] - 5

        cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ? ', (new_time, website,))
        connection.commit()
        connection.close()
        return new_time

    except Exception as e:
        print(f'Probleem aja uuendamises: {e}')
        if connection:
            connection.close()
        return 0

def restore_time(website):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ajalimiit from websites WHERE veebileht = ?', (website,))
    result = cursor.fetchone()

    if result is not None:
        time = result[0]*60
        cursor.execute('UPDATE websites SET jaanud_aega = ? WHERE veebileht = ?', (time, website,))
        connection.commit()
    else:
        print('Ei ole olemas')
    connection.close()

#andmete kogumine
def show_websites():
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM websites') #Käivitab sql käsklusi ning muudab andmebaasi
    data = cursor.fetchall()


    connection.close()
    return data

def delete_website(website):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM websites where veebileht = ?', (website,))
    connection.commit()
    connection.close()

def change_question_show_status(website):
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE websites SET kysimus_ees = not(kysimus_ees) where veebileht = ?', (website,))
    connection.commit()
    connection.close()