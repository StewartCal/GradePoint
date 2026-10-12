
# Iteration Report — GradePoint

## Implementation Plan

| Class | Method | Purpose | Must Have Story | Assigned To |
|---|---|---|---|---|
| Transcript | add_semester() | Create and store a semester | #1 | Elmo |
| Transcript | calculate_overall_gpa() | Calculate cumulative GPA | #6 | Elmo |
| Semester | add_points_course() | Add a points-based course | #2, #8 | Big Bird |
| Semester | add_weighted_course() | Add a weighted course | #2, #7 | Big Bird |
| Semester | calculate_gpa() | Calculate semester GPA | #5 | Big Bird |
| Course | add_assignment() | Create and store an assignment | #3 | Cookie Monster |
| Points_Course | calculate_grade() | Calculate grade using total points | #4, #8 | Cookie Monster |
| Weighted_Course | calculate_grade() | Calculate grade using category weights | #4, #7 | Oscar the Grouch |
| Driver | add_course() | Collect course information from the user | #2, #7, #8 | Oscar the Grouch |
| Driver | run() | Display the menu and process user choices | #1–8 | Elmo |

## Weekly Meeting

- **Day:** Wednesday
- **Time:** 4:00 PM
- **Location:** Library study room

## Revisions and Additions

- Big Bird:
    - **Change:** Added `Course_Credit` to represent completed courses separately from courses being tracked.
    - **Reason:** GPA calculations need course credit information without retaining every assignment.

- Elmo: 
    - **Change:** Added `save_transcript()` and `load_transcript()` to `Driver`.
    - **Reason:** Preserve entered information between program runs.
