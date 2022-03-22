import mysql.connector

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class Database:
    def __init__(self): #connexion à la base de donnée qui sera rappeler à chaque fois
        self.conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database='agence_tourisme'
                )

    def connexion(self):
        return self.conn

    def query_arguments(self, sql, args: tuple = ()):
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute(sql, args)
        return mycursor

    def query_simple(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        return mycursor

    def query_for2_3(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        for query in mycursor:
            results = str(query)[2:-3]
        mycursor.close()
        return results

    def query_for1_4(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        for query in mycursor:
            results = str(query)[1:-4]
        mycursor.close()
        return results

    def query_for15_3(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        for query in mycursor:
            results = str(query)[15:-3]
        mycursor.close()
        return results

    def query_for1_2(self, sql):
        mycursor = self.conn.cursor()
        mycursor.execute(sql)
        for query in mycursor:
            results = str(query)[1:-2]
        mycursor.close()
        return results

    def fetchall_arguments(self, sql, args):
        mycursor = self.query_arguments(sql, args)
        results = mycursor.fetchall()
        mycursor.close()
        return results

    def fetchall_simple(self, sql):
        mycursor = self.query_simple(sql)
        results = mycursor.fetchall()
        mycursor.close()
        return results

    def fetchone_arguments(self, sql, args):
        mycursor = self.query_arguments(sql, args)
        results = mycursor.fetchone()[0]
        mycursor.close()
        return results

    def fetchone_simple(self, sql):
        mycursor = self.query_simple(sql)
        results = mycursor.fetchone()[0]
        mycursor.close()
        return results

    def commit(self, sql, args):
        self.query_arguments(sql, args)
        self.conn.commit()

if __name__ == '__main__':
    connexion_unique = Database.Instance()
    query_test = " SELECT id FROM circuit WHERE nom = %s "
    test = ('voyage',)
    test_reussi = connexion_unique.fetchall_arguments(query_test, test)
    print(test_reussi)






