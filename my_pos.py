import time
import datetime

# item refers to food or drink items in menu
class item:
    gst = 0.09
    service_charge = 0.10

    def __init__(self,name, category, price, discount):
        self.name = name
        self.category = category
        self.price = price
        self.discount = discount / 100

    def __str__(self):
        return (f"Name = {self.name}\nType = {self.type}\nPrice = ${self.price:.2f}\nDiscount = {self.discount}%")

    def __repr__(self):
        return f"{self.name}"

# self.order is where the order for the table accumulates and will have duplicate items.
# self.order_count filters self.order and categorizes each unique item (Key) with the associated quantity (Value).
class table:
    def __init__(self, pax):
        self.pax = pax
        self.order = []
        self.order_count = {}


    def total_bill(self):
        cost = 0
        if len(self.order) != 0:
            for item in self.order:
                cost += item.price
            return cost
        else:
            return 0

class payment_method:
    def __init__(self, name, amount, number_of_transactions):
        self.name = name
        self.amount = amount
        self.number_of_transactions = number_of_transactions

#table objects
table1 = table(0)
table2 = table(0)
table3 = table(0)
table4 = table(0)
table5 = table(0)

#payment_method objects
master_card = payment_method("master_card", 0, 0)
visa = payment_method("visa", 0, 0)
american_express = payment_method("american_express", 0, 0)

#Key will be Category and value will be a list containing the item objects
menu = {}

tables = {
    1 : table1,
    2 : table2,
    3 : table3,
    4 : table4,
    5 : table5

}

#Key will be option number and value is payment_method object
payment = {
    1 : master_card,
    2 : visa,
    3 : american_express
}

# used to display interface for user to select an option (for display purpose)
main_interface = {
    1 : "menu",   # ---> will invoke display_menu function
    2 : "tables", # ---> will invoke table_page(), display_menu(), add_item() functions
    3 : "receipt", #---> will invoke display_receipt()
    4 : "close_sale", #---> will invoke close_sale()
    5 : "sales_report", #---> will invoke sales_report()
    6 : "create_item", #---> will invoke create_item()
    7 : "remove_item", #---> will invoke remove_item()
    8 : "quit"
}

#for display purpose
table_interface = {
    1 : "table_1",
    2 : "table_2",
    3 : "table_3",
    4 : "table_4",
    5 : "table_5"
}

#for display purpose
payment_interface = {
    1 : "master_card",
    2 : "visa",
    3 : "american_express"
}

# To print out the menu
def display_menu():
    time.sleep(1)
    print(f"\n{"MENU":-^20}\n")
    for key, value in menu.items():
        print(f"{key}:")
        for item in value:
            print(f"{item.name} ${item.price:.2f}")
        print()
    print("----END OF MENU----")
    time.sleep(1)

#To display receipt for a specific table
def display_receipt():
    table_number = table_page()
    time.sleep(1)
    while True:
        if len(tables[table_number].order) == 0:
            print(f"\nNo receipt yet for table {table_number}")
            time.sleep(1)
            break
        else:
            message = f"Receipt for table{table_number}"
            print("")
            for i in range(len(message)):
                print("-", end = "")
            print(f"\n{message}")
            for i in range(len(message)):
                print("-", end = "")
            print("")
            for key, value in (tables[table_number].order_count).items():
                print(f"{key.name} x {value} = ${(key.price * value):.2f}")
            subtotal = tables[table_number].total_bill()
            subtotal_sc = subtotal + (subtotal * item.service_charge)
            total = subtotal_sc + (subtotal_sc * item.gst)
            print(f"\nSubtotal: ${subtotal:.2f} ")
            print(f"\nTotal: ${total:.2f} (Inclusive of {item.gst * 100}% GST and {item.service_charge * 100}% Service Charge)")
            time.sleep(1)
            while True:
                option = input("\npress 'x' to return to main interface: ")
                if option.lower() != 'x':
                    print("Invalid input, try again")
                    continue
                else:
                    break
            break

