#файл с загрузкой данных и анализом зависимостей

import pandas as pd #импортируем библиотеку для работы с таблицами
import matplotlib.pyplot as plt #импортируем библиотеку для визуализации данных для последующего построения диаграмм рассеивания

#загружаем данные и создаем список с нужными показателями
def load_student_data(): #функция для загрузки данных из файла
    file_name = "StudentPerformanceFactors.csv" #датасет уже в этой же папки, поэтому путь к нему - его имя
    df = pd.read_csv(file_name) #загружаем данные
    students = [] #создаем список, чтобы сохранять данные о студентах

    num_rows = len(df) #находим количество строк в таблице
    for i in range(num_rows):
        row = df.iloc[i] #проходимся по каждой строке, присваивая ей номер i

        student = {
            "ID": i + 1, #айди
            "Hours_Studied": row["Hours_Studied"], #часы, потраченные на учебу
            "Sleep_Hours": row["Sleep_Hours"], #часы, потраченные на сон
            "Attendance": row["Attendance"], #процент посещаемости
            "Exam_Score": row["Exam_Score"], #итоговый балл на экзамене
            "Previous_Scores": row["Previous_Scores"], #добавляем данные о предыдущих оценках
            "Tutoring_Sessions": row["Tutoring_Sessions"] #добавляем данные о занятиях с репетитором
        }
        #создаем список студентов: айди создаем сами, используя номер ряда + 1 (первый айди = 1)
        #остальные данные берем из таблицы
        students.append(student) #добавляем студента в список
    return students

#анализируем зависимости итоговой оценки и других показателей
def analyze_dependencies(students):
    df = pd.DataFrame(students) #превращаем список в датафрейм (таблицу)
    corr_study = df["Hours_Studied"].corr(df["Exam_Score"]) #рассчитываем корреляцию между часами учебы и баллом
    corr_sleep = df["Sleep_Hours"].corr(df["Exam_Score"]) #рассчитываем корреляцию между часами сна и баллом
    corr_attendance = df["Attendance"].corr(df["Exam_Score"]) #рассчитываем корреляцию между посещаемостью и баллом
    corr_previous = df["Previous_Scores"].corr(df["Exam_Score"]) #рассчитываем корреляцию между предыдущими баллами и итоговым
    corr_tutoring = df["Tutoring_Sessions"].corr(df["Exam_Score"]) #рассчитываем корреляцию между занятиями с репетитором и итоговым баллом
#корреляция - это число от -1 до 1, показывающее степень взаимосвязанности показателей, будем использовать этот показатель для составления отчета о зависимостях
#1 - идеальная прямая зависимость (чем больше X, тем больше Y)
#0 - нет зависимости
#-1 - идеальная обратная зависимость (чем больше X, тем меньше Y)

#в реальных данных редко встречаются "идеальные" показатели, поэтому присвоим следующие значения:
    def analysis(corr_value):
        if corr_value > 0.5:
            return "сильная прямая зависимость"
        elif corr_value > 0.2:
            return "умеренная прямая зависимость"
        elif corr_value < -0.5:
            return "сильная обратная зависимость"
        elif corr_value < -0.2:
            return "умеренная обратная зависимость"
        else:
            return "слабая зависимость"

#создаем отчет с полученными зависимостями
#каждую корреляцию округляем до тысячных для более структурированного анализа
#на основе полученного числа выдаем показатель, выраженный словами
#добавляем в отчет 2 новых показателя
    dependencies_report = {
        "study_effect": {
            "correlation": round(corr_study, 3),
            "interpretation": analysis(corr_study)
        },
        "sleep_effect": {
            "correlation": round(corr_sleep, 3),
            "interpretation": analysis(corr_sleep)
        },
        "attendance_effect": {
            "correlation": round(corr_attendance, 3),
            "interpretation": analysis(corr_attendance)
        },
        "previous_scores_effect": {
            "correlation": round(corr_previous, 3),
            "interpretation": analysis(corr_previous)
        },
        "tutoring_effect": {
            "correlation": round(corr_tutoring, 3),
            "interpretation": analysis(corr_tutoring)
        }
    }

    return dependencies_report

