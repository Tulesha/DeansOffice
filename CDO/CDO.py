from abc import ABC

import pandas as pd
import math
import random
from datetime import datetime
from enum import Enum
from random import randrange
from datetime import timedelta

from Students.Budget import Budget
from Students.Contract import Contract

from Financial.BankCard import BankCard
from Financial.ReceiptOfPayment import ReceiptOfPayment

from Academic.Subject import Subject
from Academic.AcademicPerformance import AcademicPerformance
from Academic.Group import Group

from Documents.FinancialAidApplication import FinancialAidApplication
from Documents.FinancialAidApplication import Cause
from Documents.FinancialAidOrder import FinancialAidOrder
from Documents.ScholarshipOrder import ScholarshipOrder
from Documents.ScheduleSession import ScheduleSession


class CDO:
    def __init__(self):
        self.students = []
        self.documents = []
        self.employers = []
        self.performances = []
        self.groups = []
        self.subjects = []
        self.academic_performances = []

    def read_student_csv(self):
        print("Четение студентов из csv")
        self.students.clear()
        student_df = pd.read_csv(filepath_or_buffer='CSVs/Students.csv', sep=',')
        bank_df = pd.read_csv(filepath_or_buffer='CSVs/BankCards.csv', sep=',')
        payment_df = pd.read_csv(filepath_or_buffer='CSVs/PaymentReceipts.csv', sep=',')
        self.read_subjects_csv()
        for _, rows in student_df.iterrows():
            bank_card_row = bank_df[bank_df.ID == rows[6]]
            bank_card = BankCard(bank_card_row.ID.values[0],
                                 datetime.strptime(bank_card_row['shel life'].values[0], "%d.%m.%Y"),
                                 bank_card_row.amount.values[0])
            split_debtor_subjects = str(rows[13]).split(';')
            debtor_subjects = []
            if len(split_debtor_subjects) > 1:
                for subject_name in split_debtor_subjects:
                    debtor_subjects.append(self.get_subject_by_name(subject_name))
            elif split_debtor_subjects[0] != 'nan':
                debtor_subjects.append(self.get_subject_by_name(split_debtor_subjects[0]))
            if rows[7] == 1:
                self.students.append(
                    Budget(ID=rows[0], surname=rows[1], name=rows[2], patronymic=rows[3], phone=rows[4],
                           address=rows[5], bank_card=bank_card, scholarship=rows[8], debtor=bool(rows[12]),
                           debtor_subjects=debtor_subjects))
            else:
                split_payments = str(rows[9]).split(';')
                payments = []
                if len(split_payments) > 1:
                    for payment in split_payments:
                        row_payment = payment_df[payment_df['ID'] == float(payment)]
                        payments.append(ReceiptOfPayment(row_payment['ID'].values[0],
                                                         row_payment['bank name'].values[0],
                                                         datetime.strptime(row_payment['date of transaction'].values[0],
                                                                           "%d.%m.%Y")))
                elif not math.isnan(float(split_payments[0])):
                    row_payment = payment_df[payment_df['ID'] == float(split_payments[0])]
                    payments.append(ReceiptOfPayment(row_payment['ID'].values[0],
                                                     row_payment['bank name'].values[0],
                                                     datetime.strptime(row_payment['date of transaction'].values[0],
                                                                       "%d.%m.%Y")))
                self.students.append(
                    Contract(ID=rows[0], surname=rows[1], name=rows[2], patronymic=rows[3], phone=rows[4],
                             address=rows[5], bank_card=bank_card, receipts=payments, fix=bool(rows[10]),
                             debtor=bool(rows[12]), debtor_subjects=debtor_subjects))

    def read_employers_csv(self):
        print("Чтение работников из csv")
        self.employers.clear()
        self.read_subjects_csv()
        employers_df = pd.read_csv(filepath_or_buffer='CSVs/Employers.csv', sep=',')
        for _, row in employers_df.iterrows():
            if row[4] == 'Финансовый работник':
                self.employers.append(FinancialWorker(ID=row[0], surname=row[1],
                                                      name=row[2],
                                                      patronymic=row[3],
                                                      position=EmployerPosition.financial_worker))
            if row[4] == 'Диспетчер':
                self.employers.append(Dispatcher(ID=row[0], surname=row[1],
                                                 name=row[2],
                                                 patronymic=row[3],
                                                 position=EmployerPosition.dispatcher))
            if row[4] == 'Учитель':
                if row[6] == 'Лектор':
                    self.employers.append(Teacher(ID=row[0], surname=row[1], name=row[2], patronymic=row[3],
                                                  position=EmployerPosition.teacher,
                                                  subject=self.get_subject_by_name(row[5]),
                                                  teacher_type=TeacherType.lecture))
                else:
                    self.employers.append(Teacher(ID=row[0], surname=row[1], name=row[2], patronymic=row[3],
                                                  position=EmployerPosition.teacher,
                                                  subject=self.get_subject_by_name(row[5]),
                                                  teacher_type=TeacherType.practitioner))

    def read_subjects_csv(self):
        self.subjects.clear()
        subjects_df = pd.read_csv(filepath_or_buffer='CSVs/Subjects.csv', sep=',')
        for _, row in subjects_df.iterrows():
            self.subjects.append(Subject(name=row[0], faculty=row[1], lecture_hours=row[2], practical_hours=row[3],
                                         topics=str(row[4]).split(';'), type=row[5]))

    def read_academic_performance_csv(self):
        self.academic_performances.clear()
        academic_performance_df = pd.read_csv(filepath_or_buffer='CSVs/AcademicPerformance.csv', sep=',')
        self.read_subjects_csv()
        for _, row in academic_performance_df.iterrows():
            self.academic_performances.append(
                AcademicPerformance(student_id=row[0], subject=self.get_subject_by_name(row[1]), rating=row[2]))

    def read_groups_csv(self):
        self.groups.clear()
        groups_df = pd.read_csv(filepath_or_buffer='CSVs/Groups.csv', sep=',')
        self.read_student_csv()
        self.read_subjects_csv()
        for _, row in groups_df.iterrows():
            students_ids = str(row[1]).split(';')
            students = [self.get_student_by_id(int(student_id)) for student_id in students_ids]
            subjects_names = str(row[2]).split(';')
            subjects = [self.get_subject_by_name(subject_name) for subject_name in subjects_names]
            self.groups.append(
                Group(group_id=row[0], students=students, subjects=subjects, faculty=row[3], course=row[4]))

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student.ID == student_id:
                return student

    def set_debtor_for_student(self, student_id, subject):
        for student in self.students:
            if student.ID == student_id:
                student.debtor = True
                student.debtor_subjects.append(subject)

    def get_subject_by_name(self, subject_name):
        for subject in self.subjects:
            if subject.name == subject_name:
                return subject

    def get_budgets(self):
        budgets = []
        for student in self.students:
            if type(student) is Budget:
                budgets.append(student)
        return budgets

    def get_contracts(self):
        contracts = []
        for student in self.students:
            if type(student) is Contract:
                contracts.append(student)
        return contracts

    def get_academic_performance_student(self, student_id):
        student_performances = []
        for performance in self.academic_performances:
            if performance.student_id == student_id:
                student_performances.append(performance)
        return student_performances

    def get_academic_performances_by_subject(self, subject_name):
        students_performances = []
        for performance in self.academic_performances:
            if performance.subject.name == subject_name:
                students_performances.append(performance)
        return students_performances

    def get_lecture_by_subject(self, subject):
        for employer in self.employers:
            if type(employer) is Teacher:
                if employer.teacher_type == TeacherType.lecture and employer.subject.name == subject.name:
                    return employer

    def login(self, ID):
        for employer in self.employers:
            if employer.ID == ID:
                return True
        return False

    def update_students_bankCards_csv(self):
        print("Обновление файла студентов")
        student_df = pd.read_csv(filepath_or_buffer='CSVs/Students.csv', sep=',')
        bank_df = pd.read_csv(filepath_or_buffer='CSVs/BankCards.csv', sep=',')
        for student in self.students:
            student_df.loc[(student_df.ID == student.ID), 'surname'] = student.surname
            student_df.loc[(student_df.ID == student.ID), 'name'] = student.name
            student_df.loc[(student_df.ID == student.ID), 'patronymic'] = student.patronymic
            student_df.loc[(student_df.ID == student.ID), 'phone'] = student.phone
            student_df.loc[(student_df.ID == student.ID), 'address'] = student.address
            student_df.loc[(student_df.ID == student.ID), 'debtor'] = int(student.debtor)
            debtor_subjects_str = ""
            if len(student.debtor_subjects) > 1:
                for subject in student.debtor_subjects:
                    debtor_subjects_str = debtor_subjects_str + str(subject.name) + ';'
                debtor_subjects_str = debtor_subjects_str.rstrip(';')
            elif len(student.debtor_subjects) == 1:
                debtor_subjects_str = str(student.debtor_subjects[0].name)
            student_df.loc[(student_df.ID == student.ID), 'debtor_subjects'] = debtor_subjects_str
            bank_df.loc[(bank_df.ID == student.bank_card.number), 'amount'] = student.bank_card.amount
            if type(student) is Contract:
                payment_str = ""
                if len(student.get_receipts()) > 1:
                    for payment in student.get_receipts():
                        payment_str = payment_str + str(payment.transaction_number) + ';'
                    payment_str = payment_str.rstrip(';')
                else:
                    payment_str = str(student.get_receipts()[0].transaction_number)
                student_df.loc[(student_df.ID == student.ID), 'payment receipts ID'] = payment_str
                student_df.loc[(student_df.ID == student.ID), 'fix payment'] = int(student.fix)
            else:
                student_df.loc[(student_df.ID == student.ID), 'scholarship'] = student.scholarship
        student_df.to_csv('CSVs/Students.csv', sep=',', index=False)
        bank_df.to_csv('CSVs/BankCards.csv', sep=',', index=False)

    def update_receipts_payment_csv(self):
        print("Обновление файла чеков об оплате")
        payment_df = pd.read_csv(filepath_or_buffer='CSVs/PaymentReceipts.csv', sep=',')
        for student in self.students:
            if type(student) is Contract:
                for payment in student.get_receipts():
                    if payment_df[payment_df['ID'] == payment.transaction_number].empty:
                        payment_df.loc[payment_df.last_valid_index() + 1] = [payment.transaction_number,
                                                                             payment.bank_name,
                                                                             payment.date_of_transaction.strftime(
                                                                                 "%d.%m.%Y")]
        payment_df.to_csv('CSVs/PaymentReceipts.csv', sep=',', index=False)

    def update_documents_csv(self):
        print("Обновление файла документов")
        docs_df = pd.read_csv(filepath_or_buffer='CSVs/Documents.csv', sep=',')
        for document in self.documents:
            if docs_df[docs_df['ID'] == document.ID].empty:
                docs_df.loc[docs_df.last_valid_index() + 1] = [document.ID, document.name,
                                                               document.date.strftime("%d.%m.%Y"), int(document.filled),
                                                               int(document.confirmed), int(document.published)]
        docs_df.to_csv('CSVs/Documents.csv', sep=',', index=False)


