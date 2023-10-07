records = {}


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown rec_id. Try another or use help."
    return inner


def func_normalize_phone(phone):
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
        return None


@user_error
def func_add(*args):
    rec_id = args[0]
    phone = args[1]
    new_phone = func_normalize_phone(phone)

    if rec_id.lower() in records.keys() and new_phone in records.values():
        return f"Record alredy exist"
    elif new_phone == None: 
        return f"Check the phone: {phone}. Wrong format."
     
    records[rec_id] = new_phone
    return f"Add record {rec_id = }, {new_phone = }"


@user_error
def func_change(*args):
    rec_id = args[0]
    new_phone = func_normalize_phone(args[1])
    rec = records[rec_id]
    if new_phone == None: 
        return f"Check the phone: {args[1]}. Wrong format."
    if rec:
        records[rec_id] = new_phone
        return f"Change record {rec_id = }, {new_phone = }"
    

@user_error    
def func_phone(*args):
    rec_id = args[0].lower()
    return f"Phone of {rec_id} is {records.get(rec_id)}"
    

def func_hello(*args):
    return f"How can I help you?"


def func_show_all(*args):
    if len(records)==0:
        return f"Your contacts list is empty"
    f_string_generator = lambda d: "\n".join([f"{rec_id}: {phone}" for rec_id, phone in d.items()])
    result = f_string_generator(records) 
    return result
    

def unknown(*args):
    return "Unknown command. Try again."


def func_good_bye(*args):
    print(f"Good bye!")
    exit()
        

FUNCTIONS = {"hello" : func_hello,
            "add" : func_add,
            "change" : func_change, 
            "phone" : func_phone,
            "show all" : func_show_all,
            "good bye" : func_good_bye, 
            "close" : func_good_bye, 
            "exit" : func_good_bye,
            "": func_good_bye}


def parser(text: str):
    for func in FUNCTIONS.keys():
        if text.startswith(func):
            return func, text[len(func):].strip().split()
    return unknown, []


def main():
    while True:
        user_input = input(">>>")
        func, data = parser(user_input.lower())
        current_func = FUNCTIONS.get(func)
        print(current_func(*data))
        
        
if __name__ == '__main__':
    main()