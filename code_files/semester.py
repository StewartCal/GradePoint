from points_course import Points_Course
from weighted_course import Weighted_Course


class Semester:
    def __init__(self, term, year, courses=None):
        self.term = term
        self.year = year
        self.courses = courses if courses is not None else []

    def add_points_course(self, name, subject_code, number_code, hours):
        course = Points_Course(name, subject_code, number_code, hours)
        self.courses.append(course)
        return course

    def add_weighted_course(self, name, subject_code, number_code,
                            hours, categories=None):
        course = Weighted_Course(
            name, subject_code, number_code, hours,
            categories=categories
        )
        self.courses.append(course)
        return course

    def get_course(self, course_index):
        return self.courses[course_index]

    def calculate_gpa(self):
        total_quality_points = 0
        total_hours = 0

        for course in self.courses:
            grade = course.calculate_grade()

            if grade is None:
                continue

            credit = course.create_credit()
            total_quality_points += credit.calculate_quality_points()
            total_hours += credit.hours

        if total_hours == 0:
            return 0.0

        return total_quality_points / total_hours

    @staticmethod
    def from_dict(data_dictionary):
        courses = []

        for data in data_dictionary.get("points_courses", []):
            courses.append(Points_Course.from_dict(data))

        for data in data_dictionary.get("weighted_courses", []):
            courses.append(Weighted_Course.from_dict(data))

        return Semester(
            data_dictionary.get("term"),
            data_dictionary.get("year"),
            courses
        )

    def to_dict(self):
        points_courses = []
        weighted_courses = []

        for course in self.courses:
            if isinstance(course, Points_Course):
                points_courses.append(course.to_dict())
            elif isinstance(course, Weighted_Course):
                weighted_courses.append(course.to_dict())

        return {
            "term": self.term,
            "year": self.year,
            "points_courses": points_courses,
            "weighted_courses": weighted_courses
        }

    def __str__(self):
        return f"{self.term} {self.year}"