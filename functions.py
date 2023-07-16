from classes import AddressBook, Name, Phone, Record

contact_book = AddressBook()

def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Not enough parameters'
    return inner

def hello_user(args):
    return "How can I help you?"

def unknown_command(args):
    return "unknown_command"

def exit(args):
    return

@error_handler
def add_user(args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name, phone)
    contact_book.add_record(rec)
    return f'User {name.value} added!'

@error_handler
def change_phone(args):
    name = Name(args[0])
    phone = Phone(args[1])
    phones = list(map(lambda x: x.value, contact_book[name.value]))
    old_phone = Phone(phones)
    rec = Record(name, old_phone)
    rec.change_phone(old_phone, phone)
    contact_book.add_record(rec)
    return f'{name.value} now has a phone: {phone.value}\nOld number: {old_phone.value}'

def show_all(args):
    if len(contact_book)>0:
        result = ''
        for name, phones in contact_book.items():
            phone = list(map(lambda x: x.value, phones))
            result += f'Name: {name}, Phone: {phone}\n'
        return result
    return 'Contact book is empty'

@error_handler
def show_phone(args):
    name = Name(args[0])
    phones = list(map(lambda x: x.value, contact_book[name.value]))
    phone = Phone(phones)
    return f'Phone: {phone.value}'

HANDLERS = {
    'hello': hello_user,
    'add': add_user,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'exit': exit,
    'good bye': exit,
    'close': exit,
}

def parse_input(user_input):
    try:
        command, *args = user_input.split()
        command = command.lstrip()
        handler = HANDLERS[command.lower()]
    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
        handler = HANDLERS.get(command.lower(), unknown_command)
    except ValueError:
        handler = unknown_command
        args = None
    return handler, args
