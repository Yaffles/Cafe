from Meal import Meal
from Course import Course
from SPXCafe import SPXCafe

class Menu(SPXCafe):
    def __init__(self, menuName=None) -> None:
        super().__init__()
        self.setMenuName(menuName)

        # sets menu to db values
        self.setMenu()

    def setMenu(self):
        self.setCourses(Course.getCourses())

    def setCourses(self, courses):
        self.__courses = courses

    def setMenuName(self, menuName=None):
        if menuName is not None:
            self.__menuName = menuName
        else:
            self.__menuName = "The Menu"

    def getMenuName(self):
        return f"{self.__menuName}"

    def getCourses(self):
        return self.__courses

    def __str__(self) -> str:
        return f"{self.getMenuName()} Menu"

    def display(self):
        print(f"{"-"*5}{self.getMenuName()} {"-"*5}\n")
        if self.getCourses():
            for course in self.getCourses():
                course.display()

    def displayCourses(self):
        print(f"Course List: ", end="")
        courseNames = []
        for course in self.getCourses():
            courseNames.append(course.getCourseName().title())
        print(", ".join(courseNames))

    def findMeal(self, searchMeal=None):
        meals = []
        if searchMeal:
            for course in self.getCourses():
                meals += course.findMeal(searchMeal)
            return meals

    def findCourse(self, searchCourse=None):
        courses = []
        if searchCourse:
            for course in self.getCourses():
                foundCourse = course.findCourse(searchCourse)
                courses.append(foundCourse)
        return courses

def main():
    menu = Menu("Ristorant italiano")
    menu.display()

    menu.displayCourses()

    searchMeal = input("What meal do you want? ")
    meals = menu.findMeal(searchMeal)
    print("Meals found: ")
    for meal in meals:
        meal.display()

    searchCourse = input("What course do you want? ")
    courses = menu.findCourse(searchCourse)
    print("We have found the following course(s): ")
    for course in courses:
        course.display()

if __name__ == "__main__":
    main()
