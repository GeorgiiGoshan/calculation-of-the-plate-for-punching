import tkinter as tk
from tkinter import ttk

# объявляем список с формулами, пользователь на экране должен выбрать одну из них
formuls = ('N1+Fq1', 'N1-Fq+Fq1', 'N2-N1-Fq-Fq1')

# создаем пустой список меток для последующего удаления старых
labels = []

# создаем словарь единиц измерения переменных
units = {"hox": "м", "hoy": "м", "h0": "м", "Aq": "м2", "Fq": "кН", "Aq1": "м2", "Fq1": "кН",
         "F": "кН", "a": "м", "b": "м", "Ub": "м", "Fb_ult": "кН", "Us": "м", "Rsw": "кПа", "qsw": "кН/м",
         "F_sw_ult": "кН"}


def get_entry_values(entries):  # получаем значения введенные пользователем

    # создаем пустой словарь для значений
    values = {}
    # перебираем ключи словаря entries
    for key, entry in entries.items():
        # отдельно обрабатываем и сразу считаем F
        if key == "F":

            F_str = entry.get()  # получаем выбранную пользователем формулу

            # получаем значения нужные для рассчета формулы
            q = float(entries["q"].get().replace(",", "."))         # нагрузка действующая на плиту в пределах площади Aq
            a1 = float(entries["a1"].get().replace(",", "."))       # размеры стороны поперечного сечения колонны
            b1 = float(entries["b1"].get().replace(",", "."))
            zox = float(entries["zox"].get().replace(",", "."))     # защитный слой плиты для продольной и поперечной арматуры, расположенной в направлении взаимно перпендикулярных осей X и Y
            zoy = float(entries["zoy"].get().replace(",", "."))
            N1 = float(entries["N1"].get().replace(",", "."))       # продольные силы действующие в колоннах под и над плитой в поперечных сечениях у граней плиты
            N2 = float(entries["N2"].get().replace(",", "."))
            q1 = float(entries["q1"].get().replace(",", "."))       # нагрузка от собственного веса плиты
            Asw = float(entries["Asw"].get().replace(",", "."))     # площадь сечения поперечной арматуры с шагом Sw, расположенная в пределах расстояния 1/2*h0 по обе стороны контура # расчетного поперечного сечения плиты
            Sw = float(entries["Sw"].get().replace(",", "."))       # Шаг арматуры вдоль расчетного контура
            Rs = float(entries["Rs"].get().replace(",", "."))       # Расчетное сопротивление арматуры
            Rbt = float(entries["Rbt"].get().replace(",", "."))     # Расчетное сопротивление бетона
            h = float(entries["h"].get().replace(",", "."))         # Толщина плиты

            # прописываем формулы нужные для нахождения F
            hox = h - zox                   # рабочая высота сечений плиты для продольной арматуры, расположенной в направлении взаимно перпендикулярных осей X и Y
            hoy = h - zoy
            h0 = 1 / 2 * (hox + hoy)
            Aq = h0 * (a1 + b1 + h0)        # площадь зоны продавливания расположенная вокруг колонны на расстоянии 1/2*h0 от контура поперечного сечения колонны
            Fq = q * Aq                     #нормальная сила от разгружающего действия нагрузки на плиту в пределах зоны продавливания, ограниченной расчетным контуром
            Aq1 = (a1 + h0) * (b1 + h0)     # площадь зоны плиты, ограниченная расчетным контуром, расположенным вокруг колонн на расстоянии 1/2*h0 от контура поперечного сечения колонны
            Fq1 = q1 * Aq1                  # нормальная сила от разгружающего действия нагрузки, от собственного веса плиты между верхними и нижними колоннами, огранич расчетным контуром

            # Считаем саму формулу
            if F_str == "N1+Fq1":
                F_value = N1 + Fq1              # при сопряжении плиты с колонной, расположенной над плитой
            elif F_str == "N1-Fq+Fq1":
                F_value = N1 - Fq + Fq1         # при сопряжении фундаментной плиты с колонной
            elif F_str == "N2-N1-Fq-Fq1":
                F_value = N2 - N1 - Fq - Fq1    #сосредоточенная нормальная сила F при сопряжении плиты с колоннами, расположенными над и под плитой
            # добавляем к словарю
            values[key] = float(F_value)
        # для остальных данных просто преобразовывваем в число и записываем в словарь значений
        else:
            # получаем значение из поля ввода и преобразуем его в число
            values[key] = float(entry.get().replace(",", "."))
    # возвращаем словарь значений
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
    Asw = Asw / (10**4) # в м2
    Rs = Rs * 1000 # в кн/м2
    Rbt = Rbt * 1000 # в кн/м2

    # прописываем и считаем формулы
    hox = h - zox
    hoy = h - zoy
    h0 = 1 / 2 * (hox + hoy)
    Aq = h0 * (a1 + b1 + h0)
    Fq = q * Aq
    Aq1 = (a1 + h0) * (b1 + h0)
    Fq1 = q1 * Aq1
    F = values['F'] # получаем F из словаря
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
    results["F"] = F
    results["a"] = a
    results["b"] = b
    results["Ub"] = Ub
    results["Fb_ult"] = Fb_ult

    if Fb_ult != 0:  # если Fb_ult равно нулю, процентные соотношения не считаются, чтобы не вызвать ошибку деления на 0!
        F_Fb_ult = int(F / Fb_ult * 100)  # % соотношение F от Fb_ult

    if F <= Fb_ult:  # проверяем условие и если оно пройдено, прекращаем работу программы и дальнейший расчет.
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
    # добавляем формулы для арматуры
        Us = Ub
        Rsw  = 0.8 * Rs
        if Rsw > 300000:  # Rsw не может быть больше 300000мПа
            Rsw = 300000
        qsw = (Rsw * Asw) / Sw
        F_sw_ult = 0.8 * qsw * Us

        F_sw_ult_Fb_ult = int(F_sw_ult / Fb_ult * 100)  # % соотношение F_sw_ult от Fb_ult

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
            if F <= Fb_ult + F_sw_ult:
                results[
                    "F_strength_check"] = "F <= Fb_ult + F_sw_ult, условие прочности выполнено, прочность ОБЕСПЕЧЕНА!"
            else:
                results[
                    "F_strength_check"] = "F => Fb_ult + F_sw_ult, Условие прочности не выполнено. Прочность не обеспечена!"

        elif F_sw_ult < 0.5 * Fb_ult:
            results[
                "F_sw_ult_half_check"] = "F_sw_ult < 0.5Fb_ult, условие не выполняется, арматура не учитывается в расчете!"

        if F <= Fb_ult:
            results["F_strength_check"] = "F <= Fb_ult , условие прочности выполнено, прочность ОБЕСПЕЧЕНА!"
        else:
            results["F_strength_check"] ="F => Fb_ult , Условие прочности не выполнено. Прочность не обеспечена!"

    # добавляем еще результаты
    results["Us"] = Us
    results["Rsw"] = Rsw
    results["qsw"] = qsw
    results["F_sw_ult"] = F_sw_ult

    return results


