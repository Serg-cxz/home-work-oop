class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}  # оценки за ДЗ (от Reviewer)

    def rate_lecture(self, lecturer, course, grade):
        # Проверяем: лектор ли это?
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'
        # Проверяем: курс есть у студента и у лектора?
        if course in self.courses_in_progress and course in lecturer.courses_attached:
            # Инициализируем словарь, если нужно
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # оценки от студентов за лекции


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))   # None → всё ок
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка → лектор не ведёт Java
print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка → опечатка: "С++" ≠ "C++"
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка → reviewer не лектор

print(lecturer.grades)  # {'Python': [7]}