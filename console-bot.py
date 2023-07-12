from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value

class Name(Field):
    ...

class Phone(Field):
    ...

class Record:
    def __init__(self, name, phone=None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone.value)

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone.value)
        except:
            print(f'Phone {phone.value} is not listed')

    def change_phone(self, old_phone, new_phone):
        try:
            index_phone = self.phones.index(old_phone)
            self.phones.pop(index_phone)
            self.phones.insert(index_phone, new_phone)
        except ValueError:
            print(f'Phone {old_phone.value} is not listed')

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record.phones
    
    def delete_record(self, record):
        try:
            self.data.pop(record.name.value)
        except KeyError:
            print(f'Record {record} not found')

    def search_record(self, record):
        if record.name.value in self.data.keys():
            return 'Record found'

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
            result += f'Name: {name} phone: {phone}\n'
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

def main():
    while True:
        user_input = input('=> ')
        handler, args = parse_input(user_input)
        result = handler(args)
        if not result:
            print('Exit')
            break
        print(result)

if __name__ == "__main__":
    main()