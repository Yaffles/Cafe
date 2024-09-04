from SPXCafe import SPXCafe
import Course
from rapidfuzz.fuzz import partial_ratio

class Meal(SPXCafe):
    def __init__(self, mealId=None, mealName=None, mealPrice=None, course=None):
        """Constructor Method"""
        super().__init__()
        #TODO dont use courseId
        self.setMealId(mealId)
        self.setMealName(mealName)
        self.setMealPrice(mealPrice)
        self.setCourse(course)

        if self.existsDB():
            if not self.setMeal():
                print(f"Meal with ID {mealId} does not exist in the database.")
        else:
            self.save()

    def setMeal(self, mealId=None):
        retcode = False
        if mealId is not None:
            self.setMealId(mealId)

        if self.getMealId():
            sql = f"SELECT mealId, mealName, mealPrice, courseId FROM meals WHERE mealId = {self.getMealId()}"

            mealData = self.dbGetData(sql)

            for meal in mealData:
                self.setMealId(meal['mealId'])
                self.setMealName(meal['mealName'])
                self.setMealPrice(meal['mealPrice'])
                self.setCourse(Course.Course(meal['courseId']))
            retcode = True
        return retcode

    def setMealId(self, mealId):
        self.__mealId = mealId
    def setMealName(self, mealName):
        self.__mealName = mealName
    def setMealPrice(self, mealPrice):
        self.__mealPrice = mealPrice
    def setCourse(self, course=None):
        if course and isinstance(course, Course.Course):
            self.__course = course
        else:
            self.__course = None

    def getMealId(self):
        return self.__mealId
    def getMealName(self):
        return self.__mealName
    def getMealPrice(self):
        return self.__mealPrice
    def getCourse(self):
        return self.__course

    def findMeal(self, searchMeal=None):
        '''Find a Meal by name using partial_ratio from rapidfuzz'''
        if searchMeal:
            if self.isMatch(searchMeal):
                return self
        return None

    def isMatch(self, searchMeal):
        '''Check if the searchMeal is a match to the meal name'''
        return partial_ratio(searchMeal.lower(), self.getMealName().lower()) > 80

    def __str__(self):
        return f"Meal ID: {self.getMealId()}, Meal Name: {self.getMealName()}, Meal Price: {self.getMealPrice()}, Course ID: {self.getCourse().getCourseId()}"

    def display(self):
        '''Formal display Meal'''
        # print(f"Meal: <Course:{self.getCourse().getCourseId():2d} {self.getCourse().getCourseName().title()}, Meal:{self.getMealId():2d}> {self.getMealName().title():20s} ${self.getMealPrice():5.2f}")
        print(f"    > {self.getMealName().title():20s} ${self.getMealPrice():5.2f}")



    def existsDB(self):
        '''Check if the meal exists in the database'''
        retcode = False
        if self.getMealId():
            sql = f"SELECT count(*) AS count FROM meals WHERE mealId = {self.getMealId()}"

            countData = self.dbGetData(sql)
            if countData:
                for countRec in countData:
                    count = int(countRec['count'])
                if count > 0:
                    retcode = True
        return retcode

    def save(self):
        '''Save meal data back to the database'''


        if self.existsDB():
            sql = f'''UPDATE meals SET
                mealName='{self.getMealName()}',
                mealPrice={self.getMealPrice()},
                courseId={self.getCourse().getCourseId()}
                WHERE mealId={self.getMealId()}
            '''
            self.dbChangeData(sql)
        else:
            sql = f'''
                INSERT INTO meals
                (mealName, mealPrice, courseId)
                VALUES
                ('{self.getMealName()}', {self.getMealPrice()}, {self.getCourse().getCourseId()})
            '''
            # Save new primary key
            self.setMealId(self.dbPutData(sql))

    @classmethod
    def getMeals(cls,course):
        '''Gets Meals for a Course object/instance - example of Aggregation'''
        meals=[]
        if course and isinstance(course, Course.Course):
            sql = f"SELECT mealId, mealName, mealPrice, courseId FROM meals WHERE courseId={course.getCourseId()}"

            mealsData = SPXCafe().dbGetData(sql)

            for mealData in mealsData:
                # create a new instance
                meal = cls.__new__(cls)
                meal.setMealId(mealData['mealId'])
                meal.setMealName(mealData['mealName'])
                meal.setMealPrice(mealData['mealPrice'])
                meal.setCourse(course)
                # add meal object to meals list
                meals.append(meal)

        return meals


def main():
    meal = Meal(1)

    meal.display()
    meal.setMealPrice(meal.getMealPrice() + 1)
    meal.save()

    meal = Meal(1)
    meal.display()

    meal = Meal(mealName="Salata2", mealPrice=3.45, course=Course(1))
    meal.display()

    searchMeal = "salata"
    meal = meal.findMeal(searchMeal)
    if meal:
        meal.display()
    else:
        print(f"Meal {searchMeal} not found.")

if __name__ == "__main__":
    main()
