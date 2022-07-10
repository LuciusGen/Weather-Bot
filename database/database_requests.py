import os

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


class DatabaseRequests:
    def __init__(self):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()
        db_cursor.execute('SELECT * FROM sites')
        self.sites_in_table = [i.name for i in db_cursor.description[1:]]

    def select_time(self, user_id: str):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        db_cursor.execute("SELECT * FROM time "
                          "WHERE user_id = %s",
                          (user_id,))
        try:
            return db_cursor.fetchall()[0]
        except Exception:
            return None

    def select_all_user_by_time(self, hour: int):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()
        select_time = "%s:00:00" % hour

        db_cursor.execute("SELECT * FROM time "
                          "WHERE time = %s",
                          (select_time,))
        try:
            return db_cursor.fetchall()[0]
        except Exception:
            return None

    def select_sites(self, user_id: str):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        db_cursor.execute("SELECT * FROM sites "
                          "WHERE user_id = %s",
                          (user_id,))
        try:
            user_sites = db_cursor.fetchall()[0][1:]
            user_res_sites = []
            for i in range(len(user_sites)):
                if user_sites[i]:
                    user_res_sites.append(self.sites_in_table[i])
            return user_res_sites
        except Exception:
            return None

    def select_city(self, user_id: str):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        db_cursor.execute("SELECT * FROM city "
                          "WHERE user_id = %s",
                          (user_id,))
        try:
            return db_cursor.fetchall()[0]
        except Exception:
            return None

    def insert_time(self, user_id: str, time):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        try:
            db_cursor.execute(
                "INSERT INTO time (user_id, time)"
                "VALUES (%s, %s )",
                (user_id, time)
            )
            db_connector.commit()
        except psycopg2.IntegrityError:
            pass

    def insert_sites(self, user_id: str):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        try:
            db_cursor.execute(
                "INSERT INTO sites (user_id)"
                "VALUES (%s)",
                (user_id,)
            )
            db_connector.commit()
        except psycopg2.IntegrityError:
            pass

    def insert_city(self, user_id: str, city):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        try:
            db_cursor.execute(
                "INSERT INTO city (user_id, city)"
                "VALUES (%s, %s)",
                (user_id, city)
            )
            db_connector.commit()
        except psycopg2.IntegrityError:
            pass

    def insert_new_user(self, user_id: str, city: str, time):
        self.insert_city(user_id, city)
        self.insert_sites(user_id)
        self.insert_time(user_id, time)

    def update_time(self, user_id, time):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        db_cursor.execute("UPDATE time "
                          "SET time = %s "
                          "WHERE user_id = %s",
                          (time,
                           user_id)
                          )
        db_connector.commit()

    def update_city(self, user_id, city):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        db_cursor.execute("UPDATE city "
                          "SET city = %s"
                          "WHERE user_id = %s",
                          (city,
                           user_id)
                          )
        db_connector.commit()

    def update_site(self, user_id: str, sites_to_update: list):
        db_connector = psycopg2.connect(DATABASE_URL)
        db_cursor = db_connector.cursor()

        cites_in_format = [False for _ in self.sites_in_table]
        for i in sites_to_update:
            cites_in_format[self.sites_in_table.index(i)] = True

        db_cursor.execute(
            "UPDATE sites "
            "SET rp5 = %s, meteoinfo = %s, foreca = %s "
            "WHERE user_id = %s ",
            (cites_in_format[0],
             cites_in_format[1],
             cites_in_format[2],
             user_id)
        )
        db_connector.commit()

    def check_user_in_db(self, user_id):
        if self.select_city(user_id) and self.select_sites(user_id) and self.select_time(user_id):
            return True
        return False
