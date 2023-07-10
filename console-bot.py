contact_book = {}

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
            return 'Enter user name'
    return inner

def hello_user(args):
    return "How can I help you?"

def unknown_command(args):
    return "unknown_command"

def exit(args):
    return

@error_handler
def add_user(args):
    name, phone = args
    contact_book[name] = phone
    return f'User {name} added!'

@error_handler
def change_phone(args):
    name, phone = args
    old_phone = contact_book[name]
    contact_book[name] = phone
    return f'{name} now has a phone: {phone}\nOld number: {old_phone}'

def show_all(args):
    if len(contact_book)>0:
        result = ''
        for name, phone in contact_book.items():
            result += f'Name: {name} phone: {phone}\n'
        return result
    return 'Contact book is empty'

@error_handler
def show_phone(args):
    name = args[0]
    phone = contact_book[name]
    return f'Phone: {phone}'

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