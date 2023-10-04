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
    def inner(*args):
        if func == func_add:
            try:
                return func(*args)
            except IndexError:
                print(f"Not enough params")
                func()
        else:    
            try:
                return func(*args)
            except IndexError:
                print(f"Not enough params")
                func_add()
            except UnboundLocalError:
                print(f"The contact for change was not found")
                get_input()
            except TypeError:
                if args == "":
                    func_good_bye()
                else:
                    print(f"Unknown command: {args[0]}. Try again")
                    get_input()
            except KeyError:
                pass
    return inner

#converting number in propper format
@input_error        
def sanitize_phone_number(phone, func):

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
        return func()



#adding new Contact to the contacts list
@input_error 
def func_add():
    contact_ = input("Enter name and phone: ").upper()
    if contact_ == "":
        func_good_bye()
    name = contact_.split()[0] 
    phone = sanitize_phone_number(contact_.split()[1], func_add)
    new_contact = Contact(name, phone)
    if new_contact in CONTACTS_LIST:
        print(f"Contact {new_contact} already exist")
        return get_input()
    else:
        CONTACTS_LIST.add(new_contact)
        print(f"New contact with name: {new_contact.name} and with number: {new_contact.phone} succesfully added")
        return get_input()



#changing the number of existing contact 
def func_change():
    if len(CONTACTS_LIST)!=0:
        input_name = input("Please enter the name of the contact for changing: ").upper().strip()

        for i in filter(lambda x: x.name == input_name, CONTACTS_LIST):
            existing_contact = i
        if existing_contact:
            new_phone = sanitize_phone_number(input("Please enter new phone: "), func_change) 
            if new_phone != None:
                edited_contact = Contact(input_name, new_phone)
                CONTACTS_LIST.remove(existing_contact)
                CONTACTS_LIST.add(edited_contact)
                print(f"contact {edited_contact.name} was succesfully updated with the phone: {edited_contact.phone}")
            else: 
                exit
        else: 
            print(f"contact {input_name} was not found")
    else: 
        print("You have no contacts in contacts list")

    return get_input()

#search phone in contacts list
def func_phone():
    if len(CONTACTS_LIST) == 0:
        print("You have no contacts in contacts list")
        return get_input()
    input_name = input("Please enter the name for search: ").upper().strip()
    for contact in filter(lambda x: x.name == input_name, CONTACTS_LIST):
        found_contact = contact
            
    if found_contact: 
        print(contact.phone)
    else:
        print(f"you have no contact with name {input_name}")
    return get_input()

#show all contacts saved in contacts list 
def func_show_all():
    if len(CONTACTS_LIST) == 0:
        print("You have no contacts in contacts list")
    for contact in CONTACTS_LIST:
        print(f"{contact.name} {contact.phone}")
    return get_input()

#reaction on exit key word
def func_good_bye():
    print("Good bye!")
    exit()


#getting input as param for define_command
@input_error
def get_input():
    user_input = input("Enter the command >>>  ")
    return define_command(user_input) 

#the func finds the command from dict by key word

@input_error
def define_command(user_input):

    if user_input == None:
        exit 

    FUNCTIONS = {"hello" : func_hello,
            "add" : func_add,
            "change" : func_change, 
            "phone" : func_phone,
            "show all" : func_show_all,
            "good bye" : func_good_bye, 
            "close" : func_good_bye, 
            "exit" : func_good_bye,
            "": func_good_bye}
    
    run_func = FUNCTIONS.get(user_input.lower())()
    return run_func

def main() -> None:
    
    while True:

        user_input = input("Enter the command >>> ").lower()
        define_command(user_input)
        if user_input == "":
            break

    return None

    


if __name__ == '__main__':

    main()