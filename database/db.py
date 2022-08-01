from database import create_connection


class SalerData:

    @staticmethod
    def add_user(saler_id, fio, phone):
        cnx, cur = create_connection()
        cur.execute(f'''INSERT INTO users(id,fio,phone)
                        VALUES ({saler_id}, '{fio}', '{phone}')''')
        cnx.commit()
        cnx.close()

    @staticmethod
    def get_user(saler_id):
        cnx, cur = create_connection()
        cur.execute(
            f''' SELECT * FROM `users` WHERE `id` = {saler_id}''')
        saler = cur.fetchone()
        cnx.close()
        return saler

    @staticmethod
    def get_user_id_by_phone(phone):
        cnx, cur = create_connection()
        cur.execute(
            f''' SELECT id FROM `users` WHERE `phone` = '{phone}' ''')
        saler = cur.fetchone()[0]
        cnx.close()
        return saler

    @staticmethod
    def update_user_point(saler_id):
        cnx, cur = create_connection()
        cur.execute(f'''UPDATE users SET `point` = `point` + 1 WHERE `id` = {saler_id}''')
        cur.execute(f'''INSERT INTO history(`datatime`, `points`, `user_id`) VALUES (NOW(), '+1', {saler_id})''')
        cnx.commit()
        cnx.close()

    @staticmethod
    def get_history(saler_id):
        cnx, cur = create_connection()
        cur.execute(f'''SELECT datatime, points FROM history WHERE user_id = {saler_id} ORDER BY datatime DESC''')
        data = cur.fetchall()
        new_data = []
        for i in range(len(data)):
            new_data.append(f'{data[i][0].strftime("%Y-%m-%d %H:%M:%S")}    {data[i][1]}')
        cnx.close()
        return new_data

    @classmethod
    def minus_user_point(cls, phone, points):
        cnx, cur = create_connection()
        saler_id = cls.get_user_id_by_phone(phone)
        cur.execute(f'''UPDATE users SET `point` = `point` - {points} WHERE `phone` = '{phone}' ''')
        cur.execute(f'''INSERT INTO history(`datatime`, `points`, `user_id`) VALUES (NOW(),'-{points}', {saler_id})''')
        cnx.commit()
        cnx.close()

    @staticmethod
    def update_user(saler_id, fio, phone):
        cnx, cur = create_connection()
        cur.execute(f'''UPDATE users SET `fio`='{fio}', `phone`='{phone}' WHERE `id`={saler_id} ''')
        cnx.commit()
        cnx.close()


class AdminData:
    @staticmethod
    def get_user_data(phone):
        cnx, cur = create_connection()
        cur.execute(f"SELECT * FROM users WHERE `phone` = '{phone}' ")
        data = cur.fetchone()
        cnx.close()
        return data

    @staticmethod
    def get_history():
        cnx, cur = create_connection()
        cur.execute(
            f'''SELECT users.fio, datatime, points
            FROM history
            INNER JOIN users ON history.user_id = users.id''')
        data = cur.fetchall()
        cnx.close()
        return data

    @staticmethod
    def get_excel():
        cnx, cur = create_connection()
        cur.execute(
            f'''SELECT `fio`, `phone`, `point` FROM users ''')
        data = cur.fetchall()
        cnx.close()
        return data
