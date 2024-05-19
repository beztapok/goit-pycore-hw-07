from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)

    @staticmethod
    def validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", День народження: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Контактне ім'я: {self.name.value}, Телефони: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming = []
        for record in self.values():
            if record.birthday and 0 <= (record.birthday.value.replace(year=today.year) - today).days <= 7:
                upcoming.append(record.name.value)
        return upcoming

# Демонстрація використання
if __name__ == "__main__":
    book = AddressBook()
    john = Record("John")
    john.add_phone("1234567890")
    john.add_birthday("15.05.1990")
    book.add_record(john)

    jane = Record("Jane")
    jane.add_phone("9876543210")
    jane.add_birthday("09.12.1995")
    book.add_record(jane)

    print(john)  # Виведення даних John
    print(book.get_upcoming_birthdays())  # Перевірка майбутніх днів народження

   
