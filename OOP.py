class SchoolMember():
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("Создан SchoolMember {}".format(self.name))

    def info(self):
        print('Name: {}, Age: {}'.format(self.name, self.age), end=', ')


class Teacher():
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print("Создан Teacher {}".format(self.name))

    def info(self):
        SchoolMember.info(self)
        print('Salary: {}'.format(self.salary))

class Student():
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print("Создан Teacher {}".format(self.name))
    
    def info(self):
        SchoolMember.info(self)
        print('Marks: {}'.format(', '.join(str(i) for i in self.marks)))

t = Teacher('Mary', 22, 45000)
s = Student('Ken', 15, (4,5,5))

t.info()
s.info()