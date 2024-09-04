from Meal import Meal
from Course import Course
from SPXCafe import SPXCafe

class Menu(SPXCafe):
    def __init__(self, menuName=None) -> None:
        """Constructor Method"""
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

    def getCourses(self) -> list[Course]:
        return self.__courses

    def __str__(self) -> str:
        return f"{self.getMenuName()} Menu"

    def display(self):
        """Display the menu"""
        # print(f"{"-"*5}{self.getMenuName()} {"-"*5}\n")
        print("""
╦┌┬┐┌─┐┬  ┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┬  ┬┌─┐┬─┐  ╦  ┬ ┬┌┐┌┌─┐┬ ┬
║ │ ├─┤│  │├─┤  ╠╣ │ │├┬┘├┤ └┐┌┘├┤ ├┬┘  ║  │ │││││  ├─┤
╩ ┴ ┴ ┴┴─┘┴┴ ┴  ╚  └─┘┴└─└─┘ └┘ └─┘┴└─  ╩═╝└─┘┘└┘└─┘┴ ┴""")
        if self.getCourses():
            for course in self.getCourses():
                course.display()

    def displayCourses(self):
        """Display the courses in the menu"""
        print(f"Course List: ", end="")
        courseNames = []
        for course in self.getCourses():
            courseNames.append(course.getCourseName().title())
        print(", ".join(courseNames))

    def findMeal(self, searchMeal=None) -> list[Meal]:
        """Find meals from a search term"""

        meals = []
        if searchMeal:
            for course in self.getCourses():
                meals += course.findMeal(searchMeal)
        return meals

    def findCourse(self, searchCourse=None):
        """Find courses from the menu"""

        courses = []
        if searchCourse:
            for course in self.getCourses():
                foundCourse = course.findCourse(searchCourse)
                courses.append(foundCourse)
        return courses

def main():
    menu = Menu("restaurant italiano")
    menu.display()

if __name__ == "__main__":
    main()
