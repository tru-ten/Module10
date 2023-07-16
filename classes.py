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
        self.phones.append(phone)

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            print(f'Phone {phone.value} is not listed')

    def change_phone(self, old_phone, new_phone):
        try:
            index_phone = self.phones.index(old_phone)
            self.phones[index_phone] = new_phone
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
