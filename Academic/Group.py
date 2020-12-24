class Group:
    def __init__(self, group_id, students, subjects, faculty, course):
        self.group_id = group_id
        self.students = students
        self.subjects = subjects
        self.faculty = faculty
        self.course = course

    def get_subjects(self):
        return self.subjects
