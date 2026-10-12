from course import Course
from assignment import Assignment


class Weighted_Course(Course):
    def __init__(self, name, subject_code, number_code, hours,
                 assignments=None, final_grade=None,
                 grade_override=False, categories=None):

        super().__init__(
            name, subject_code, number_code, hours,
            assignments, final_grade, grade_override
        )

        self.categories = categories.copy() if categories is not None else {}

    def add_category(self, name, weight):
        self.categories[name] = weight

    def edit_category(self, name, new_name=None, new_weight=None):
        if new_weight is not None:
            self.categories[name] = new_weight

        if new_name is not None:
            self.categories[new_name] = self.categories.pop(name)

            for assignment in self.assignments:
                if assignment.category == name:
                    assignment.category = new_name

    def delete_category(self, name):
        del self.categories[name]

        self.assignments = [
            assignment for assignment in self.assignments
            if assignment.category != name
        ]

    def calculate_grade(self):
        if self.grade_override:
            return self.final_grade

        total_weight = 0
        weighted_grade = 0

        for category, weight in self.categories.items():
            earned_points = 0
            possible_points = 0

            for assignment in self.assignments:
                if assignment.category == category:
                    earned_points += assignment.earned_grade
                    possible_points += assignment.possible_grade

            if possible_points > 0:
                category_grade = earned_points / possible_points
                weighted_grade += category_grade * weight
                total_weight += weight

        if total_weight == 0:
            return None

        percent_grade = (weighted_grade / total_weight) * 100

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

        return Weighted_Course(
            data_dictionary.get("name"),
            data_dictionary.get("subject_code"),
            data_dictionary.get("number_code"),
            data_dictionary.get("hours"),
            assignments,
            data_dictionary.get("final_grade"),
            data_dictionary.get("grade_override", False),
            data_dictionary.get("categories", {})
        )

    def to_dict(self):
        data_dictionary = super().to_dict()
        data_dictionary["categories"] = self.categories.copy()
        return data_dictionary

    def __str__(self):
        return super().__str__()