#добавляем функцию для создания диаграммы рассеивания
#создадим 6 графиков, и, так как сетка 2х3 вмещает в себя больше нужных 5 графиков, в 6 дополнительно проанализируем 2 "независимых" показателя - часы учебы и предыдущие баллы
#более детальный анализ позволит пользователю оценивать не только текущую ситуацию, но и учитывать предыдущий опыт


def create_scatter_plots(students):
    df = pd.DataFrame(students)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10)) #создаем сетку 2х3 размером 15х10 дюймов

#структура axes[х, у] описывает расположение графика: х строка у столбец, при этом нумерация начинается с 0
#например, axes[0, 0] - это левый верхний график (фактически 1 строка, 1 столбец)
#.scatter используется для создания точечного графика
#.set_xlabel используется для подписи оси х
#.set_уlabel используется для подписи оси у
#.set_title используется для создания заголовка графика
#зная это, создадим всю сетку графиков

    #диаграмма 1: часы учебы и итоговый балл
    axes[0, 0].scatter(df["Hours_Studied"], df["Exam_Score"])
    axes[0, 0].set_xlabel("Часы учебы")
    axes[0, 0].set_ylabel("Итоговый балл")
    axes[0, 0].set_title("Зависимость балла от часов учебы")

    #диаграмма 2: часы сна и итоговый балл
    axes[0, 1].scatter(df["Sleep_Hours"], df["Exam_Score"])
    axes[0, 1].set_xlabel("Часы сна")
    axes[0, 1].set_ylabel("Итоговый балл")
    axes[0, 1].set_title("Зависимость балла от часов сна")

    #диаграмма 3: посещаемость и итоговый балл
    axes[0, 2].scatter(df["Attendance"], df["Exam_Score"])
    axes[0, 2].set_xlabel("Посещаемость")
    axes[0, 2].set_ylabel("Итоговый балл")
    axes[0, 2].set_title("Зависимость балла от посещаемости")

    #диаграмма 4: предыдущие баллы и итоговый балл
    axes[1, 0].scatter(df["Previous_Scores"], df["Exam_Score"])
    axes[1, 0].set_xlabel("Предыдущие оценки")
    axes[1, 0].set_ylabel("Итоговый балл")
    axes[1, 0].set_title("Зависимость балла от предыдущих результатов")

    #диаграмма 5: занятия с репетитором и итоговый балл
    axes[1, 1].scatter(df["Tutoring_Sessions"], df["Exam_Score"])
    axes[1, 1].set_xlabel("Занятия с репетитором")
    axes[1, 1].set_ylabel("Итоговый балл")
    axes[1, 1].set_title("Зависимость балла от занятий с репетитором")

    #диаграмма 6: часы учебы и предыдущие баллы
    axes[1, 2].scatter(df["Hours_Studied"], df["Previous_Scores"])
    axes[1, 2].set_xlabel("Часы учебы")
    axes[1, 2].set_ylabel("Предыдущие баллы")
    axes[1, 2].set_title("Связь часов учебы и предыдущих баллов")

#сохраняем график

    plt.tight_layout()
    plot_file = 'scatter_plots.png'
    plt.savefig(plot_file)
    plt.close()

    return plot_file

#проведем более комплексный анализ влияния факторов на итоговый балл: возьмем пары факторов, чтобы найти наиболее значимую

def analyze_two_factors(students):
    df = pd.DataFrame(students)
    results = {} #создаем список для сохранения результатов анализа
    pairs_to_check = [
        ("Hours_Studied", "Sleep_Hours", "Учеба и Сон"),
        ("Attendance", "Previous_Scores", "Посещаемость и Предыдущие баллы"),
        ("Hours_Studied", "Tutoring_Sessions", "Учеба и Занятия с репетитором")
    ] #запишем пары, которые будем проверять