class EmployerPosition(Enum):
    financial_worker = 1
    dispatcher = 2
    teacher = 3


class TeacherType(Enum):
    lecture = 1
    practitioner = 2


class Employer(ABC):
    def __init__(self, ID, surname, name, patronymic, position):
        self.ID = ID
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.position = position
        self.free = True
        self.working = False
        self.cdo = None

    def start_working(self):
        print("ДОБРОЕ УТРО")
        self.cdo = CDO()
        self.cdo.read_employers_csv()
        if self.cdo.login(self.ID):
            self.working = True
            print("Ауентефикация прошла успешно")
        else:
            self.working = False
            print("Неверный логин")

    def stop_working(self):
        self.working = False
        print("Я ПОШЁЛ СПАТЬ")

    def become_busy(self):
        self.free = False

    def become_free(self):
        self.free = True


class FinancialWorker(Employer):
    def __init__(self, ID, surname, name, patronymic, position):
        super().__init__(ID, surname, name, patronymic, position)

    def fix_payment(self, date_open, date_close):
        if self.working is True and self.free is True:
            print("Начало фиксации оплаты")
            self.become_busy()
            self.cdo.read_student_csv()
            contracts = self.cdo.get_contracts()
            for contract in contracts:
                if not contract.fix:
                    payments = contract.receipts
                    for payment in payments:
                        if date_open <= payment.date_of_transaction <= date_close:
                            contract.set_fix(True)
                if not contract.fix:
                    contract.add_receipts(ReceiptOfPayment(random.randint(100000, 999999), 'SPB', date_close))
                    contract.set_fix(True)
        self.cdo.update_students_bankCards_csv()
        self.cdo.update_receipts_payment_csv()
        self.become_free()
        print("Завершение фиксации оплаты")

    def assign_scholarship(self):
        if self.working is True and self.free is True:
            print("Начало создания приказа на стипендию")
            self.become_busy()
            order = ScholarshipOrder(random.randint(100000, 999999),
                                     'Приказ на стипендию' + datetime.now().strftime("%d-%m-%Y"), datetime.now())
            self.cdo.documents.append(order)
            self.cdo.read_student_csv()
            self.cdo.read_academic_performance_csv()
            budgets = self.cdo.get_budgets()
            for budget in budgets:
                performances = self.cdo.get_academic_performance_student(budget.ID)
                exams_ratings = [performance.rating for performance in performances if
                                 performance.subject.type == "Экзамен"]
                zahchets_ratings = [performance.rating for performance in performances if
                                    performance.subject.type == "Зачет"]
                if len([rating for rating in exams_ratings if rating < 74]) > 0 or len(
                        [rating for rating in zahchets_ratings if rating < 60]) > 0 or budget.debtor is True:
                    budget.set_scholarship(0)
                    order.set_budget_scholarship(budget, budget.get_scholarship())
                elif len([rating for rating in exams_ratings if rating > 90]) == len(exams_ratings) and len(
                        [rating for rating in zahchets_ratings if rating > 60]) == len(
                    zahchets_ratings) and budget.debtor is False:
                    budget.set_scholarship(4100)
                    order.set_budget_scholarship(budget, budget.get_scholarship())
                elif budget.debtor is False:
                    budget.set_scholarship(2000)
                    order.set_budget_scholarship(budget, budget.get_scholarship())
            order.set_filled(True)
            order.set_confirmed(True)
            order.set_published(True)
            budgets, scholarships = order.get_budgets_scholarships()

            for i in range(len(budgets)):
                budgets[i].bank_card.add_amount(scholarships[i])

            budgets_surname = [x.surname for x in budgets]
            order_df = pd.DataFrame(columns=['surname', 'amount'])
            order_df['surname'] = budgets_surname
            order_df['amount'] = scholarships
            order_df.to_csv('CSVs/ScholarshipOrder' + order.date.strftime("%d-%m-%Y") + '.csv', sep=',',
                            index=False)
            self.cdo.update_students_bankCards_csv()
            self.cdo.update_documents_csv()
            self.become_free()
            print("Завершение создания приказа на стипендию")

    def assign_financial_order(self):
        self.cdo.read_student_csv()
        self.cdo.students[0].set_financial_applications(
            FinancialAidApplication(462714, 'Финансовая помощь', datetime(2020, 9, 1), self.cdo.students[0].surname,
                                    Cause.disability))
        self.cdo.students[1].set_financial_applications(
            FinancialAidApplication(752658, 'Финансовая помощь', datetime(2020, 9, 1), self.cdo.students[1].surname,
                                    Cause.lostParent))
        self.cdo.students[2].set_financial_applications(
            FinancialAidApplication(837642, 'Финансовая помощь', datetime(2020, 9, 1), self.cdo.students[3].surname,
                                    Cause.financial_position))
        if self.working is True and self.free is True:
            print("Начало создания приказа финансовую помощь")
            self.become_busy()
            order = FinancialAidOrder(random.randint(100000, 999999),
                                      'Приказ материальной помощи ' + datetime.now().strftime("%d-%m-%Y"),
                                      datetime.now())
            self.cdo.documents.append(order)
            for student in self.cdo.students:
                if len(student.financial_applications) != 0:
                    for application in student.financial_applications:
                        if application.cause == Cause.disability:
                            order.set_student_amount(student, 10000)
                        if application.cause == Cause.lostParent:
                            order.set_student_amount(student, 10000)
                        if application.cause == Cause.financial_position:
                            order.set_student_amount(student, 2000)
            order.set_filled(True)
            order.set_confirmed(True)
            order.set_published(True)
            students, amounts = order.get_students_amounts()

            for i in range(len(students)):
                students[i].bank_card.add_amount(amounts[i])

            students_surname = [x.surname for x in students]
            order_df = pd.DataFrame(columns=['surname', 'amount'])
            order_df['surname'] = students_surname
            order_df['amount'] = amounts
            order_df.to_csv('CSVs/FinancialAssistanceOrder' + order.date.strftime("%d-%m-%Y") + '.csv', sep=',',
                            index=False)
            self.cdo.update_students_bankCards_csv()
            self.cdo.update_documents_csv()
            self.become_free()
            print("Завершение создания приказа финансовую помощь")