# To update backend with table sales revenue details and reset table object parameters
def close_sale():
    table_number = table_page()
    while True:
        if len(tables[table_number].order) == 0:
            print(f"\nNo orders to close for table{table_number}")
            time.sleep(1)
            break
        else:
            print("")
            message = f"Receipt for table{table_number}:"
            for i in range(len(message)):
                print("-", end = "")
            print(f"\n{message}")
            for i in range(len(message)):
                print("-", end = "")
            print("")
            for key, value in (tables[table_number].order_count).items():
                print(f"{key.name} x {value} = ${(key.price * value):.2f}")
            subtotal = tables[table_number].total_bill()
            subtotal_sc = subtotal + (subtotal * item.service_charge)
            total = subtotal_sc + (subtotal_sc * item.gst)
            print(f"\nSubtotal: ${subtotal:.2f} ")
            print(f"\nTotal: ${total:.2f} (Inclusive of {item.gst * 100}% GST and {item.service_charge * 100}% Service Charge)")

            print("")
            for key, value in payment_interface.items():
                print(f"option {key} : {value}")
            valid_options = (1,2,3)
            while True:
                try:
                    option = input("Enter option number to continue: ")
                    option = int(option)
                    if option in valid_options:
                        break
                    else:
                        print("Invalid option")
                        continue
                except ValueError:
                    print("please enter an integer")
                    continue
            #calculate subtotal and total. Add total to amount attribute of payment method object
            subtotal = tables[table_number].total_bill()
            subtotal_sc = subtotal + (subtotal * item.service_charge)
            total = subtotal_sc + (subtotal_sc * item.gst)
            payment[option].amount += total
            payment[option].number_of_transactions += 1
            #reset table attributes
            tables[table_number].pax = 0
            (tables[table_number].order).clear()
            (tables[table_number].order_count).clear()

            print(f"\nPayment for table{table_number} closed successfully")
            time.sleep(1)
            break

#to print Sales revenue information based on sales that have been closed using close_sale() function
def sales_report():
    print("")
    time.sleep(1)
    message = "Sales Report"
    for i in range(20):
        print("-", end = "")
    print(f"\n|{message:^18}|")
    for i in range(20):
        print("-", end = "")

    time.sleep(1)
    print("")

    total_receipts = 0
    total_sales_revenue = 0
    for value in payment.values():
        total_receipts += value.number_of_transactions
        total_sales_revenue += value.amount

    now = datetime.datetime.now()
    now = now.strftime("Date Generated: %d-%m-%y, Time Generated: %H:%M:%S")

    print(now)
    print(f"\nTotal Number Of Receipts: {total_receipts}")
    print(f"Total Sales Revenue: ${total_sales_revenue:.2f}")
    time.sleep(1)

    print("\nRevenue by payment Method:")
    count = 1
    for value in payment.values():
        print(f"\t{count}.{value.name} : ${value.amount:.2f}")
        count += 1
    print("\nEnd of Sales Report")
    while True:
            option = input("\npress 'x' to return to main interface: ")
            if option.lower() != 'x':
                print("Invalid input, try again")
                continue
            else:
                break

# To check if a vlue is of type float
def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def create_item():
    while True:
        name = input("\nname of item: ")
        name = name.replace(" ", "_")
        category = input("item category: ")

        price = input("price ($): ")
        while isfloat(price) == False:      #using self defined isfloat() to check for float input
            price = input("price: ")
        price = float(price)

        discount = input("discount (%): ")
        while isfloat(discount) == False:  #using self defined isfloat() to check for float input
            discount = input("discount: ")
        discount = float(discount)

        name = item(name, category, price, discount)
        option = input("would you like to add this item to menu?: ")
        while True:
            if option.lower() == "yes":
                if menu.get(category) is not None:
                    menu.get(category).append(name)
                    time.sleep(1)
                    print("\nitem created successfully")
                    time.sleep(1)
                    break
                else:
                    menu.update({category : []})
                    menu.get(category).append(name)
                    time.sleep(1)
                    print(f"\ncategory {name.category} and {name.name} item created successfully")
                    time.sleep(1)
                    break
            elif option.lower() == 'no':
                print("item not added")
                time.sleep(1)
                break
            else:
                print("invalid input, try again")
                option = input("would you like to add this item to menu?: ")
                time.sleep(1)
                continue

        option = input("Do you want to add another item?: ")
        valid_options = ["yes", "no"]
        while option.lower() not in valid_options:
            print("invalid input, please try again")
            time.sleep(1)
            option = input("Do you want to add another item?: ")

        if option.lower() == "yes":
            continue
        elif option.lower() == "no":
            break

# To remove an item from the menu if it exists in the menu
def remove_item():
    while True:
        item_removed = False
        option = input("Enter name of item to be removed: ")
        option = option.replace(" ", "_")
        for key, value in menu.items():
            for item in value:
                if option == item.name:
                    value.remove(item)
                    print("\nitem deleted successfully")
                    if len(value) == 0:
                        menu.pop(key)
                    time.sleep(1)
                    item_removed = True
                    break
            if item_removed == True:
                break
        if item_removed == False:
            print("\nitem does not exist in Menu")

        answer = input("\nDo you want to remove more items? ")
        valid_answer = ["yes", "no"]
        while answer.lower() not in valid_answer:
            print("invalid input, please try again")
            time.sleep(1)
            answer = input("\nDo you want to remove more items? ")

        if answer.lower() == "yes":
            continue
        elif answer.lower() == "no":
            print("\nReturning to main interface")
            time.sleep(1)
            break