#еще раз определим значения корреляций
    def analysis(corr_value):
        if corr_value > 0.5:
            return "сильная прямая зависимость"
        elif corr_value > 0.2:
            return "умеренная прямая зависимость"
        elif corr_value < -0.5:
            return "сильная обратная зависимость"
        elif corr_value < -0.2:
            return "умеренная обратная зависимость"
        else:
            return "слабая зависимость"
    for factor1, factor2, pair_name in pairs_to_check:
        combined_value = (df[factor1] + df[factor2]) / 2 #считаем среднее двух факторов
        correlation = combined_value.corr(df["Exam_Score"]) #считаем корреляцию среднего и итогового балла
        results[pair_name] = {
            "correlation": round(correlation, 3),
            "interpretation": analysis(correlation)  # Используем уже готовую функцию
        } #сохраняем результат

        return results

#возвращаем результаты всей работы в одном словаре для следующего участника
def participant1_complete_work():
    students = load_student_data()
    dependencies = analyze_dependencies(students)
    scatter_file = create_scatter_plots(students) #создаем диаграммы рассеивания
    two_factors_analysis = analyze_two_factors(students)
    return {
        'students_data': students,
        'dependencies_analysis': dependencies,
        'scatter_plots_file': scatter_file, #добавляем диаграммы в return
        'two_factors': two_factors_analysis
    }

#выводим результаты этой части работы
#корреляцию выражаем в числовом и текстовом виде
if __name__ == "__main__":
    a = participant1_complete_work() #запускаем программу работы участника 1

    print(f"Студентов: {len(a['students_data'])}") #выводим общее количество студентов
    print(f"\nУчеба: {a['dependencies_analysis']['study_effect']['correlation']} ({a['dependencies_analysis']['study_effect']['interpretation']})") #зависимость между часами учебы и итоговым баллом
    print(f"Сон: {a['dependencies_analysis']['sleep_effect']['correlation']} ({a['dependencies_analysis']['sleep_effect']['interpretation']})") #зависимость между часами сна и итоговым баллом
    print(f"Посещаемость: {a['dependencies_analysis']['attendance_effect']['correlation']} ({a['dependencies_analysis']['attendance_effect']['interpretation']})") #зависимость между посещаемостью и итоговым баллом
    print(f"Предыдущие баллы: {a['dependencies_analysis']['previous_scores_effect']['correlation']} ({a['dependencies_analysis']['previous_scores_effect']['interpretation']})") #зависимость между предыдущим и итоговым баллом
    print(f"Занятия с репетитором: {a['dependencies_analysis']['tutoring_effect']['correlation']} ({a['dependencies_analysis']['tutoring_effect']['interpretation']})") #зависимость между занятиями с репетитором и итоговым баллом
    print("(Как сочетание факторов влияет на итоговый балл)")
    for pair_name, data in a['two_factors'].items():
        print(f"  {pair_name}: {data['correlation']} ({data['interpretation']})")
#сохраним отчет в текстовый файл analysis_report.txt
    with open('analysis_report.txt', 'w', encoding='utf-8') as file:
        file.write(f"Студентов: {len(a['students_data'])}\n")
        file.write(f"Учеба: {a['dependencies_analysis']['study_effect']['correlation']} ({a['dependencies_analysis']['study_effect']['interpretation']})\n")
        file.write(f"Сон: {a['dependencies_analysis']['sleep_effect']['correlation']} ({a['dependencies_analysis']['sleep_effect']['interpretation']})\n")
        file.write(f"Посещаемость: {a['dependencies_analysis']['attendance_effect']['correlation']} ({a['dependencies_analysis']['attendance_effect']['interpretation']})\n")
        file.write(f"Предыдущие баллы: {a['dependencies_analysis']['previous_scores_effect']['correlation']} ({a['dependencies_analysis']['previous_scores_effect']['interpretation']})\n")
        file.write(f"Занятия с репетитором: {a['dependencies_analysis']['tutoring_effect']['correlation']} ({a['dependencies_analysis']['tutoring_effect']['interpretation']})\n")
        file.write("\nАнализ пар факторов:")
        for pair_name, data in a['two_factors'].items():
            file.write(f" {pair_name}: {data['correlation']} ({data['interpretation']})")


