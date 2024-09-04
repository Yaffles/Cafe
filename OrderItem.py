from SPXCafe import SPXCafe
from Meal import Meal

class OrderItem(SPXCafe):
    '''OrderItem class - holds information about an item in an order'''

    def __init__(self, meal=None, quantity=1, orderItemId=None, orderId=None,  price=None, mealName=None, mealId=None) -> None:
        ''' Constructor Method '''
        super().__init__()

        self.setOrderItemId(orderItemId)

        if orderItemId:
            if not self.existsDB():
                print(f"OrderItem with ID {orderItemId} does not exist in the database.")
        else:
            self.setOrderId(orderId)
            self.setQuantity(quantity)

            self.setPrice(price)
            self.setName(mealName)
            self.setMealId(mealId)

            if meal and isinstance(meal, Meal):
                self.setMealId(meal.getMealId())

                mealName = meal.getMealName()
                price = meal.getMealPrice()
                self.setName(mealName)
                self.setPrice(price)

    def setOrderItemId(self, orderItemId):
        self.__orderItemId = orderItemId
    def getOrderItemId(self):
        return self.__orderItemId

    def setOrderId(self, orderId):
        self.__orderId = orderId
    def getOrderId(self):
        return self.__orderId

    def setMealId(self, mealId):
        self.__mealId = mealId
    def getMealId(self):
        return self.__mealId

    def setQuantity(self, quantity):
        self.__quantity = quantity
    def getQuantity(self):
        return self.__quantity

    def setPrice(self, price):
        self.__price = price
    def getPrice(self):
        return self.__price

    def setName(self, mealName):
        self.__mealName = mealName
    def getName(self):
        return self.__mealName

    def existsDB(self):
        """Check if the orderItem exists in the database and set the details"""
        retcode = False
        if self.getOrderItemId():
            sql = f"SELECT orderItemId, orderId, mealId, quantity, price, name FROM orderItems WHERE orderItemId = {self.getOrderItemId()}"
            orderData = SPXCafe().dbGetData(sql)
            if orderData:
                item = orderData[0]
                self.setOrderId(item['orderId'])
                self.setMealId(item['mealId'])
                self.setQuantity(item['quantity'])
                self.setPrice(item['price'])
                self.setName(item['name']) # TODO Assuming 'name' is a column in your orderItems table
                retcode = True
        return retcode

    def save(self):
        '''Save the OrderItem to the database'''
        if not self.getOrderItemId() and self.getOrderId() and self.getMealId() and self.getQuantity() and self.getPrice() and self.getName():
            sql = f"INSERT INTO orderItems (orderId, mealId, quantity, price, name) VALUES ({self.getOrderId()}, {self.getMealId()}, {self.getQuantity()}, {self.getPrice()}, '{self.getName()}')"
            id = self.dbPutData(sql)
            if id:
                self.setOrderItemId(id)
                return True
        return False

    def display(self):
        '''Display the OrderItem details'''
        print(f"    Meal Name: {self.getName()}")
        print(f"    Quantity: {self.getQuantity()}")
        print(f"    Price: {self.getPrice()}")

    def __str__(self) -> str:
        string = f"{self.getQuantity()} {self.getName()} for ${self.getPrice()}"
        if self.__quantity > 1:
            string += " each"
        return string
