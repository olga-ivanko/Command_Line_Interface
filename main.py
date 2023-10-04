import collections


Contact = collections.namedtuple('Contact', ['name', 'phone'])
CONTACTS_LIST = set()



#raction on hello   
def func_hello() -> None:
    print ("How can I help you?")
    next_func = define_command(user_input=input(">>> "))
    return next_func

#decorator for errors
def input_error(func):
    def inner():
        try:
            return func()
        except IndexError:
            print(f"Not enough params")
            func()
        
    return inner
        

def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    if len(new_phone) == 12:
        return "+" + new_phone
    elif len(new_phone) == 10:
        return "+38" + new_phone
    else: 
        print(f"please check the phone {phone}")
        func_add()
        return None


#adding new Contact to the contacts list
@input_error 
def func_add():
    contact_ = input("Enter name and phone: ").upper()
    name = contact_.split()[0] 
    phone = sanitize_phone_number(contact_.split()[1])
    new_contact = Contact(name, phone)
    if new_contact in CONTACTS_LIST:
        print(f"Contact {new_contact} already exist")
        return func_hello()
    else:
        CONTACTS_LIST.add(new_contact)
        print(f"New contact with name: {new_contact.name} and with number: {new_contact.phone} succesfully added")
        return get_input()



#changing the number of existing contact 
def func_change():
    input_name = input("Please enter the name of the contact for changing: ").upper()
    for i in filter(lambda x: x.name == input_name, CONTACTS_LIST):
       existing_contact = i
       new_phone = input("Please enter new phone: ")
       
    edited_contact = Contact(input_name, new_phone)
    CONTACTS_LIST.remove(existing_contact)
    CONTACTS_LIST.add(edited_contact)

    print(f"contact {edited_contact.name} was succesfully updated with the phone: {edited_contact.phone}")  

    return get_input()

#search phone in contacts list
def func_phone():
    input_name = input("Please enter the name for search: ").upper()
    for contact in  CONTACTS_LIST:
        if input_name == contact.name:
            print(contact.phone)
    return get_input()

#show all contacts saved in contacts list 
def func_show_all():
    for contact in CONTACTS_LIST:
        print(f"{contact.name} {contact.phone}")
    return get_input()

#reaction on exit key word
def func_good_bye():
    print("Good bye!")
    return None

#getting input as param for define_command
def get_input():
    user_input = input(">>>  ")
    return define_command(user_input) 

#the func finds the command from dict by key word
def define_command(user_input):
    FUNCTIONS = {"hello" : func_hello,
            "add" : func_add,
            "change" : func_change, 
            "phone" : func_phone,
            "show all" : func_show_all,
            "good bye" : func_good_bye, 
            "close" : func_good_bye, 
            "exit" : func_good_bye}
    
    if user_input.lower() in FUNCTIONS:
        run_func = FUNCTIONS.get(user_input.lower())()
        return run_func

    

        

def main() -> str:
    
    while True:
        user_input = input(">>> ").lower()        

        define_command(user_input)
        if user_input in ["", "exit", "."]:
            break
    return None

    


if __name__ == '__main__':

    main()