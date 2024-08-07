from SPXCafe import SPXCafe

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

    def setCustomer(self, userName=None, customerId=None):
        """Set the customer data from the database"""
        retcode = False
        if self.getCustomerId():
            sql = f"SELECT firstName, lastName, userName FROM customers WHERE customerId = {self.getCustomerId()}"
            customerData = self.dbGetData(sql)
            for customer in customerData:
                self.setFirstName(customer['firstName'])
                self.setLastName(customer['lastName'])
                self.setUserName(customer['userName'])
            return True
        elif self.getUserName():
            sql = f"SELECT customerId, firstName, lastName FROM customers WHERE userName = '{self.getUserName()}'"
            customerData = self.dbGetData(sql)
            for customer in customerData:
                self.setCustomerId(customer['customerId'])
                self.setFirstName(customer['firstName'])
                self.setLastName(customer['lastName'])
            return True

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
        retcode = False

        sql = ""
        sqlother = None

        if self.getCustomerId():
            sqlother = f"SELECT count(*) AS count FROM customers WHERE customerId = '{self.getCustomerId()}'"

        elif self.getUserName():
            sql = f"SELECT customerId, userName FROM customers WHERE userName = '{self.getUserName()}'"

        if sqlother:
            countData = self.dbGetData(sqlother)
            if countData:
                for countRecord in countData:
                    count = int(countRecord['count'])
                if count > 0:
                    retcode = True

        elif sql:
            customerData = self.dbGetData(sql)
            if customerData:
                for customer in customerData:
                    self.setCustomerId(customer['customerId'])
                    self.setUserName(customer['userName'])



                    retcode = True
        return retcode



    # def setCustomer(self, userName=None, customerId=None):
    #     pass. Not using anymore

    def save(self):
        """Save / update the customer to the database"""
        id = self.getCustomerId()
        if id: # If we have a customerId, then update the record
            # sql = "UPDATE customers SET firstName = %s, lastName = %s, userName = %s WHERE customerId = %s"
            # values = (self.getFirstName(), self.getLastName(), self.getUserName(), id)
            # self.dbPutData(sql, values) TODO Mabye implement

            sql = f"UPDATE customers SET firstName = '{self.getFirstName()}', lastName = '{self.getLastName()}', userName = '{self.getUserName()}' WHERE customerId = {id}"
            self.dbChangeData(sql)
        else: # If we don't have a customerId, then insert the record
            sql = f"INSERT INTO customers (firstName, lastName, userName) VALUES ('{self.getFirstName()}', '{self.getLastName()}', '{self.getUserName()}')"
            id = self.dbPutData(sql)
            self.setCustomerId(id)



def main():
    c = Customer("jbloggs")
    print(c.getFirstName())
    print(c.getLastName())
    print(c.getUserName())
    print(c.getCustomerId())

if __name__ == "__main__":
    main()
