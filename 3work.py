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

    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
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

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._average_grade() == other._average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # оценки от студентов за лекции

    def _average_lecture_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
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

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._average_lecture_grade() == other._average_lecture_grade()


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