# To display the main interface and ask user to select an option
# Returns an integer (case 1 to 8) that corresponds to a set of instructions (function calls)
def main_page():
    print("")
    message = "Welcome to POS system"
    for i in range(len(message)):
        print("-", end = "")
    print("")
    print(message)
    for i in range(len(message)):
        print("-", end = "")

    print("")
    for key, value in main_interface.items():
        print(f"option {key} : {value.upper()}")
    option = input("\nEnter option number to continue: ")
    while option.isdigit() != True:
        print("Invalid option number, try again")
        option = input("\nEnter option number to continue: ")
    else:
        return int(option)

# To display the tables and ask user to select a table
# Returns an integer (key) that corresponds to a table_object (value) in the tables dictionary
def table_page():
    valid_table_numbers = list(range(1, len(table_interface) + 1))
    print("")
    message = "select a table below"
    for i in range(len(message)):
        print("-", end = "")
    print("")
    print(message)
    for i in range(len(message)):
        print("-", end = "")

    print("")
    for key, value in table_interface.items():
        print(f"option {key} : {value.upper()}")
    while True:
        try:
            option = input("\nEnter option number to continue: ")
            option = int(option)
            if option not in valid_table_numbers:
                print("invalid option number, try again")
                continue
            else:
                return option
        except ValueError:
            print("please enter an integer")
            continue

# If table is empty (no pax), ask for number of pax, display menu, ask user to key in order
# If table is occupied (pax != 0), display order history, display menu, ask user to key in order
def enter_table(number):
    message = f"Order History for Table{number}"

    if len(tables[number].order) != 0:
        print("")
        for i in range(len(message)):
            print("-", end = "")
        print(f"\n{message}")
        for i in range(len(message)):
            print("-", end = "")
        print("")
        for key, value in (tables[number].order_count).items():
            print(f"{key.name}, Quantity: {value}")
        print("")

    temp_list = []
    if tables[number].pax == 0:
        num = input(f"\nKey in number of pax for table{number}: ")
        while num.isdigit() == False:
            num = input(f"Key in number of pax for table{number}: ")
        tables[number].pax = int(num)

    display_menu()

    answer = input(f"please key in order for table{number}, press x to end: ")
    answer = answer.replace(" ", "_")
    while answer.lower() != 'x':
        item_exists = False
        for value in menu.values():
            for item in value:
                if item.name == answer:
                    item_exists = True
                    while True:
                        try:
                            quantity = input("Quantity: ")
                            quantity = int(quantity)
                            break
                        except ValueError:
                            print("invalid input")
                            continue
                    for i in range(quantity):
                        temp_list.append(item)
                    break
            if item_exists == True:
                break

        if item_exists == True:
            answer = input(f"please key in order for table{number}, press x to end: ")
            answer = answer.replace(" ", "_")
            continue
        elif item_exists == False:
            print("Invalid Item")
            answer = input(f"please key in order for table{number}, press x to end: ")
            answer = answer.replace(" ", "_")
            continue
    print("")

    unique_items = []
    item_count = {}
    for item in temp_list:
        if item not in unique_items:
            unique_items.append(item)
    for item in unique_items:
        item_count.update({item : temp_list.count(item)})

    print("Order Summary:")
    for key, value in item_count.items():
        print(f"{key.name}, quantity: {value}")

    if len(temp_list) != 0:
        answer = input("press 'c' to confirm, press 'v' to void: ")
        while True:
            if answer.lower() == 'c':
                for item in temp_list:
                    (tables[number].order).append(item)
                break
            elif answer.lower() == 'v':
                break
            else:
                print("Invalid input, try again")
                answer = input("press 'c' to confirm, press 'v' to void: ")
                continue

    for key, value in item_count.items():
        if (tables[number].order_count).get(key) is not None:
            (tables[number].order_count)[key] += item_count[key]
        else:
            tables[number].order_count.update({key : value})

# case statements use integer value returned from main_page() function call
def main():
    while True:
        option = main_page()
        match option:
            case 1 : display_menu()
            case 2 :
                table_number = table_page() #table_page() returns table number which is used as key in the tables dictionary to access the table object
                enter_table(table_number)
            case 3 : display_receipt()
            case 4 : close_sale()
            case 5 : sales_report()
            case 6 : create_item()
            case 7 : remove_item()
            case 8 :
                print("Exiting POS system programme")
                break
            case _ :
                print("Invalid option number, try again")

if __name__ == "__main__":
    main()


