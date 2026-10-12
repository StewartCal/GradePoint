class Course_Credit:
    def __init__(self, name, subject_code, number_code, hours, final_grade=None):
        self.name = name
        self.subject_code = subject_code
        self.number_code = number_code
        self.hours = hours
        self.final_grade = final_grade

    def calculate_quality_points(self):
        grade_points = {
            "A": 4.0,
            "B": 3.0,
            "C": 2.0,
            "D": 1.0,
            "F": 0.0
        }
        return grade_points.get(self.final_grade, 0.0) * self.hours

    def edit_credit(self, new_name=None, new_subject_code=None,
                    new_number_code=None, new_hours=None, new_final_grade=None):
        if new_name is not None:
            self.name = new_name
        if new_subject_code is not None:
            self.subject_code = new_subject_code
        if new_number_code is not None:
            self.number_code = new_number_code
        if new_hours is not None:
            self.hours = new_hours
        if new_final_grade is not None:
            self.final_grade = new_final_grade

    @staticmethod
    def from_dict(data_dictionary):
        return Course_Credit(
            data_dictionary.get("name"),
            data_dictionary.get("subject_code"),
            data_dictionary.get("number_code"),
            data_dictionary.get("hours"),
            data_dictionary.get("final_grade")
        )

    def to_dict(self):
        return {
            "name": self.name,
            "subject_code": self.subject_code,
            "number_code": self.number_code,
            "hours": self.hours,
            "final_grade": self.final_grade
        }

    def __str__(self):
        return f"{self.subject_code} {self.number_code} - {self.name}: {self.final_grade or 'No Grade'}"