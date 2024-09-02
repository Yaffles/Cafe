from SPXCafe import SPXCafe
import Order


class Customer(SPXCafe):
    orders = []

    def __init__(self, userName=None, customerId=None, firstName=None, lastName=None):
        ''' Constructor Method. Allow either a username or a customerId to be passed in.'''
        super().__init__()

        self.setCustomerId(customerId)
        self.setUserName(userName)
        self.setFirstName(firstName)
        self.setLastName(lastName)


        # if userName is not None:
        #     self.setUserName(userName)
        #     self.setFirstName("Joe")
        #     self.setLastName("Bloggs")
            # self.existsDB()
        # elif customerId is not None:
        #     self.setCustomerId(customerId)

        if self.existsDB():
            if not self.setCustomer():
                print(f"Customer with ID {customerId} does not exist in the database.")

    def setCustomer(self):
        """Set the customer data from the database"""
        successful = False
        if self.getCustomerId():
            sql = f"SELECT firstName, lastName, userName FROM customers WHERE customerId = {self.getCustomerId()}"
            customerData = self.dbGetData(sql)
            for customer in customerData:
                self.setFirstName(customer['firstName'])
                self.setLastName(customer['lastName'])
                self.setUserName(customer['userName'])
            successful = True

        elif self.getUserName():
            sql = f"SELECT customerId, firstName, lastName FROM customers WHERE userName = '{self.getUserName()}'"
            customerData = self.dbGetData(sql)
            for customer in customerData:
                self.setCustomerId(customer['customerId'])
                self.setFirstName(customer['firstName'])
                self.setLastName(customer['lastName'])
            successful = True
        return successful

    def setFirstName(self, firstName=None):
        self.__firstName = firstName
    def setLastName(self, lastName=None):
        self.__lastName = lastName
    def setUserName(self, userName=None):
        self.__userName = userName
    def setCustomerId(self, customerId=None):
        self.__customerId = customerId

    def getFirstName(self):
        return self.__firstName
    def getLastName(self):
        return self.__lastName
    def getUserName(self):
        return self.__userName
    def getCustomerId(self):
        return self.__customerId


    def existsDB(self):
        '''Check if the customer exists in the database'''
        successful = False

        if self.__customerId:
            sql = f"SELECT COUNT(*) AS count FROM customers WHERE customerId = '{self.__customerId}'"
            countData = self.dbGetData(sql)
            if countData and int(countData[0]['count']) > 0:
                successful = True
        elif self.__userName:
            sql = f"SELECT customerId, userName FROM customers WHERE userName = '{self.__userName}'"
            customerData = self.dbGetData(sql)
            if customerData:
                self.__customerId = customerData[0]['customerId']
                self.__userName = customerData[0]['userName']
                successful = True
        return successful


    def save(self):
        """Save / update the customer to the database"""
        id = self.getCustomerId()
        if id:
            sql = f"UPDATE customers SET firstName = '{self.getFirstName()}', lastName = '{self.getLastName()}', userName = '{self.getUserName()}' WHERE customerId = {id}"
            self.dbChangeData(sql)

        else: # If we don't have a customerId, then insert the record
            sql = f"INSERT INTO customers (firstName, lastName, userName) VALUES ('{self.getFirstName()}', '{self.getLastName()}', '{self.getUserName()}')"
            id = self.dbPutData(sql)
            self.setCustomerId(id)

    def getOrders(self):
        """ Get's the past orders of the customer """
        orders = []
        sql = f"SELECT orderId, totalAmount, orderDate FROM orders WHERE customerId = {self.getCustomerId()}"
        orderData = self.dbGetData(sql)

        for order in orderData:
            orders.append(Order.Order(orderId=order['orderId']))
        return orders

    @classmethod
    def getAllCustomerIds(cls):
        """Retrieve all customer IDs from the database"""
        sql = "SELECT customerId FROM customers"
        data = SPXCafe().dbGetData(sql)

        ids = [record['customerId'] for record in data]
        return ids


def main():
    c = Customer("jbloggs")
    print(c.getFirstName())
    print(c.getLastName())
    print(c.getUserName())
    print(c.getCustomerId())

if __name__ == "__main__":
    main()
