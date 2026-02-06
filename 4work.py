class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка'
        if course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg = round(self._average_grade(), 1)
        courses_in_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished_courses = ', '.join(self.finished_courses) or 'Нет'
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {avg}\n'
            f'Курсы в процессе изучения: {courses_in_progress}\n'
            f'Завершенные курсы: {finished_courses}'
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() < other._average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_lecture_grade(self):
        all_grades = [g for grades in self.grades.values() for g in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        avg = round(self._average_lecture_grade(), 1)
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {avg}'
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_lecture_grade() < other._average_lecture_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# === ФУНКЦИИ ДЛЯ СРЕДНЕЙ ОЦЕНКИ ПО КУРСУ ===

def average_grade_for_course(students, course):
    all_grades = []
    for student in students:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0


def average_lecture_grade_for_course(lecturers, course):
    all_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            all_grades.extend(lecturer.grades[course])
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0



# Студенты
student1 = Student('Алиса', 'Смирнова', 'жен')
student1.courses_in_progress = ['Python', 'Git']
student1.finished_courses = ['Введение в программирование']

student2 = Student('Борис', 'Иванов', 'муж')
student2.courses_in_progress = ['Python', 'Java']
student2.finished_courses = ['Алгоритмы']

# Лекторы
lecturer1 = Lecturer('Елена', 'Петрова')
lecturer1.courses_attached = ['Python', 'Git']

lecturer2 = Lecturer('Михаил', 'Сидоров')
lecturer2.courses_attached = ['Python', 'Java']

# Эксперты
reviewer1 = Reviewer('Олег', 'Козлов')
reviewer1.courses_attached = ['Python', 'Git']

reviewer2 = Reviewer('Наталья', 'Волкова')
reviewer2.courses_attached = ['Python', 'Java']

# Выставление оценок студентам
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 8)

reviewer2.rate_hw(student2, 'Python', 7)
reviewer2.rate_hw(student2, 'Java', 8)

# Выставление оценок лекторам
student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Git', 9)
student1.rate_lecture(lecturer2, 'Python', 8)  # можно, т.к. студент1 учит Python

student2.rate_lecture(lecturer2, 'Python', 9)
student2.rate_lecture(lecturer2, 'Java', 10)
student2.rate_lecture(lecturer1, 'Python', 7)  # тоже можно

# Вывод информации
print("=== СТУДЕНТЫ ===")
print(student1)
print()
print(student2)

print("\n=== ЛЕКТОРЫ ===")
print(lecturer1)
print()
print(lecturer2)

print("\n=== ЭКСПЕРТЫ ===")
print(reviewer1)
print()
print(reviewer2)

# Сравнение
print(f"\nСтудент1 > Студент2? {student1 > student2}")
print(f"Лектор1 < Лектор2? {lecturer1 < lecturer2}")

# Средние оценки по курсам
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]

print(f"\nСредняя оценка за ДЗ по курсу 'Python': {average_grade_for_course(students_list, 'Python')}")
print(f"Средняя оценка за лекции по курсу 'Python': {average_lecture_grade_for_course(lecturers_list, 'Python')}")
