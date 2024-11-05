import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

SERVER_PARAMS = {
    'dbname': 'postgres',  # подключаемся к существующей базе для создания новой
    'user': 'postgres',
    'password': 'Пароль',
    'host': 'localhost'
}

DB_PARAMS = {
    'dbname': 'client_db',  # имя новой базы данных
    'user': 'postgres',
    'password': 'Пароль',
    'host': 'localhost'
}

def connect_server():
    #print("SERVER_PARAMS:", SERVER_PARAMS)
    return psycopg2.connect(**SERVER_PARAMS)

def connect_db():
    return psycopg2.connect(**DB_PARAMS)


# Функция для создания новой базы данных
def create_database():
    conn = connect_server()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE client_db")
        print("База данных 'client_db' создана.")
    except psycopg2.errors.DuplicateDatabase:
        print("База данных 'client_db' уже существует.")

    cursor.close()
    conn.close()


# Функция для создания таблиц в базе данных
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Создание таблицы клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    ''')

    # Создание таблицы телефонов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
            phone VARCHAR(20) NOT NULL
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Таблицы 'clients' и 'phones' созданы.")


def add_client(first_name, last_name, email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (first_name, last_name, email))

    client_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return client_id


def add_phone(client_id, phone):
    conn = connect_db()
    cursor = conn.cursor()

    # Проверка, существует ли клиент с таким client_id
    cursor.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
    client_exists = cursor.fetchone()

    if not client_exists:
        print(f"Ошибка: Клиент с ID {client_id} не существует.")
        cursor.close()
        conn.close()
        return

    cursor.execute('''
        INSERT INTO phones (client_id, phone)
        VALUES (%s, %s)
    ''', (client_id, phone))
    print("Телефон добавлен.")
    conn.commit()
    cursor.close()
    conn.close()


def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = connect_db()
    cursor = conn.cursor()

    # Проверка, существует ли клиент с таким client_id
    cursor.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
    client_exists = cursor.fetchone()

    if not client_exists:
        print(f"Ошибка: Клиент с ID {client_id} не существует.")
        cursor.close()
        conn.close()
        return

    if first_name:
        cursor.execute('UPDATE clients SET first_name = %s WHERE id = %s', (first_name, client_id))
    if last_name:
        cursor.execute('UPDATE clients SET last_name = %s WHERE id = %s', (last_name, client_id))
    if email:
        cursor.execute('UPDATE clients SET email = %s WHERE id = %s', (email, client_id))

    print("Данные клиента обновлены.")

    conn.commit()
    cursor.close()
    conn.close()


def delete_phone(client_id, phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM phones WHERE client_id = %s AND phone = %s
    ''', (client_id, phone))

    conn.commit()
    cursor.close()
    conn.close()


def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Проверка, существует ли клиент с таким client_id
    cursor.execute("SELECT id FROM clients WHERE id = %s", (client_id,))
    client_exists = cursor.fetchone()

    if not client_exists:
        print(f"Ошибка: Клиент с ID {client_id} не существует.")
        cursor.close()
        conn.close()
        return

    cursor.execute('DELETE FROM clients WHERE id = %s', (client_id,))

    print("Телефон удален.")

    conn.commit()
    cursor.close()
    conn.close()

def find_client(first_name=None, last_name=None, email=None, phone=None):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()

    if not clients:
        print("\nНет данных о клиентах.")
        cursor.close()
        conn.close()
        return

    if phone:
        cursor.execute('''
            SELECT clients.id, clients.first_name, clients.last_name, clients.email
            FROM clients
            JOIN phones ON clients.id = phones.client_id
            WHERE phones.phone = %s
        ''', (phone,))
    else:
        query = sql.SQL('SELECT id, first_name, last_name, email FROM clients WHERE 1=1')
        params = []
        if first_name:
            query = query + sql.SQL(' AND first_name = %s')
            params.append(first_name)
        if last_name:
            query += sql.SQL(' AND last_name = %s')
            params.append(last_name)
        if email:
            query += sql.SQL(' AND email = %s')
            params.append(email)

        #print(query,params)
        cursor.execute(query, params)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_all_data():
    """Функция для вывода всех данных из таблиц clients и phones"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()

    if not clients:
        print("\nНет данных о клиентах.")
        cursor.close()
        conn.close()
        return

    print("\nДанные из таблицы 'clients':")

    for client in clients:
        client_id, first_name, last_name, email = client
        print(f"ID: {client_id}, Имя: {first_name}, Фамилия: {last_name}, Email: {email}")

    cursor.execute("SELECT phone FROM phones WHERE client_id = %s", (client_id,))
    phones = cursor.fetchall()

    # Если у клиента есть телефоны, выводим их
    if phones:
        print("Телефоны:", ", ".join(phone[0] for phone in phones))
    else:
        print("Телефоны: нет номеров")

    cursor.close()
    conn.close()


def display_menu():
    print("\nМеню:")
    print("1. Добавить нового клиента")
    print("2. Добавить телефон для клиента")
    print("3. Изменить данные клиента")
    print("4. Удалить телефон клиента")
    print("5. Удалить клиента")
    print("6. Найти клиента")
    print("7. Вывести все данные таблиц")
    print("0. Выйти")


def main():
    create_database()
    create_tables()

    while True:
        display_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            email = input("Введите email: ")
            client_id = add_client(first_name, last_name, email)
            print(f"Клиент добавлен с ID {client_id}")

        elif choice == "2":
            client_id = int(input("Введите ID клиента: "))
            phone = input("Введите телефон: ")
            add_phone(client_id, phone)


        elif choice == "3":
            client_id = int(input("Введите ID клиента: "))
            first_name = input("Введите новое имя (нажмите Enter, чтобы пропустить): ") or None
            last_name = input("Введите новую фамилию (нажмите Enter, чтобы пропустить): ") or None
            email = input("Введите новый email (нажмите Enter, чтобы пропустить): ") or None
            update_client(client_id, first_name, last_name, email)


        elif choice == "4":
            client_id = int(input("Введите ID клиента: "))
            phone = input("Введите телефон для удаления: ")
            delete_phone(client_id, phone)


        elif choice == "5":
            client_id = int(input("Введите ID клиента: "))
            delete_client(client_id)
            print("Клиент удален.")

        elif choice == "6":
            first_name = input("Введите имя для поиска (нажмите Enter, чтобы пропустить): ") or None
            last_name = input("Введите фамилию для поиска (нажмите Enter, чтобы пропустить): ") or None
            email = input("Введите email для поиска (нажмите Enter, чтобы пропустить): ") or None
            phone = input("Введите телефон для поиска (нажмите Enter, чтобы пропустить): ") or None
            results = find_client(first_name, last_name, email, phone)
            if results:
                for client in results:
                    print(f"ID: {client[0]}, Имя: {client[1]}, Фамилия: {client[2]}, Email: {client[3]}")
            else:
                print("Клиент не найден.")

        elif choice == "7":
            get_all_data()  # Вывод всех данных из таблиц clients и phones

        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите пункт из меню.")


if __name__ == '__main__':
    main()
