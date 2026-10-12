from semester import Semester
from course_credit import Course_Credit


class Transcript:
    def __init__(self, semesters=None, credits=None):
        self.semesters = semesters if semesters is not None else []
        self.credits = credits if credits is not None else []

    def add_semester(self, year, term):
        semester = Semester(term, year)
        self.semesters.append(semester)
        return semester

    def get_semester(self, semester_index):
        return self.semesters[semester_index]

    def add_credit(self, name, subject_code, number_code, hours, final_grade):
        credit = Course_Credit(
            name, subject_code, number_code, hours, final_grade
        )
        self.credits.append(credit)
        return credit

    def calculate_overall_gpa(self):
        total_quality_points = 0
        total_hours = 0

        for credit in self.credits:
            if credit.final_grade is not None:
                total_quality_points += credit.calculate_quality_points()
                total_hours += credit.hours

        for semester in self.semesters:
            for course in semester.courses:
                grade = course.calculate_grade()

                if grade is not None:
                    credit = course.create_credit()
                    total_quality_points += credit.calculate_quality_points()
                    total_hours += credit.hours

        if total_hours == 0:
            return 0.0

        return total_quality_points / total_hours

    @staticmethod
    def from_dict(data_dictionary):
        semesters = []
        credits = []

        for data in data_dictionary.get("semesters", []):
            semesters.append(Semester.from_dict(data))

        for data in data_dictionary.get("credits", []):
            credits.append(Course_Credit.from_dict(data))

        return Transcript(semesters, credits)

    def to_dict(self):
        semesters = []
        credits = []

        for semester in self.semesters:
            semesters.append(semester.to_dict())

        for credit in self.credits:
            credits.append(credit.to_dict())

        return {
            "semesters": semesters,
            "credits": credits
        }

    def __str__(self):
        return (
            f"Transcript: {len(self.semesters)} semesters, "
            f"{len(self.credits)} completed credits"
        )