from Avatar import Avatar
from Menu import Menu
from Customer import Customer
from Order import Order
from OrderItem import OrderItem

from Meal import Meal # only for pretty

from NLP import NLP

from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract, extractOne


class Chatbot():
    """Chatbot class - the main class for the chatbot"""

    def __init__(self, cafeName="Italiabot", waiterName="Luigi"):
        """Initialise the chatbot"""

        self.setCafeName(cafeName)
        self.waiter = Avatar(waiterName)
        self.waiter.say(f"Welcome to {self.cafeName}, I am {waiterName}.")
        self.menu = Menu("Italia Forever Lunch")
        self.nlp = NLP()

        #  These are the keywords for each option and the corresponding response when choosing that option
        self.exitRequest = ["exit","leave","bye", "abandon", "quit"]
        self.historyRequest = ["history", "previous"]
        self.menuRequest = ["menu", "course", "meal","choice","options"]
        self.orderRequest = ["order", "buy","food"]
        self.dieRequest = ["die", "kill", "kym"]


        self.mainOptions = self.exitRequest + self.historyRequest + self.menuRequest + self.orderRequest + self.dieRequest

    def setCafeName(self, cafeName):
        self.cafeName = cafeName
    def getCafeName(self):
        return self.cafeName

    def getOptions(self, choice=None, options=None, requiredConfidence=80):
        ''' choose from a list options'''
        matches = []
        maxConfidence = 0

        while len(matches)==0:
            if not choice:
                choice = self.waiter.listen().strip().lower()
                if not choice:
                    break

            results = extract(choice, options, scorer=partial_ratio, processor=default_process)

            for result in results:
                (match, confidence, index) = result
                # print(f"Checking: {result}")
                if confidence > maxConfidence:
                    maxConfidence = confidence
                    matches = [match]
                elif confidence == maxConfidence:
                    matches.append(match)

            # print(f"You have matched: {','.join(matches)} with confidence level {maxConfidence}% {len(matches)}")


        if maxConfidence < requiredConfidence:
            return None
        return matches[0] if len(matches)>0 else []

    def getUserConfirmation(self, choice=None):
        """Get the user's confirmation for a yes or no question"""

        # Define multiple options for "yes" and "no"
        yes_options = ["yes", "yeah", "yup", "sure", "of course"]
        no_options = ["no", "nope", "nah", "not really"]

        options = yes_options + no_options

        choice = self.getOptions(choice=choice, options=options, requiredConfidence=80)
        # Determine if the choice is a "yes" or "no"
        if choice in yes_options:
            return "yes"
        elif choice in no_options:
            return "no"
        else:
            # Handle the case where the option is below the required confidence level
            inp = self.waiter.listen("I'm sorry, I didn't understand that. Please say yes or no.")
            return self.getUserConfirmation(inp)

    def isPastCustomer(self):
        """Checks if the person has been to the restaurant before"""
        inp = self.waiter.listen(f"Have you been to {self.getCafeName()} before?").strip().lower()
        choice = self.getUserConfirmation(inp)
        if choice == "yes":
            return True
        else:
            return False

    def getCustomer(self):
        '''Get a customer - using username typed in for accuracy '''

        # get user name - typed in for accuracy
        username = self.waiter.listen("Please enter your username: ",useSR=False)
        print(".... Checking our customer database.....")
        # lookup customer in database
        self.customer = Customer(username)



        if self.customer.existsDB():
            print("Customer exists")
        else:
            print(f"Customer with username {username} does not exist")
            self.waiter.say(f"I am sorry, I could not find you in our database with username {username}.")
            self.customer = None
            return False

        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}!")
        return True

    def createCustomer(self):
        '''Create a new customer'''
        self.waiter.say("Let's create a new account for you.")


        firstName, lastName = self.askForName()

        # self.waiter.say(f"Hello {names}. Welcome to Italiabot. How can I help you today?")
        


        # get username
        username = self.waiter.listen(f"Thank you {firstName}. Please choose a uesrname: ",useSR=False)
        self.customer = Customer(userName=username, firstName=firstName, lastName=lastName)
        self.customer.save()
    
        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}.  May I call your {self.customer.getFirstName()}?")

    def askForName(self):
        """Ask the user for their name"""

        inp = self.waiter.listen("What is your name?", useSR=False)
        name = self.nlp.getNameByPartsOfSpeech(inp)

        while name == "":
            inp = self.waiter.listen("Could not understand, what is your name?", useSR=False)
            name = self.nlp.getNameByPartsOfSpeech(inp)


    
        names = name.split(" ")
        firstName = names[0].title()
        lastName = names[1].title() if len(names)>1 else ""

        return firstName,lastName

    def getRequest(self):
        """Get the user's request for the chatbot"""
        while True:
            self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do? ")

            option = self.waiter.listen("Order food? See the menu? Look at your order history? or Exit?")

            choice = self.getOptions(option, self.mainOptions)

            if choice:
                return choice
            
            self.waiter.say(f"I am sorry, I don't understand your choice. You said: '{option}. Please try again.")

    def displayOrderHistory(self):
        """Display the order history of the customer"""
        self.waiter.say(f"Ok, {self.customer.getFirstName()}. Let's show your previous orders. ")
        orders = Order.getOrdersByCustomer(self.customer.getCustomerId())
        for o in orders:
            o.display()

    def displayMenu(self):
        """Display the menu of the restaurant"""
        self.waiter.say(f"Alright, {self.customer.getFirstName()}. Let's see the menu. ")
        
        self.menu.display()
    
    def displayCourse(self):
        """Display a single course in the menu"""
        course = self.chooseCourse()
        if course:
            course.display()

    def chooseCourse(self):
        """Ask the user to choose a course from the menu"""
        courses = self.menu.getCourses()
        courseNames = [course.getCourseName() for course in courses] + ["all"]

        answer = self.waiter.listen("What course would you like to view?").strip().lower()
        selectedCourseName = self.getOptions(answer, courseNames)
        if selectedCourseName:
            if selectedCourseName == "all":
                self.menu.display()
                return None
            
            selectedCourse = [course for course in courses if course.getCourseName() == selectedCourseName][0]
            return selectedCourse
        else:
            self.waiter.say(f"Sorry, I could not find that course in the menu. Please try again.")
            return self.chooseCourse()

    def askForMeal(self) -> tuple[Meal, int]:
        """Ask the user for the meal they would like to order""" 
        item = self.waiter.listen("What would you like to order?").strip().lower()

        # check if user is asking to exit/abandon or view the menu
        contains = self.getOptions(item, self.exitRequest + self.menuRequest)
        if contains:
            if contains in self.exitRequest:
                self.waiter.say(f"Ok {self.customer.getFirstName()}, the order has been cancelled.")
                return None, None
            elif contains in self.menuRequest:
                self.displayCourse()
                return self.askForMeal()

        numberWord = self.nlp.getNumber(item)

        if numberWord:
            item = item.replace(numberWord, "").strip()
            
        quantity = self.nlp.getInteger(numberWord)

        if not quantity:
            if "couple" in item:
                quantity = 2
                item = item.replace("couple", "").strip()
            elif " a " in item:
                quantity = 1
                item = item.replace(" a", "").strip()
        
        
        meals = self.menu.findMeal(item)

        if len(meals) > 1:
            mealNames = [meal.getMealName() for meal in meals]

            new = self.waiter.listen(f"Please choose between: {mealNames.join(", ")}")
            chosenMealNames = self.getOptions(new, meals)
            chosenMeals = [meal for meal in meals if meal.getMeanName() in chosenMealNames]
            return chosenMeals[0], quantity


        elif len(meals) == 0:
            self.waiter.say(f"Could not find {item} on the menu")
            return self.askForMeal()
        else:
            return meals[0], quantity

    def askForQuantity(self) -> int:
        """Ask the user for the quantity of the meal they would like to order"""
        answer = self.waiter.listen("How many would you like?")
        numberWord = self.nlp.getNumber(answer)
        quantity = self.nlp.getInteger(numberWord)

        if quantity:
            return quantity
        
        # words = answer.split(" ")
        # for word in words:
        #     try:
        #         if int(word):
        #             return int(word)
        #     except ValueError:
        #         pass

        self.waiter.say(f"Sorry, I could not understand the quantity. Please try again.")
        return self.askForQuantity()
        


    def orderFood(self):
        """Create an order for the customer with at least ."""
        self.waiter.say(f"Prego, {self.customer.getFirstName()}. Let's order some food. ")
        order = Order(self.customer.getCustomerId())

        self.menu.display() #TODO check if we wanna to this
        while True:            
            meal, quantity = self.askForMeal()
            # check if they want to exit
            if meal is None:
                break
            
            if meal:
                if not quantity:
                    quantity = self.askForQuantity()

                orderItem = OrderItem(mealId=meal.getMealId(), quantity=quantity)
                mealName = meal.getMealName
                if quantity > 1:
                    mealName += "s"
                self.waiter.say(f"Ok, {quantity} {meal.getMealName()} added to your order.")

                order.addItem(orderItem)

                if order.getItemAmount() >= 3:
                    self.waiter.say(f"Would you like to order anything else?")

                    choice = self.getUserConfirmation()
                    if choice == "no":
                        Order.display()
                        choice = self.getUserConfirmation("Is this correct?")
                        if choice == "yes":
                            break
            
            else:
                self.waiter.say(f"Sorry, I could not find that item in the menu. Please try again.")
        

        id = order.save()
        if id:
            self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering at {self.getCafeName()} today. Your order number is {id}.") # getCafeName() function
            order.display()
        else:
            self.waiter.say(f"Sorry, {self.customer.getFirstName()}, I could not process your order. Please try again.")





    def run(self):
        """Run the chatbot"""
        # get the customer
        if not self.isPastCustomer() or not self.getCustomer():
            self.createCustomer()

        # LOOP - 1) Order? 2) View Menu 3) Order History 4) Leave/Exit
        running = True
        while running:

            choice = self.getRequest()
            print(choice)

            if choice in self.exitRequest:
                self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering at {self.getCafeName()} today. Bye bye")
                running = False

            elif choice in self.historyRequest:
                self.displayOrderHistory()
            elif choice in self.menuRequest:
                self.displayMenu()
            elif choice in self.orderRequest:
                self.orderFood()
            elif choice in self.dieRequest:
                self.waiter.say(f"KYS")
                running = False

def main():
    italiabot = Chatbot()

    italiabot.run()


# if __name__ == "__main__":
main()
