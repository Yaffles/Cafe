import Meal
from SPXCafe import SPXCafe
from rapidfuzz.fuzz import partial_ratio

class Course(SPXCafe):
    """Course class - holds information about a Menu course"""

    def __init__(self, courseId=None, courseName=None, meals=None) -> None:
        """Constructor Method"""
        super().__init__()

        self.setCourseId(courseId)
        self.setCourseName(courseName)
        self.setMeals(meals)

        if self.existsDB():
            if not self.setCourse():
                print(f"Course with ID {courseId} does not exist in the database.")

    def setCourse(self, courseId=None):
        """Set the course data from the database"""

        retcode = False
        if courseId is not None:
            self.setCourseId(courseId)

        if self.getCourseId():
            sql = f"SELECT courseId, courseName FROM courses WHERE courseId = {self.getCourseId()}"

            courseData = self.dbGetData(sql)

            if courseData:
                for course in courseData:
                    self.setCourseId(course['courseId'])
                    self.setCourseName(course['courseName'])
                    self.setMeals(Meal.Meal.getMeals(self))
                    retcode = True
        return retcode

    def setCourseId(self, courseId):
        self.__courseId = courseId
    def setCourseName(self, courseName):
        if courseName is not None:
            self.__courseName = courseName.lower()
        else:
            self.__courseName = None

    def setMeals(self, meals=None):
        """Set the meals for the course"""
        if meals is not None:
            self.__meals = meals
        else:
            self.__meals = []

    def addMeal(self, meal):
        """Add a meal to the course"""
        if isinstance(meal, Meal.Meal):
            self.__meals.append(meal)
            meal.setCourse(self)

    def findMeal(self, searchMeal=None):
        """Find a Meal by name using NLP"""
        meals = []
        if searchMeal:
            for meal in self.getMeals():
                foundMeal = meal.findMeal(searchMeal)
                if foundMeal:
                    meals.append(foundMeal)
        return meals

    def findCourse(self, searchCourse=None):
        '''Find a Meal by name using NLP'''
        if searchCourse:
            if self.isMatch(searchCourse):
                return self
        return None

    def isMatch(self, searchCourse):
        '''Check if the searchMeal is a match to the meal name'''
        return partial_ratio(searchCourse.lower(), self.getCourseName().lower()) > 80

    def getCourseId(self):
        return self.__courseId
    def getCourseName(self):
        return self.__courseName
    def getMeals(self):
        return self.__meals

    def __str__(self) -> str:
        """String representation of the Course object"""
        return f"Course ID: {self.getCourseId()}, Course Name: {self.getCourseName()}"

    def display(self):
        """Display the Course object"""
        print(self.getCourseName().title()+": ")
        for meal in self.getMeals():
            meal.display()
        print()

    def existsDB(self):
        '''Check if object already exists in database'''
        retcode = False
        if self.getCourseId():
            sql = f"SELECT count(*) AS count FROM courses WHERE courseId={self.getCourseId()}"
            countData = self.dbGetData(sql)
            if countData:
                for countData in self.dbGetData(sql):
                    count = int(countData['count'])
                if count > 0:
                    retcode = True
        return retcode

    def save(self):
        """Save the Course object to the database"""

        if self.existsDB():
            sql = f"UPDATE courses SET courseName = '{self.getCourseName()}' WHERE courseId = {self.getCourseId()}"
            self.dbChangeData(sql)
        else:
            sql = f"INSERT INTO courses (courseName) VALUES ('{self.getCourseName()}')"
            self.setCourseId(self.dbPutData(sql))

    def delete(self):
        """Delete the Course object from the database"""

        if len(self.getMeals()) > 0:
            for meal in self.getMeals():
                meal.delete()
        else:
            sql = f"DELETE FROM courses WHERE courseId = {self.getCourseId()}"
            self.dbChangeData(sql)

    @classmethod
    def getCourses(cls):
        """Get all the courses from the database"""

        courses = []
        sql = "SELECT courseId, courseName FROM courses ORDER BY courseId"

        coursesData = SPXCafe().dbGetData(sql)

        for courseData in coursesData:
            course = cls.__new__(cls) # create empty object of type this class
            course.setCourseId(courseData['courseId'])
            course.setCourseName(courseData['courseName'])
            course.setMeals(Meal.Meal.getMeals(course))
            courses.append(course)
        return courses

def main():
    course = Course(1)
    course.display()
    course.setCourseName(course.getCourseName()+"X")
    course.save()
    course = Course(1)
    course.display()
    course1 = Course(courseName="New Course")
    course1.save()
    course1.display()

    print("New meal")
    meal = Meal.Meal(mealName="New meal", mealPrice=99.99, course=course1)
    meal.display()

    searchMeal = input("Search Meal: ").lower().strip()
    meals = course.findMeal(searchMeal)
    print("Meals found: ")
    if meals:
        for meal in meals:
            meal.display()
    else:
        print(f"Search result for {searchMeal} is not found")

    searchCourse = input("Search Course: ").lower().strip()
    isCourse = course.findCourse(searchCourse)
    if isCourse:
        isCourse.display()
    else:
        print(f"Search result for {searchCourse} is not found")


if __name__ == "__main__":
    main()
