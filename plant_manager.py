from database import get_db_connection


class PlantManager:

    @staticmethod
    def get_all_plant_data():
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM plants')
                plant_data = cursor.fetchall()
        return plant_data

    @staticmethod
    def get_plant_data_for_user(user_id):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT plants.* FROM user_plants JOIN plants ON user_plants.plant_name = plants.plant_name WHERE user_id = %s', (user_id,))
                plant_data = cursor.fetchall()
        return plant_data

    @staticmethod
    def get_plant_names_for_user(user_id):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT plant_name FROM user_plants WHERE user_id = %s', (user_id,))
                plants = cursor.fetchall()
        return [plant['plant_name'] for plant in plants]

    @staticmethod
    def add_plant_for_user(plant_name, user_id):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('INSERT INTO user_plants (user_id, plant_name) VALUES (%s, %s)', (user_id, plant_name))
                connection.commit()

    @staticmethod
    def remove_plant_for_user(plant_name, user_id):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('DELETE FROM user_plants WHERE user_id = %s AND plant_name = %s', (user_id, plant_name))
                connection.commit()