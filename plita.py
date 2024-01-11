import tkinter as tk
from tkinter import ttk


def processing_entries(entries: dict) -> dict:
    """функция для обработки полученных значений. Принимает словарь значений ввёденных пользователем и возвращает
    новый словарь со зачениями типа float и формулой для расчёта F."""

    values = {}  # создаем словарь для выходных значений

    for key, value in entries.items():  # перебираем словарь entries
        if key == 'F':
            values['F'] = value.get()
        else:
            values[key] = float(
                value.get().replace(',', '.'))  # приводим значения к типу float и записываем в словарь values

    return values


def search_more_values_for_F(values: dict) -> dict:
    """Функция для поиска и записи вспомогательных значений для послудующего поиска F. Формулы берутся из методички
    НИИЖБ по расчёту на продавливание. Принимает на вход словарь значений и дополняет его значениями из формул."""

    values['hox'] = values['h'] - values['zox']  # рабочая высота сечений плиты
    values['hoy'] = values['h'] - values['zoy']
    values['h0'] = 1 / 2 * (values['hox'] + values['hoy'])  # расчётная рабочая высота попер. сеч. плиты
    values['Aq'] = values['h0'] * (values['a1'] + values['b1'] + values['h0'])
    values['Fq'] = values['q'] * values['Aq']  # нормальная сила от разгр. действия реакт. давл. грунта
    values['Aq1'] = (values['a1'] + values['h0']) * (values['b1'] + values['h0'])  # площадь зоны плиты, ограниченная
    # расчётным контуром
    values['Fq1'] = values['q1'] * values['Aq1']  # нормальная сила от догруж. действия нагрузки от собств. веса

    return values


def search_F_value(values: dict) -> dict:
    """Функция для расчёта и добавления в словарь значений переменной F_value. Выбирает из трёх формул, предложенных
    пользователю. Принимает словарь значений и возращает его обновленную версию."""

    if values['F'] == 'N1+Fq1':
        values['F_value'] = values['N1'] + values['Fq1']
    elif values['F'] == 'N1-Fq+Fq1':
        values['F_value'] = values['N1'] - values['Fq'] + values['Fq1']
    elif values['F'] == 'N2-N1-Fq-Fq1':
        values['F_value'] = values['N2'] - values['N1'] - values['Fq'] - values['Fq1']

    return values


def start_working(entries: dict) -> dict:
    """Функция запускающая работу других функций от начала и до расчёта F_value. Принимает словарь значений
    полученных от пользователя для передачи в функцию processing_entries. На выходе получается полный словарь
    преобразованных и расчитанных значений вплоть до F_value."""

    values = processing_entries(entries)
    values = search_more_values_for_F(values)
    values = search_F_value(values)

    return values