class Teacher(Employer):
    def __init__(self, ID, surname, name, patronymic, position, subject, teacher_type):
        super().__init__(ID, surname, name, patronymic, position)
        self.subject = subject
        self.teacher_type = teacher_type

    def close_ratings(self):
        if self.working is True and self.free is True:
            print("Закрытие оценок")
            self.become_busy()
            self.cdo.read_student_csv()
            self.cdo.read_academic_performance_csv()

            students_performances = self.cdo.get_academic_performances_by_subject(self.subject.name)

            for performance in students_performances:
                if performance.rating < 60:
                    self.cdo.set_debtor_for_student(performance.student_id, self.subject)
            self.cdo.update_students_bankCards_csv()
            self.become_free()
            print("Завершение закрытия оценок")


def get_random_date(start, end):
    delta = end - start
    int_delta = delta.days
    random_days = randrange(int_delta)
    return start + timedelta(days=random_days, hours=10)


class Dispatcher(Employer):
    def __init__(self, ID, surname, name, patronymic, position):
        super().__init__(ID, surname, name, patronymic, position)

    def create_schedule_session(self, season, year):
        if self.working is True and self.free is True:
            print("Начало составления сессии")
            self.become_busy()
            self.cdo.read_groups_csv()
            self.cdo.read_employers_csv()
            schedule_session = ScheduleSession(random.randint(100000, 999999),
                                               'Расписание сессии ' + season + ' ' + str(year) + 'год', datetime.now())
            self.cdo.documents.append(schedule_session)

            for group in self.cdo.groups:
                start_exam_date = None
                if season == "Зима":
                    start_exam_date = get_random_date(datetime(year, 1, 7),
                                                      datetime(year, 1, 31 - len(group.get_subjects())))
                elif season == "Лето":
                    start_exam_date = get_random_date(datetime(year, 6, 1),
                                                      datetime(year, 6, 31 - len(group.get_subjects())))
                date = start_exam_date
                for subject in group.get_subjects():
                    lecture = self.cdo.get_lecture_by_subject(subject)
                    date += timedelta(days=2)
                    schedule_session.set_subject_teacher_group_date(subject, lecture, group, date)
            schedule_session.set_filled(True)
            schedule_session.set_confirmed(True)
            schedule_session.set_published(True)

            subjects, teachers, groups, dates = schedule_session.get_subject_teacher_group_date()
            subjects_names = [subject.name for subject in subjects]
            teachers_names = [teacher.surname for teacher in teachers]
            groups_number = [group.group_id for group in groups]
            dates_string = [date.strftime("%d-%m-%Y %H:%M") for date in dates]

            schedule_session_df = pd.DataFrame(columns=['group', 'teacher_name', 'subject_name', 'date'])
            schedule_session_df['group'] = groups_number
            schedule_session_df['teacher_name'] = teachers_names
            schedule_session_df['subject_name'] = subjects_names
            schedule_session_df['date'] = dates_string

            schedule_session_df.to_csv(
                'CSVs/ScheduleSession' + season + str(year) + '.csv', sep=',',
                index=False)

            self.cdo.update_documents_csv()
            self.become_free()
            print("Завершение составления сессии")
