from SPXCafe import SPXCafe
from Meal import Meal

class OrderItem(Meal):
    '''OrderItem class - holds information about an item in an order'''

    def __init__(self, orderItemId=None, orderId=None, mealId=None, quantity=1, price=None, mealName=None) -> None:
        ''' Constructor Method '''
        super().__init__(mealId=mealId, mealName=mealName, mealPrice=price, )

        self.setOrderItemId(orderItemId)
        self.setOrderId(orderId)
        self.setMealId(mealId)
        self.setQuantity(quantity)
        
        # self.setPrice(price)
        # self.setMealName(mealName)

        if mealId:
            meal = Meal(mealId)
            mealName = meal.getMealName()
            price = meal.getMealPrice()
            self.setMealName(mealName)
            self.setPrice(price)





    def setOrderItemId(self, orderItemId):
        self.__orderItemId = orderItemId
    def getOrderItemId(self):
        return self.__orderItemId
    
    def setOrderId(self, orderId):
        self.__orderId = orderId
    def getOrderId(self):
        return self.__orderId
    
    # def setMealId(self, mealId):
    #     self.__mealId = mealId
    # def getMealId(self):
    #     return self.__mealId
    
    def setQuantity(self, quantity):
        self.__quantity = quantity
    def getQuantity(self):
        return self.__quantity
    
    # def setPrice(self, price):
    #     self.__price = price
    # def getPrice(self):
    #     return self.__price
    
    # def setMealName(self, mealName):
    #     self.__mealName = mealName
    # def getMealName(self):
    #     return self.__mealName
    
    def save(self):
        '''Save the OrderItem to the database'''
        if not self.getOrderItemId() and self.getOrderId() and self.getMealId() and self.getQuantity() and self.getPrice():
            sql = f"INSERT INTO orderItems (orderId, mealId, quantity, price) VALUES ({self.getOrderId()}, {self.getMealId()}, {self.getQuantity()}, {self.getPrice()})"
            id = self.dbPutData(sql)
            if id:
                self.setOrderItemId(id)
                return True
        return False
    
    def display(self):
        '''Display the OrderItem details'''
        print(f"    Meal Name: {self.getMealName()}")
        print(f"    Quantity: {self.getQuantity()}")
        print(f"    Price: {self.getPrice()}")
