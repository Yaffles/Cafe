from SPXCafe import SPXCafe
from OrderItem import OrderItem
import Customer

class Order(SPXCafe):
    def __init__(self, customer=None, orderId=None, totalAmount=None, orderDate=None) -> None:
        ''' Constructor Method '''
        super().__init__()

        self.items: list [OrderItem] = []
        self.setTotalAmount(0)

        if orderId is not None:
            self.setOrderId(orderId)
            if self.existsDB():
                self.setOrderItems()

        elif customer is not None:
            self.setCustomer(customer)
            self.setOrderId(None)
            self.setTotalAmount(0)
            self.setOrderDate(None)



    def setOrderId(self, orderId):
        self.__orderId = orderId
    def getOrderId(self):
        return self.__orderId

    def setTotalAmount(self, totalAmount):
        self.__totalAmount = totalAmount
    def getTotalAmount(self):
        return self.__totalAmount
    def addTotalAmount(self, amount):
        self.__totalAmount += amount

    def setOrderDate(self, orderDate):
        self.__orderDate = orderDate
    def getOrderDate(self):
        return self.__orderDate

    def setCustomer(self, customer):
        if (isinstance(customer, Customer.Customer)):
            self.__customer = customer

    def getCustomer(self):
        return self.__customer

    def getItemAmount(self):
        """ returns the total number of items in the order"""
        return sum([item.getQuantity() for item in self.items])

    def addItem(self, meal=None, quantity=1, orderItemId=None, orderId=None,  price=None, mealName=None, mealId=None):
        """Add an OrderItem to the order"""
        item = OrderItem(meal=meal, quantity=quantity, orderItemId=orderItemId, orderId=orderId, price=price, mealName=mealName, mealId=mealId)

        self.addTotalAmount(item.getPrice() * item.getQuantity())
        item.setOrderId(self.getOrderId())

        for orderMeal in self.items:
            if item.getMealId() == orderMeal.getMealId():
                orderMeal.setQuantity(orderMeal.getQuantity() + item.getQuantity())
                return

        self.items.append(item)



    def save(self):
        """Save the order to the database if it does not exist and save items, returns success"""
        if not self.getOrderId() and self.getCustomer():
            sql = f"INSERT INTO orders (customerId, totalAmount) VALUES ({self.getCustomer().getCustomerId()}, {self.getTotalAmount()})"
            id = self.dbPutData(sql)
            if id:
                self.setOrderId(id)
                for item in self.items:
                    item.setOrderId(id)
                    item.save()
                return id
        return None

    def existsDB(self):
        """Check if the order exists in the database and set the order details"""
        retcode = False
        if self.getOrderId():
            sql = f"SELECT orderId, totalAmount, orderDate FROM orders WHERE orderId = {self.getOrderId()}"
            orderData = self.dbGetData(sql)
            if orderData:
                for order in orderData:
                    self.setOrderId(order['orderId'])
                    self.setOrderDate(order['orderDate'])
                    retcode = True
        return retcode

    def setOrderItems(self):
        """Get the order items from the database and set the order items"""
        sql = f"SELECT orderItemId FROM orderItems WHERE orderId = {self.getOrderId()}"
        orderItemData = self.dbGetData(sql)
        for orderItem in orderItemData:
            self.addItem(orderItemId=orderItem['orderItemId'])



    def display(self):
        """Display the order details"""
        if self.getOrderId():
            print(f"Order Number: {self.getOrderId()}")
            print(f"Order Date: {self.getOrderDate()}")

        for item in self.items:
            print(f"• {item}")

        print(f"Total Amount: ${self.getTotalAmount()}\n")

    def __str__(self):
        string = ""
        if self.getOrderId():
            string += f"Order Number: {self.getOrderId()}\n"
            string += f"Order Date: {self.getOrderDate()}\n"
        for item in self.items:
            string += f"• {item}\n"

        string += f"Total Amount: ${self.getTotalAmount()}\n"
        return string






if __name__ == "__main__":
    pass