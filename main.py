from CDO.CDO import CDO
from CDO.CDO import FinancialWorker
from datetime import datetime
from CDO.CDO import Dispatcher
from CDO.CDO import EmployerPosition
from CDO.CDO import Teacher
from CDO.CDO import TeacherType

# Финансовый работник
financial_worker = FinancialWorker(123456, 'Колькина', 'Мария', 'Алексеевна', 'Финансовый работник')
financial_worker.start_working()

financial_worker.fix_payment(datetime(2020, 9, 1), datetime(2020, 10, 1))
financial_worker.assign_financial_order()
financial_worker.assign_scholarship()
#financial_worker.stop_working()

# # Диспетчер
# dispatcher = Dispatcher(123457, 'Пупкин', 'Михаил', 'Иванович', EmployerPosition.dispatcher)
# dispatcher.start_working()
# dispatcher.create_schedule_session('Лето', 2020)
# dispatcher.stop_working()
#
# # Учитель
# cdo = CDO()
# cdo.read_subjects_csv()
# subject = cdo.get_subject_by_name('Программирование')
#
# teacher = Teacher(123458, 'Повышев', 'Владислав', 'Вячеславович', EmployerPosition.teacher, subject,
#                   TeacherType.lecture)
# teacher.start_working()
# teacher.close_ratings()
# teacher.stop_working()
