from Avatar import Avatar
from Menu import Menu
from Customer import Customer
from Order import Order
from NLP import NLP

from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract



class Chatbot():
    """Chatbot class - the main class for the chatbot"""

    def __init__(self, cafeName="Italiabot", waiterName="Luigi", menuName="Italia Forever Lunch", useSr=True):
        """Initialise the chatbot"""
        self.setCafeName(cafeName)
        self.waiter = Avatar(waiterName, useSr, speed=200) # Can increase speed if needed
        self.waiter.say(f"Welcome to {self.cafeName}, I am {waiterName}.")
        self.menu = Menu(menuName)
        self.nlp = NLP()

        #  These are the keywords for each option and the corresponding response when choosing that option
        self.exitRequest = ["exit","leave","bye", "abandon", "quit"]
        self.historyRequest = ["history", "previous"]
        self.menuRequest = ["menu", "course", "meal","choice","options"]
        self.orderRequest = ["order", "buy","food"]


        self.mainOptions = self.exitRequest + self.historyRequest + self.menuRequest + self.orderRequest

    def setCafeName(self, cafeName):
        self.cafeName = cafeName
    def getCafeName(self):
        return self.cafeName

    def getChoice(self, choice=None, options=None, requiredConfidence=80, question=None):
        ''' choose from a list of options'''
        if not options:
            return []
        matches = []
        maxConfidence = 0

        while len(matches)==0:
            if not choice:
                if not question:
                    question = "Please choose from the following options: " + ", ".join(options)
                choice = self.waiter.listen(question).strip().lower()
                if not choice:
                    break

            results = extract(choice, options, scorer=partial_ratio, processor=default_process)

            for result in results:
                (match, confidence, index) = result
                if confidence > maxConfidence:
                    maxConfidence = confidence
                    matches = [match]
                elif confidence == maxConfidence:
                    matches.append(match)



        if maxConfidence < requiredConfidence:
            return None
        return matches[0] if len(matches)>0 else []

    def getUserConfirmation(self, question=None):
        """Get the user's confirmation for a yes or no question"""

        # Define multiple options for "yes" and "no"
        yes_options = ["yes", "yeah", "yup", "sure", "of course"]
        no_options = ["no", "nope", "nah", "not really"]

        options = yes_options + no_options

        choice = self.getChoice(choice=None, options=options, requiredConfidence=80, question=question)
        # Determine if the choice is a "yes" or "no"
        if choice in yes_options:
            return "yes"
        elif choice in no_options:
            return "no"
        else:
            # Handle the case where the option is below the required confidence level
            return self.getUserConfirmation("I'm sorry, I didn't understand that. Please say yes or no.")

    def isPastCustomer(self):
        """Checks if the person has been to the restaurant before"""
        choice = self.getUserConfirmation(f"Have you been to {self.getCafeName()} before?")
        if choice == "yes":
            return True
        else:
            return False

    def getCustomer(self):
        '''Get a customer - using username typed in for accuracy '''

        # get user name - typed in for accuracy
        username = self.waiter.listen("Please enter your username: ",useSR=False)
        # lookup customer in database
        self.customer = Customer(username)



        if not self.customer.existsDB():
            self.waiter.say(f"I am sorry, I could not find you in our database with username {username}.")
            self.customer = None
            return False

        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}!")
        return True

    def createCustomer(self):
        '''Create a new customer'''
        self.waiter.say("Let's create a new account for you.")


        firstName = self.askForName("What is your first name?")
        lastName = self.askForName("What is your last name?")
        username = self.waiter.listen(f"Thank you {firstName} {lastName}. Please choose a username: ",useSR=False)

        self.customer = Customer(userName=username, firstName=firstName, lastName=lastName)
        self.customer.save()


        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}!")

    def askForName(self, question):
        """Ask the user for their name"""

        inp = self.waiter.listen(question, useSR=False)
        name = self.nlp.getName(inp)

        while name == "":
            inp = self.waiter.listen(f"Could not understand, {question}", useSR=False)
            name = self.nlp.getName(inp)
        names = name.split(" ")
        name = names[0].title()

        return name

    def getRequest(self):
        """Get the user's request for the chatbot"""
        while True:
            self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do? ")

            option = self.waiter.listen("Order food? See the menu? Look at your order history? or Exit?")
            if not option:
                self.waiter.say("I'm sorry, I didn't understand that. Please try again.")
                continue

            choice = self.getChoice(option, self.mainOptions)

            if choice:
                return choice

            self.waiter.say(f"I am sorry, I don't understand your choice. You said: '{option}'. Please try again.")

    def displayOrderHistory(self):
        """Display the order history of the customer"""
        orders = self.customer.getOrders()
        if len(orders) == 0:
            self.waiter.say(f"Sorry, {self.customer.getFirstName()}, I could not find any previous orders for you.")
        else:
            self.waiter.say(f"Ok, {self.customer.getFirstName()}. Let's show your previous orders. ")
            for order in orders:
                order.display()

    def displayMenu(self):
        """Display the menu of the restaurant"""
        self.waiter.say(f"Alright, {self.customer.getFirstName()}. Let's see the menu. ")

        self.menu.display()

    def displayCourse(self):
        """Display a single course in the menu or all"""
        course = self.chooseCourse()
        if course:
            course.display()

    def chooseCourse(self):
        """Ask the user to choose a course from the menu """
        courses = self.menu.getCourses()
        courseNames = [course.getCourseName() for course in courses] + ["all"]

        answer = self.waiter.listen("What course would you like to view?").strip().lower()
        selectedCourseName = self.getChoice(answer, courseNames)
        if selectedCourseName:
            if selectedCourseName == "all":
                self.menu.display()
                return None

            selectedCourse = [course for course in courses if course.getCourseName() == selectedCourseName][0]
            return selectedCourse
        else:
            self.waiter.say(f"Sorry, I could not find that course in the menu. Please try again.")
            return self.chooseCourse()

    def askForMeal(self):
        """Ask the user for the meal they would like to order"""
        item = self.waiter.listen("What would you like to order?").strip().lower()

        # check if user is asking to exit/abandon or view the menu
        contains = self.getChoice(item, self.exitRequest + self.menuRequest)
        if contains:
            if contains in self.exitRequest:
                return None, None
            elif contains in self.menuRequest:
                self.displayCourse()
                return self.askForMeal()

        numberWord = self.nlp.getNumber(item)

        quantity=None
        if numberWord:
            item = item.replace(numberWord, "").strip()
            quantity = self.nlp.getInteger(numberWord)

        if not quantity:
            if "couple" in item:
                quantity = 2
                item = item.replace(" couple", "").strip()
            elif " a " in item:
                quantity = 1
                item = item.replace("a", "").strip()


        meals = self.menu.findMeal(item)

        if len(meals) > 1:
            mealNames = [meal.getMealName() for meal in meals]
            while True:
                new = self.waiter.listen(f"Please choose between: {", ".join(mealNames)}")
                if new:
                    chosenMealNames = self.getChoice(new, mealNames)
                    chosenMeals = [meal for meal in meals if meal.getMealName() == chosenMealNames]
                    if len(chosenMeals) > 0:
                        return chosenMeals[0], quantity


        elif len(meals) == 0:
            self.waiter.say(f"Could not find {item} on the menu")
            return self.askForMeal()
        else:
            return meals[0], quantity

    def askForQuantity(self, meal) -> int:
        """Ask the user for the quantity of the meal they would like to order"""
        answer = self.waiter.listen(f"How many {meal.getMealName()}s would you like?")
        numberWord = self.nlp.getNumber(answer)

        quantity = None
        if numberWord:
            quantity = self.nlp.getInteger(numberWord)

        if quantity:
            return quantity


        self.waiter.say(f"Sorry, I could not understand the quantity. Please try again.")
        return self.askForQuantity(meal)



    def orderFood(self):
        """Create an order for the customer with at least 3 items."""
        self.waiter.say(f"Prego, {self.customer.getFirstName()}. Let's order some food. ")
        order = Order(self.customer)

        orderCancelled = False
        running = True

        self.menu.display()

        while running:
            meal, quantity = self.askForMeal()
            if meal is None: # user wants to exit
                orderCancelled = True
                running = False

            else:
                if not quantity:
                    quantity = self.askForQuantity(meal)

                # Add item to order
                order.addItem(meal, quantity)
                # State the item
                mealName = meal.getMealName() + ("s" if quantity > 1 else "")
                self.waiter.say(f"Ok, {quantity} {mealName} added to your order.")

                # If order is finished, ask for confirmation
                if order.getItemAmount() >= 3:
                    choice = self.getUserConfirmation("Would you like to order anything else?")
                    if choice == "no":
                        self.waiter.say("Ok, you have ordered:")
                        self.waiter.say(str(order))
                        choice = self.getUserConfirmation("Is this order correct?")
                        if choice == "yes":
                            running = False


        if orderCancelled:
            self.waiter.say(f"Ok {self.customer.getFirstName()}, the order has been cancelled.")
            return

        id = order.save()
        if id:
            self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering at {self.getCafeName()} today. Your order number is {id}.")
        else:
            self.waiter.say(f"Sorry, {self.customer.getFirstName()}, I could not process your order. Please try again later.")





    def run(self):
        """Run the chatbot"""
        # get the customer
        if not self.isPastCustomer() or not self.getCustomer():
            self.createCustomer()

        # LOOP - 1) Order? 2) View Menu 3) Order History 4) Leave/Exit
        running = True
        while running:

            choice = self.getRequest()

            if choice in self.exitRequest:
                self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for visiting {self.getCafeName()}. We hope to see you again soon!")
                running = False

            elif choice in self.historyRequest:
                self.displayOrderHistory()
            elif choice in self.menuRequest:
                self.displayCourse()
            elif choice in self.orderRequest:
                self.orderFood()

def main():
    italiabot = Chatbot(cafeName="Italiabot", waiterName="Luigi", menuName="Italia Forever Lunch", useSr=True)
    italiabot.run()


if __name__ == "__main__":
    main()
