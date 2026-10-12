class Assignment:
    def __init__(self, title, category, possible_grade, earned_grade):
        self.title = title
        self.category = category
        self.possible_grade = possible_grade
        self.earned_grade = earned_grade

    def calculate_percentage(self):
        if self.possible_grade == 0:
            return 0
        return (self.earned_grade / self.possible_grade) * 100

    def edit_assignment(self, new_title=None, new_category=None,
                        new_possible_grade=None, new_earned_grade=None):
        if new_title is not None:
            self.title = new_title
        if new_category is not None:
            self.category = new_category
        if new_possible_grade is not None:
            self.possible_grade = new_possible_grade
        if new_earned_grade is not None:
            self.earned_grade = new_earned_grade

    @staticmethod
    def from_dict(data_dictionary):
        return Assignment(
            data_dictionary.get("title"),
            data_dictionary.get("category"),
            data_dictionary.get("possible_grade"),
            data_dictionary.get("earned_grade")
        )

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "possible_grade": self.possible_grade,
            "earned_grade": self.earned_grade
        }

    def __str__(self):
        return f"{self.title} - {self.calculate_percentage():.2f}%"