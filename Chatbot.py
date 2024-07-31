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

    def __init__(self, cafeName="Italiabot", waiterName="Luigi"):
        ''' Constructor Method '''

        self.cafeName = cafeName
        self.waiter = Avatar(waiterName)
        self.waiter.say(f"Welcome to {self.cafeName}.")
        self.menu = Menu("Italia Forever Lunch")
        self.nlp = NLP()

        #  These are the keywords for each option and the corresponding response when choosing that option
        self.exitRequest =      {
                "keywords":      ["exit","leave","bye"],
                "response":      "leave us now"
        }
        self.historyRequest =   {
                "keywords":      ["history", "previous"],
                "response":      "see your previous orders"
        }
        self.menuRequest =      {
                "keywords":      ["menu", "course", "meal","choice","options"],
                "response":      "see the menu"
        }
        self.orderRequest =     {
                "keywords":      ["order", "buy","food"],
                "response":      "order some food"
        }
        self.dieRequest =     {
                "keywords":      ["die", "kill", "kym"],
                "response":      "kill your self"
        }

        self.mainOptions = self.exitRequest["keywords"] + self.historyRequest["keywords"] + self.menuRequest["keywords"] + self.orderRequest["keywords"] + self.dieRequest["keywords"]

        # self.exitRequest =      [["exit","leave","bye"],                            "leave us now"]
        # self.historyRequest =   [["history", "previous"],                           "see your previous orders"]
        # self.menuRequest =      [["menu", "course", "meal","choice","options"],     "see the menu"]
        # self.orderRequest =     [["order", "buy","food"],                           "order some food"]
        # self.dieRequest =     [["die", "kill", "kym"],                           "kill your self"]



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

            print(f"You have matched: {','.join(matches)} with confidence level {maxConfidence}% {len(matches)}")

            # if len(matches)>1:
            #     self.waiter.say(f"Sorry, I am not sure if you wanted {' or '.join(matches)}. Please try again.")
            #     options = matches
            #     matches = []
            #     maxConfidence = 0

        if maxConfidence < requiredConfidence:
            return None
        return matches[0] if len(matches)>0 else []

    def getUserConfirmation(self, choice=None):
        # Define multiple options for "yes" and "no"
        yes_options = ["yes", "yeah", "yup", "sure", "of course"]
        no_options = ["no", "nope", "nah", "not really"]
        # Combine all options into a single list
        options = yes_options + no_options
        # Use the getOptions method to get the user's choice
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
        inp = self.waiter.listen(f"Have you been to {self.cafeName} before?").strip().lower()
        choice = self.getUserConfirmation(inp)
        if choice == "yes":
            return True
        else:
            return False


    def getCustomer(self):
        '''Get a customer - using username typed in for accuracy '''

        # get user name - typed
        print("Italiabot")
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

        inp = self.waiter.listen("What is your name?", useSR=False)
        name = self.nlp.getNameByPartsOfSpeech(inp)
        # name = self.nlp.getNameByEntityType(inp)
        names = name.split(" ")
        firstName = names[0].title()
        lastName = names[1].title() if len(names)>1 else ""

        # self.waiter.say(f"Hello {names}. Welcome to Italiabot. How can I help you today?")
        


        # get username
        username = self.waiter.listen(f"Thank you {firstName}. Please choose a uesrname: ",useSR=False)
        self.customer = Customer(userName=username, firstName=firstName, lastName=lastName)
        self.customer.save()
    
        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}.  May I call your {self.customer.getFirstName()}?")

    def getRequest(self):
        response = None

        while not response:
            self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do? ")

            option = self.waiter.listen("Order food? See the menu? Look at your order history? or Exit?")

            choice = self.getOptions(option, self.mainOptions)

            if choice in self.exitRequest['keywords']:
                response = self.exitRequest['response']
            elif choice in self.historyRequest['keywords']:
                response = self.historyRequest['response']
            elif choice in self.menuRequest['keywords']:
                response = self.menuRequest['response']
            elif choice in self.orderRequest['keywords']:
                response = self.orderRequest['response']
            else:
                self.waiter.say(f"I am sorry, I don't understand your choice. You said: '{option}. Please try again.")

        self.waiter.say(f"Right, You chose to {response}.")
        return choice

    def displayOrderHistory(self):
        self.waiter.say(f"Ok, {self.customer.getFirstName()}. Let's show your previous orders. ")
        orders = Order.getOrdersByCustomer(self.customer.getCustomerId())
        for o in orders:
            o.display()

    def displayMenu(self):
        self.waiter.say(f"Alright, {self.customer.getFirstName()}. Let's see the menu. ")
        self.menu.display()

    def askForMeal(self):
        item = self.waiter.listen("What would you like to order?").strip().lower()
        meals = self.menu.findMeal(item)

        if len(meals) > 1:
            mealNames = [meal.getMealName() for meal in meals]


            new = self.waiter.listen(f"Please choose between: {mealNames.join(", ")}")
            chosenMealNames = self.getOptions(new, meals)
            chosenMeals = [meal for meal in meals if meal.getMeanName() in chosenMealNames]
            return chosenMeals[0]


        elif len(meals) == 0:
            self.waiter.say(f"Could not find {item} on the menu")
            return self.askForMeal()
        else:
            return meals[0]



    def orderFood(self):
        self.waiter.say(f"Prego, {self.customer.getFirstName()}. Let's order some food. ")
        order = Order(self.customer.getCustomerId())
        while True:
            self.menu.display()
            
            meal: Meal = self.askForMeal()
            if meal:
                orderItem = OrderItem(mealId=meal.getMealId())
                orderItem.display()
                order.addItem(orderItem)
                self.waiter.say(f"Would you like to order anything else?")
                choice = self.getUserConfirmation()
                if choice == "no":
                    break
            
            else:
                self.waiter.say(f"Sorry, I could not find that item in the menu. Please try again.")
        
        id = order.save()
        if id:
            self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering at {self.cafeName} today. Your order number is {id}.") # getCafeName() function
        else:
            self.waiter.say(f"Sorry, {self.customer.getFirstName()}, I could not process your order. Please try again.")





    def run(self):
        # get the customer
        if not self.isPastCustomer() or not self.getCustomer():
            self.createCustomer()

        # LOOP - 1) Order? 2) View Menu 3) Order History 4) Leave/Exit
        running = True
        while running:

            choice = self.getRequest()
            print(choice)

            if choice in self.exitRequest['keywords']:
                self.waiter.say(f"Thank you, {self.customer.getFirstName()}, for ordering with Italiabot today. Bye bye")
                running = False

            elif choice in self.historyRequest['keywords']:
                self.displayOrderHistory()
            elif choice in self.menuRequest['keywords']:
                self.displayMenu()
            elif choice in self.orderRequest['keywords']:
                self.orderFood()
            elif choice in self.dieRequest['keywords']:
                self.waiter.say(f"KYS")
                running = False

def main():
    print("main")
    italiabot = Chatbot()


    italiabot.run()


# if __name__ == "__main__":
main()