def calculate(values):  # считаем по формулам

    # получаем данные из словаря значений
    q = values['q']
    a1 = values['a1']
    b1 = values['b1']
    zox = values['zox']
    zoy = values['zoy']
    N1 = values['N1']
    N2 = values['N2']
    q1 = values['q1']
    Asw = values['Asw']
    Sw = values['Sw']
    Rs = values['Rs']
    Rbt = values['Rbt']
    h = values['h']

    # переводим нужные данные
    Asw = Asw / (10 ** 4)  # в м2
    Rs = Rs * 1000  # в кн/м2
    Rbt = Rbt * 1000  # в кн/м2

    # прописываем и считаем формулы
    hox = h - zox
    hoy = h - zoy
    h0 = 1 / 2 * (hox + hoy)
    Aq = h0 * (a1 + b1 + h0)
    Fq = q * Aq
    Aq1 = (a1 + h0) * (b1 + h0)
    Fq1 = q1 * Aq1
    F_value = values['F_value']  # получаем F из словаря
    a = a1 + h0
    b = b1 + h0
    Ub = 2 * (a + b)
    Fb_ult = Rbt * Ub * h0

    results = {}  # создаем словарь для результатов

    # записываем полученные значения в словарь
    results["hox"] = hox

    results["hoy"] = hoy
    results["h0"] = h0
    results["Aq"] = Aq
    results["Fq"] = Fq
    results["Aq1"] = Aq1
    results["Fq1"] = Fq1
    results["F"] = F_value
    results["a"] = a
    results["b"] = b
    results["Ub"] = Ub
    results["Fb_ult"] = Fb_ult

    if Fb_ult != 0:  # если Fb_ult равно нулю, процентные соотношения не считаются, чтобы не вызвать ошибку деления на 0!
        F_Fb_ult = int(F_value / Fb_ult * 100)  # % соотношение F от Fb_ult

    if F_value <= Fb_ult:  # проверяем условие и если оно пройдено, прекращаем работу программы и дальнейший расчет.
        if Fb_ult != 0:
            results[
                "Fb_check"] = f"Несущая способность удовлетворительна, арматура не нужна. F это {F_Fb_ult}% от Fb_ult"
            return results
        else:
            results["Fb_check"] = "Несущая способность удовлетворительна, арматура не нужна."
            return results

    else:
        # если условия не пройдено - необходимо добавить арматуру, поэтому продолжаем расчеты
        results['Fb_check'] = 'Несущая способность неудовлетворительна, добавляем арматуру.'

        # добавляем формулы для арматуры
        Us = Ub
        Rsw = 0.8 * Rs
        if Rsw > 300000:  # Rsw не может быть больше 300000мПа
            Rsw = 300000
        qsw = (Rsw * Asw) / Sw
        F_sw_ult = 0.8 * qsw * Us

        try:
            F_sw_ult_Fb_ult = int(F_sw_ult / Fb_ult * 100)  # % соотношение F_sw_ult от Fb_ult
        except ZeroDivisionError:
            pass

        if F_sw_ult > Fb_ult:
            F_sw_ult = Fb_ult
            results["F_sw_ult_check"] = "F_sw_ult > Fb_ult, поэтому приравниваем F_sw_ult к Fb_ult"
        if F_sw_ult < Fb_ult:
            if Fb_ult != 0:  # если Fb_ult равно нулю, процентные соотношения не считаются, чтобы не вызвать ошибку деления на 0!
                results[
                    "F_sw_ult_check"] = f"F_sw_ult < Fb_ult, проверка ПРОЙДЕНА! F_sw_ult это {F_sw_ult_Fb_ult}% от Fb_ult "
            else:
                results["F_sw_ult_check"] = "F_sw_ult < Fb_ult, проверка ПРОЙДЕНА!"

                # добавляем еще результаты
        results["Us"] = Us
        results["Rsw"] = Rsw
        results["qsw"] = qsw
        results["F_sw_ult"] = F_sw_ult

        # делаем проверки и результат заносим в словарь результатов

        if F_sw_ult > 0.5 * Fb_ult:
            results["F_sw_ult_half_check"] = "F_sw_ult > 0.5Fb_ult, проверка ПРОЙДЕНА!"
            if F_value <= Fb_ult + F_sw_ult:
                results[
                    "F_strength_check"] = "F <= Fb_ult + F_sw_ult, условие прочности выполнено, прочность ОБЕСПЕЧЕНА!"
            else:
                results[
                    "F_strength_check"] = "F => Fb_ult + F_sw_ult, Условие прочности не выполнено. Прочность не обеспечена!"

        elif F_sw_ult < 0.5 * Fb_ult:
            results[
                "F_sw_ult_half_check"] = "F_sw_ult < 0.5Fb_ult, условие не выполняется, арматура не учитывается в расчете!"

            if F_value <= Fb_ult:
                results["F_strength_check"] = "F <= Fb_ult, условие прочности выполнено, прочность ОБЕСПЕЧЕНА!"
            else:
                results["F_strength_check"] = "F => Fb_ult, Условие прочности не выполнено. Прочность не обеспечена!"

    return results


def show_values():  # выводим результаты на экран приложения
    values = start_working(entries)  # получаем словарь значений
    print(values)
    results = calculate(values)  # считаем с помощью функции calculate
    print(results)
    global labels  # создаем глобальную переменную для хранения меток
    if labels:  # если список меток не пустой
        for label in labels:  # удаляем каждую метку с экрана
            label.destroy()
    labels = []  # обнуляем список меток
    for i, (key, value) in enumerate(results.items()):  # выводим на экран приложения пользователю
        if isinstance(value, (int, float)):  # проверяем, является ли значение числом
            value = round(value, 3)  # округляем значение до трех знаков после запятой
            unit = units[key]  # получаем единицу измерения из словаря units по ключу
            label = tk.Label(win, text=f"{key}: {value} {unit}")
        else:
            label = tk.Label(win, text=f"{value}", font=("Arial", 10, "bold"))
        label.grid(row=i + 1, column=3, sticky="w")
        labels.append(label)  # добавляем метку в список


win = tk.Tk()  # создаем окно приложения
##photo = tk.PhotoImage(file='fit.png') # пока не используем иконку приложения для простоты тестов на разных устройствах
##win.iconphoto(False, photo)
win.title('Расчёт плиты на продавливание')  # задаем название вверху окна
win.geometry('1100x600+250+50')  # задаем размер и адрес окна
win.resizable(False, False)  # запрещаем менять размер

# Создаем окна для ввода данных с клавиатуры
label_1 = tk.Label(win, text='Введите данные согласно указанным единицам: ', justify='center', font='bold')
label_1.grid(row=0, column=0, columnspan=2, stick='we')

