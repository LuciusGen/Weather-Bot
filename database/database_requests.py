import sqlite3


class DatabaseRequests:
    def __init__(self, db_name: str):
        self.__db_connector = sqlite3.connect(db_name, check_same_thread=False)
        self.__db_cursor = self.__db_connector.cursor()
        self.sites_in_table = list(map(lambda x: x[0],
                                       self.__db_connector.execute('SELECT * FROM sites').description))[1:]

    def select_time(self, user_id: str):
        self.__db_cursor.execute("SELECT * FROM time "
                                 "WHERE user_id = ?",
                                 (user_id,))
        try:
            return self.__db_cursor.fetchall()[0]
        except Exception:
            return None

    def select_sites(self, user_id: str):
        self.__db_cursor.execute("SELECT * FROM sites "
                                 "WHERE user_id = ?",
                                 (user_id,))
        try:
            user_sites = self.__db_cursor.fetchall()[0][1:]
            user_res_sites = []
            for i in range(len(user_sites)):
                if user_sites[i] == "1":
                    user_res_sites.append(self.sites_in_table[i])
            return user_res_sites
        except Exception:
            return None

    def select_city(self, user_id: str):
        self.__db_cursor.execute("SELECT * FROM city "
                                 "WHERE user_id = ?",
                                 (user_id,))
        try:
            return self.__db_cursor.fetchall()[0]
        except Exception:
            return None

    def insert_time(self, user_id: str, time):
        try:
            self.__db_cursor.execute(
                "INSERT INTO time (user_id, time)"
                "VALUES (?, ?)",
                (user_id, time)
            )
            self.__db_connector.commit()
        except sqlite3.IntegrityError:
            pass

    def insert_sites(self, user_id: str):
        try:
            self.__db_cursor.execute(
                "INSERT INTO sites (user_id)"
                "VALUES (?)",
                (user_id,)
            )
            self.__db_connector.commit()
        except sqlite3.IntegrityError:
            pass

    def insert_city(self, user_id: str, city):
        try:
            self.__db_cursor.execute(
                "INSERT INTO city (user_id, city)"
                "VALUES (?, ?)",
                (user_id, city)
            )
            self.__db_connector.commit()
        except sqlite3.IntegrityError:
            pass

    def insert_new_user(self, user_id: str, city: str, time):
        self.insert_city(user_id, city)
        self.insert_sites(user_id)
        self.insert_time(user_id, time)

    def update_time(self, user_id, time):
        self.__db_cursor.execute("UPDATE time "
                                 "SET time = ?"
                                 "WHERE user_id == ? ",
                                 (time,
                                  user_id)
                                 )
        self.__db_connector.commit()

    def update_city(self, user_id, city):
        self.__db_cursor.execute("UPDATE city "
                                 "SET city = ?"
                                 "WHERE user_id == ? ",
                                 (city,
                                  user_id)
                                 )
        self.__db_connector.commit()

    def update_site(self, user_id: str, sites_to_update: list):
        cites_in_format = [0 for _ in self.sites_in_table]
        for i in sites_to_update:
            cites_in_format[self.sites_in_table.index(i)] = 1

        self.__db_cursor.execute(
            "UPDATE sites "
            "SET rp5 = ?, Mail = ?, Meteoinfo = ?, Yandex = ?, Foreca= ?, Gismeteo = ?, Accuweather = ?"
            "WHERE user_id == ? ",
            (cites_in_format[0],
             cites_in_format[1],
             cites_in_format[2],
             cites_in_format[3],
             cites_in_format[4],
             cites_in_format[5],
             cites_in_format[6],
             user_id)
        )
        self.__db_connector.commit()

    def check_user_in_db(self, user_id):
        if self.select_city(user_id) and self.select_sites(user_id) and self.select_time(user_id):
            return True
        return False