def show_values():  # выводим результаты на экран приложения
    values = get_entry_values(entries)  # получаем словарь значений
    ##    print(values) # выводим в консоль для проверки
    results = calculate(values)  # считаем с помощью функции calculate
    ##    print(results) # выводим в консоль для проверки
    global labels  # создаем глобальную переменную для хранения меток
    if labels:  # если список меток не пустой
        for label in labels:  # удаляем каждую метку с экрана
            label.destroy()
    labels = []  # обнуляем список меток
    for i, (key, value) in enumerate(results.items()):  # выводим на экран приложения пользователю
        if isinstance(value, (int, float)):  # проверяем, является ли значение числом
            value = round(value, 3)  # округляем значение до трех знаков после запятой
            unit = units[key]  # получаем единицу измерения из словаря units по ключу
            label = tk.Label(win, text = f"{key}: {value} {unit}")
        else:
            label = tk.Label(win, text = f"{value}", font=("Arial", 10, "bold"))
        label.grid(row=i + 1, column=3, sticky="w")
        labels.append(label)  # добавляем метку в список

def create_window():
    win = tk.Tk() # создаем окно приложения
    ##photo = tk.PhotoImage(file='fit.png') # пока не используем иконку приложения для простоты тестов на разных устройствах
    ##win.iconphoto(False, photo)
    win.title('Расчёт плиты на продавливание') # задаем название вверху окна
    width = 1100  # ширина окна в пикселях
    height = 600  # высота окна в пикселях
    x = 250  # координата x левого верхнего угла окна
    y = 50  # координата y левого верхнего угла окна
    win.geometry(f'{width}x{height}+{x}+{y}')  # задаем размер и адрес окна
    win.geometry('1100x600+250+50')  # задаем размер и адрес окна
    win.resizable(False, False)  # запрещаем менять размер
    # задаем размеры столбцов
    win.grid_columnconfigure(0, minsize=200)
    win.grid_columnconfigure(0, minsize=100)
    return win

win = create_window()

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
F = ttk.Combobox(win, values=formuls)
F.grid(row=14, column=1)

# Создаем словарь для значений
entries = {"q": q, "a1": a1, "b1": b1, "zox": zox, "zoy": zoy, "N1": N1, "N2": N2, "q1": q1, "Asw": Asw, "Sw": Sw,
           "Rs": Rs, "Rbt": Rbt, "h": h, "F": F}

btn_start = tk.Button(win, text = 'Рассчитать', command=show_values, bg='orange',activebackground='orange',bd=5) # создаем кнопку "рассчитать" которая запускает расчет
btn_start.grid(row=15, column=0, columnspan=2, stick='we')


win.mainloop()