label_2 = tk.Label(win, text='Введите нагрузку действующую на плиту q, кН/м2: ')
label_2.grid(row=1, column=0, stick='e')
q = tk.Entry(win)
q.grid(row=1, column=1)

label_3 = tk.Label(win, text='Первый размер стороны поперечного сечения колонны a1, м: ')
label_3.grid(row=2, column=0, stick='e')
a1 = tk.Entry(win)
a1.grid(row=2, column=1)

label_4 = tk.Label(win, text='Второй размер стороны поперечного сечения колонны b1, м: ')
label_4.grid(row=3, column=0, stick='e')
b1 = tk.Entry(win)
b1.grid(row=3, column=1)

label_5 = tk.Label(win, text='Защитный слой плиты для продольной арматуры zox, м: ')
label_5.grid(row=4, column=0, stick='e')
zox = tk.Entry(win)
zox.grid(row=4, column=1)

label_6 = tk.Label(win, text='Защитный слой плиты для продольной арматуры zoy, м: ')
label_6.grid(row=5, column=0, stick='e')
zoy = tk.Entry(win)
zoy.grid(row=5, column=1)

label_7 = tk.Label(win, text='Продольная сила действующая в колонне под плитой N1, кН: ')
label_7.grid(row=6, column=0, stick='e')
N1 = tk.Entry(win)
N1.grid(row=6, column=1)

label_8 = tk.Label(win, text='Продольная сила действующая в колонне над плитой N2, кН: ')
label_8.grid(row=7, column=0, stick='e')
N2 = tk.Entry(win)
N2.grid(row=7, column=1)

label_9 = tk.Label(win, text='Нагрузка от собственного веса плиты q1, кН/м2: ')
label_9.grid(row=8, column=0, stick='e')
q1 = tk.Entry(win)
q1.grid(row=8, column=1)

label_10 = tk.Label(win, text='Площадь сечения поперечной арматуры  Asw с шагом Sw, см2: ')
label_10.grid(row=9, column=0, stick='e')
Asw = tk.Entry(win)
Asw.grid(row=9, column=1)

label_11 = tk.Label(win, text='Шаг арматуры вдоль расчетного контура Sw, м: ')
label_11.grid(row=10, column=0, stick='e')
Sw = tk.Entry(win)
Sw.grid(row=10, column=1)

label_12 = tk.Label(win, text='Расчетное сопротивление арматуры Rs, мПа: ')
label_12.grid(row=11, column=0, stick='e')
Rs = tk.Entry(win)
Rs.grid(row=11, column=1)

label_13 = tk.Label(win, text='Расчетное сопротивление бетона Rbt, МПа: ')
label_13.grid(row=12, column=0, stick='e')
Rbt = tk.Entry(win)
Rbt.grid(row=12, column=1)

label_14 = tk.Label(win, text='Толщина плиты h, м (не менее 0.18м!): ')
label_14.grid(row=13, column=0, stick='e')
h = tk.Entry(win)
h.grid(row=13, column=1)

label_15 = tk.Label(win, text='Тип сопряжения перекрытия с колонной (формула), F = ')
label_15.grid(row=14, column=0, stick='e')
formuls = ('N1+Fq1', 'N1-Fq+Fq1',
           'N2-N1-Fq-Fq1')  # объявляем список с формулами, пользователь на экране должен выбрать одну из них
F = ttk.Combobox(win, values=formuls)
F.grid(row=14, column=1)

# Создаем словарь для значений
entries = {"q": q, "a1": a1, "b1": b1, "zox": zox, "zoy": zoy, "N1": N1, "N2": N2, "q1": q1, "Asw": Asw, "Sw": Sw,
           "Rs": Rs, "Rbt": Rbt, "h": h, "F": F}

labels = []  # создаем пустой список меток для последующего удаления старых

units = {"hox": "м", "hoy": "м", "h0": "м", "Aq": "м2", "Fq": "кН", "Aq1": "м2", "Fq1": "кН",
         "F": "кН", "a": "м", "b": "м", "Ub": "м", "Fb_ult": "кН", "Us": "м", "Rsw": "кПа", "qsw": "кН/м",
         "F_sw_ult": "кН"}

btn_start = tk.Button(win, text='Рассчитать', command=show_values, bg='orange', activebackground='orange',
                      bd=5)  # создаем кнопку "рассчитать" которая запускает расчет
btn_start.grid(row=15, column=0, columnspan=2, stick='we')

# задаем размеры столбцов
win.grid_columnconfigure(0, minsize=200)
win.grid_columnconfigure(0, minsize=100)

win.mainloop()
