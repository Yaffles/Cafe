import sqlite3

class Database():

    def __init__(self,dbname):
        self.__dbname = dbname

    def dbConnect(self):
        """Connect to the database"""

        try:
            conn = sqlite3.connect(self.__dbname)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection problem. Error: {e}")
            return None

    def dbGetData(self,sql):
        """Get data from the database"""
        returnData = None
        try:
            with sqlite3.connect(self.__dbname) as conn:
                # Indicate we want column names returned
                conn.row_factory = sqlite3.Row
                # Execute query and fetch all rows back and store data in the returnData variable
                returnData = conn.cursor().execute(sql).fetchall()
                # Now we get all the Courses one at a time

        except sqlite3.Error as e:
            print(f"Menu Database problem. Error: {e}")
            returnData = None
        return returnData

    def dbPutData(self,sql):
        """Put data into the database"""
        # insert sql command - returns new id
        newId = None
        try:
            with sqlite3.connect(self.__dbname) as conn:
                # Indicate we want column names returned
                cursor = conn.cursor()
                cursor.execute(sql)
                newId = cursor.lastrowid
                cursor.close()
        except sqlite3.Error as e:
            print(f"Menu Database problem. Error: {e}")
        finally:
            if conn:
                conn.commit()

        return newId

    def dbChangeData(self,sql):
        """Change data in the database"""
        # change data sql command - can be update or delete commands
        try:
            with sqlite3.connect(self.__dbname) as conn:
                # Indicate we want column names returned
                cursor = conn.cursor()
                cursor.execute(sql)
                cursor.close()

        except sqlite3.Error as e:
            print(f"Menu Database problem. Error: {e}")
        finally:
            if conn:
                conn.commit()


# Test harness - calls all the methods above to see if they work
def main():
    db = Database("spxcafecopy.db")

    print(db)

    results = db.dbGetData("SELECT courseId,courseName FROM courses")
    if results:
        for course in results:
            print(course['courseId'],course['courseName'])

    sql = "INSERT INTO meals (mealName, mealPrice, courseId) VALUES ('meringue',6.5,3)"
    mealId = db.dbPutData(sql)

    results = db.dbGetData(f"SELECT * FROM meals WHERE mealId = {mealId}")
    if results:
        for meal in results:
            print(meal['mealId'],meal['mealName'],meal['mealPrice'])
    else:
        print(f"Meal {mealId} not found")

    sql = f"UPDATE meals SET mealName = 'Vanilla Slice' WHERE mealId = {mealId}"
    db.dbChangeData(sql)

    results = db.dbGetData(f"SELECT * FROM meals WHERE mealId = {mealId}")
    if results:
        for meal in results:
            print(meal['mealId'],meal['mealName'],meal['mealPrice'])
    else:
        print(f"Meal {mealId} not found")


    sql = f"DELETE FROM meals WHERE mealId = {mealId}"
    db.dbChangeData(sql)

    results = db.dbGetData(f"SELECT * FROM meals WHERE mealId = {mealId}")
    if results:
        for meal in results:
            print(meal['mealId'],meal['mealName'],meal['mealPrice'])
    else:
        print(f"Meal {mealId} not found")




if __name__=="__main__":
    main()
