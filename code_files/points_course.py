from course import Course
from assignment import Assignment


class Points_Course(Course):
    def __init__(self, name, subject_code, number_code, hours,
                 assignments=None, final_grade=None, grade_override=False):

        super().__init__(
            name, subject_code, number_code, hours,
            assignments, final_grade, grade_override
        )

        self.total_points = self.calculate_total_points()

    def add_assignment(self, title, category, possible_grade, earned_grade):
        super().add_assignment(title, category, possible_grade, earned_grade)
        self.total_points += possible_grade

    def edit_assignment(self, assignment_index, new_title=None,
                        new_category=None, new_possible_grade=None,
                        new_earned_grade=None):

        old_points = self.assignments[assignment_index].possible_grade

        super().edit_assignment(
            assignment_index, new_title, new_category,
            new_possible_grade, new_earned_grade
        )

        updated_points = self.assignments[assignment_index].possible_grade
        self.total_points += updated_points - old_points

    def delete_assignment(self, assignment_index):
        removed_points = self.assignments[assignment_index].possible_grade
        super().delete_assignment(assignment_index)
        self.total_points -= removed_points

    def calculate_grade(self):
        if self.grade_override:
            return self.final_grade

        if self.total_points == 0:
            return None

        earned_points = self.calculate_earned_points()
        percent_grade = (earned_points / self.total_points) * 100

        if percent_grade >= 90:
            self.final_grade = "A"
        elif percent_grade >= 80:
            self.final_grade = "B"
        elif percent_grade >= 70:
            self.final_grade = "C"
        elif percent_grade >= 60:
            self.final_grade = "D"
        else:
            self.final_grade = "F"

        return self.final_grade

    @staticmethod
    def from_dict(data_dictionary):
        assignments = []

        for assg in data_dictionary.get("assignments", []):
            assignments.append(Assignment.from_dict(assg))

        return Points_Course(
            data_dictionary.get("name"),
            data_dictionary.get("subject_code"),
            data_dictionary.get("number_code"),
            data_dictionary.get("hours"),
            assignments,
            data_dictionary.get("final_grade"),
            data_dictionary.get("grade_override", False)
        )

    def to_dict(self):
        data_dictionary = super().to_dict()
        data_dictionary["total_points"] = self.total_points
        return data_dictionary

    def __str__(self):
        return super().__str__()