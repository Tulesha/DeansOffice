from Documents.Document import Document


class ScheduleSession(Document):
    def __init__(self, ID, name, date):
        super().__init__(ID, name, date)
        self.subjects = []
        self.teachers = []
        self.groups = []
        self.dates = []

    def set_subject_teacher_group_date(self, subject, teacher, group, date):
        self.subjects.append(subject)
        self.teachers.append(teacher)
        self.groups.append(group)
        self.dates.append(date)

    def get_subject_teacher_group_date(self):
        return self.subjects, self.teachers, self.groups, self.dates
