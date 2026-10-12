import json
from pathlib import Path

from transcript import Transcript
from weighted_course import Weighted_Course


class Driver:
    def __init__(self):
        self.data_file = Path("data/transcript.json")
        self.transcript = self.load_transcript()

    # FILE PERSISTENCE

    def load_transcript(self):
        if not self.data_file.exists():
            return Transcript()

        with open(self.data_file, "r") as file:
            data = json.load(file)

        return Transcript.from_dict(data)

    def save_transcript(self):
        with open(self.data_file, "w") as file:
            json.dump(self.transcript.to_dict(), file, indent=4)

    # INPUT VALIDATION

    def get_integer(self, prompt, minimum=None):
        while True:
            value = input(prompt).strip()

            if not value.isdigit():
                print("Please enter a valid whole number.")
                continue

            number = int(value)

            if minimum is not None and number < minimum:
                print(f"Enter a number of at least {minimum}.")
                continue

            return number

    def get_number(self, prompt, minimum=None, maximum=None):
        while True:
            value = input(prompt).strip()

            if not value.replace(".", "", 1).isdigit():
                print("Please enter a valid number.")
                continue

            number = float(value)

            if minimum is not None and number < minimum:
                print(f"Enter a number of at least {minimum}.")
                continue

            if maximum is not None and number > maximum:
                print(f"Enter a number no greater than {maximum}.")
                continue

            return number

    def get_text(self, prompt):
        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("This field cannot be blank.")

    # OBJECT SELECTION

    def select_semester(self):
        if not self.transcript.semesters:
            print("No semesters available. Add a semester first.")
            return None

        print("\nSemesters:")

        for index, semester in enumerate(self.transcript.semesters, start=1):
            print(f"{index}. {semester}")

        while True:
            index = self.get_integer("Select semester (0 to cancel): ", 0)

            if index == 0:
                return None

            if index <= len(self.transcript.semesters):
                return self.transcript.get_semester(index - 1)

            print("Invalid semester selection.")

    def select_course(self, semester):
        if not semester.courses:
            print("No courses available. Add a course first.")
            return None

        print("\nCourses:")

        for index, course in enumerate(semester.courses, start=1):
            print(f"{index}. {course}")

        while True:
            index = self.get_integer("Select course (0 to cancel): ", 0)

            if index == 0:
                return None

            if index <= len(semester.courses):
                return semester.get_course(index - 1)

            print("Invalid course selection.")

    def select_course_from_transcript(self):
        semester = self.select_semester()

        if semester is None:
            return None

        return self.select_course(semester)

    # SEMESTER MANAGEMENT

    def add_semester(self):
        year = self.get_integer("Year: ", 1)

        while True:
            term = input("Term (Spring/Summer/Fall): ").strip().capitalize()

            if term in ("Spring", "Summer", "Fall"):
                break

            print("Please enter Spring, Summer, or Fall.")

        for semester in self.transcript.semesters:
            if semester.year == year and semester.term == term:
                print("That semester already exists.")
                return False

        self.transcript.add_semester(year, term)
        print("Semester added.")
        return True

    # COURSE MANAGEMENT

    def add_course(self):
        semester = self.select_semester()

        if semester is None:
            return False

        name = self.get_text("Course name: ")
        subject = self.get_text("Subject code: ").upper()
        number = self.get_text("Course number: ")
        hours = self.get_integer("Credit hours: ", 1)

        print("\n1. Points-based")
        print("2. Weighted")

        while True:
            course_type = input("Course type: ").strip()

            if course_type in ("1", "2"):
                break

            print("Choose 1 or 2.")

        if course_type == "1":
            semester.add_points_course(name, subject, number, hours)

        else:
            categories = {}

            print("\nEnter assignment categories and their weights.")
            print("Weights must total 100%.")

            while True:
                remaining = 100 - sum(categories.values())

                if abs(remaining) < 0.000001:
                    break

                category = input(
                    "Category name (blank to finish): "
                ).strip()

                if not category:
                    if not categories:
                        print("Add at least one category.")
                    else:
                        print("Category weights must total 100%.")
                    continue

                if category in categories:
                    print("That category already exists.")
                    continue

                weight = self.get_number(
                    f"{category} weight (%): ",
                    minimum=0.000001,
                    maximum=remaining
                )

                categories[category] = weight

            semester.add_weighted_course(
                name, subject, number, hours, categories
            )

        print("Course added.")
        return True

    # ASSIGNMENT MANAGEMENT

    def add_assignment(self):
        course = self.select_course_from_transcript()

        if course is None:
            return False

        title = self.get_text("Assignment title: ")

        if isinstance(course, Weighted_Course):
            categories = list(course.categories)

            print("\nCategories:")

            for index, category in enumerate(categories, start=1):
                print(f"{index}. {category}")

            while True:
                index = self.get_integer("Select category: ", 1)

                if index <= len(categories):
                    category = categories[index - 1]
                    break

                print("Invalid category selection.")

        else:
            category = input("Category (optional): ").strip()

        possible = self.get_number(
            "Possible points: ", minimum=0.000001
        )

        earned = self.get_number(
            "Earned points: ", minimum=0, maximum=possible
        )

        course.add_assignment(title, category, possible, earned)

        print("Assignment added.")
        return True

    # GRADE CALCULATIONS

    def view_course_grade(self):
        course = self.select_course_from_transcript()

        if course is None:
            return

        grade = course.calculate_grade()
        print(f"Course grade: {grade if grade is not None else 'N/A'}")

    def view_semester_gpa(self):
        semester = self.select_semester()

        if semester is None:
            return

        print(f"Semester GPA: {semester.calculate_gpa():.2f}")

    def view_overall_gpa(self):
        print(
            f"Overall GPA: "
            f"{self.transcript.calculate_overall_gpa():.2f}"
        )

    # MAIN MENU

    def run(self):
        while True:
            print("\nGRADEPOINT")
            print("1. Add Semester")
            print("2. Add Course")
            print("3. Add Assignment")
            print("4. View Course Grade")
            print("5. View Semester GPA")
            print("6. View Overall GPA")
            print("7. Exit")

            choice = input("Choose an option: ").strip()
            changed = False

            if choice == "1":
                changed = self.add_semester()

            elif choice == "2":
                changed = self.add_course()

            elif choice == "3":
                changed = self.add_assignment()

            elif choice == "4":
                self.view_course_grade()

            elif choice == "5":
                self.view_semester_gpa()

            elif choice == "6":
                self.view_overall_gpa()

            elif choice == "7":
                self.save_transcript()
                print("Data saved. Goodbye.")
                break

            else:
                print("Invalid option.")

            if changed:
                self.save_transcript()


if __name__ == "__main__":
    driver = Driver()
    driver.run()
