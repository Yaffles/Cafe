from Database import Database
from SPXCafe import SPXCafe
from OrderItem import OrderItem

class Order(SPXCafe):
    def __init__(self, customerId=None, orderId=None, totalAmount=None, orderDate=None) -> None:
        ''' Constructor Method '''
        super().__init__()

        self.items: list [OrderItem] = []

        if orderId is not None:
            self.setOrderId(orderId)
            if self.existsDB():
                self.setOrderItems()
        
        elif customerId is not None:
            self.setCustomerId(customerId)
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
    
    def setCustomerId(self, customerId):
        self.__customerId = customerId
    def getCustomerId(self):
        return self.__customerId
    
    def addItem(self, item):
        if isinstance(item, OrderItem):
            self.addTotalAmount(item.getPrice() * item.getQuantity())
            item.setOrderId(self.getOrderId())

            for orderMeal in self.items:
                if item.getMealId() == orderMeal.getMealId():
                    orderMeal.setQuantity(orderMeal.getQuantity() + item.getQuantity())
                    return

            self.items.append(item)
            
            
    
    def save(self):
        """save the order to the database if it does not exist and save items, returns True if successful"""
        if not self.getOrderId() and self.getCustomerId():
            sql = f"INSERT INTO orders (customerId, totalAmount) VALUES ({self.getCustomerId()}, {self.getTotalAmount()})"
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
            orderData = SPXCafe().dbGetData(sql)
            if orderData:
                for order in orderData:
                    self.setOrderId(order['orderId'])
                    # self.setTotalAmount(order['totalAmount']) TODO I add in addItem instead
                    self.setOrderDate(order['orderDate'])
                    retcode = True
        return retcode

    def setOrderItems(self):
        """Get the order items from the database and set the order items"""
        sql = f"SELECT mealOrderId, mealId, quantity, orderId FROM orderItems WHERE orderId = {self.getOrderId()}"
        orderItemData = SPXCafe().dbGetData(sql)
        for orderItem in orderItemData:
            mealName = SPXCafe().dbGetData(f"SELECT mealName FROM meals WHERE mealId = {orderItem['mealId']}")[0]['mealName']

            self.addItem(OrderItem(orderItem['mealOrderId'], self.getOrderId(), orderItem['mealId'], orderItem['quantity'], 0, mealName))



    def display(self):
        print(f"Order ID: {self.getOrderId()}")
        print(f"Total Amount: {self.getTotalAmount()}")
        print(f"Order Date: {self.getOrderDate()}")
        print(f"Order Items: {len(self.items)}")
        for item in self.items:
            print(f"    {item.getQuantity()} {item.getMealName()} for ${item.getPrice()}")
            # item.display()
        print()
    
    
    
    @classmethod
    def getOrdersByCustomer(cls, customerId):
        orders = []
        sql = f"SELECT orderId, totalAmount, orderDate FROM orders WHERE customerId = {customerId}"
        orderData = SPXCafe().dbGetData(sql)

        for order in orderData:
            orders.append(Order(orderId=order['orderId']))
        return orders
    #print
    


if __name__ == "__main__":
    order = Order.getOrdersByCustomer(2)
    print(order)
    for o in order:
        o.display()

    order = Order(customerId=2)
    order.addItem(OrderItem(mealId=1, quantity=2, price=10))
    order.addItem(OrderItem(mealId=2, quantity=1, price=15))
    order.display()

    order.save()
    order.display()

