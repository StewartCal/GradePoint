from assignment import Assignment
from course_credit import Course_Credit


class Course:
    def __init__(self, name, subject_code, number_code, hours,
                 assignments=None, final_grade=None, grade_override=False):
        self.name = name
        self.subject_code = subject_code
        self.number_code = number_code
        self.hours = hours
        self.assignments = assignments if assignments is not None else []
        self.final_grade = final_grade
        self.grade_override = grade_override

    def add_assignment(self, title, category, possible_grade, earned_grade):
        assignment = Assignment(title, category, possible_grade, earned_grade)
        self.assignments.append(assignment)

    def edit_assignment(self, assignment_index, new_title=None,
                        new_category=None, new_possible_grade=None,
                        new_earned_grade=None):
        self.assignments[assignment_index].edit_assignment(
            new_title, new_category, new_possible_grade, new_earned_grade
        )

    def delete_assignment(self, assignment_index):
        self.assignments.pop(assignment_index)

    def override_final_grade(self, new_grade):
        self.final_grade = new_grade
        self.grade_override = True

    def create_credit(self):
        return Course_Credit(
            self.name, self.subject_code, self.number_code,
            self.hours, self.final_grade
        )

    def calculate_earned_points(self):
        earned = 0
        for assignment in self.assignments:
            earned += assignment.earned_grade
        return earned

    def calculate_total_points(self):
        total = 0
        for assignment in self.assignments:
            total += assignment.possible_grade
        return total

    def to_dict(self):
        assignments = []

        for assignment in self.assignments:
            assignments.append(assignment.to_dict())

        return {
            "name": self.name,
            "subject_code": self.subject_code,
            "number_code": self.number_code,
            "hours": self.hours,
            "assignments": assignments,
            "final_grade": self.final_grade,
            "grade_override": self.grade_override
        }

    def __str__(self):
        return (
            f"{self.subject_code} {self.number_code} - "
            f"{self.name}: {self.final_grade or 'No Grade'}"
        )