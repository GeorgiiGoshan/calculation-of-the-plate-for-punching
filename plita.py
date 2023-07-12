import tkinter as tk
from tkinter import ttk

formuls = ('N1+Fq1','N1-Fq+Fq1','N2-N1-Fq-Fq1')

def get_entry_values(entries):     #получаем значения введенные пользователем

    values = {}
    for key, entry in entries.items():
        if key == "F":

            F_str = entry.get()
           
            q = float(entries["q"].get())
            a1 = float(entries["a1"].get())
            b1 = float(entries["b1"].get())
            zox = float(entries["zox"].get())
            zoy = float(entries["zoy"].get())
            N1 = float(entries["N1"].get())
            N2 = float(entries["N2"].get())
            q1 = float(entries["q1"].get())
            Asw = float(entries["Asw"].get())
            Sw = float(entries["Sw"].get())
            Rs = float(entries["Rs"].get())
            Rbt = float(entries["Rbt"].get())
            h = float(entries["h"].get())

            hox = h - zox
            hoy = h - zoy
            h0 = 1/2 * (hox + hoy)
            Aq = h0 * (a1 + b1 + h0)
            Fq = q*Aq
            Aq1 = (a1 + h0) * (b1 + h0)
            Fq1 = q1 * Aq1
            
            

            if F_str == "N1+Fq1":
                F_value = N1 + Fq1
            elif F_str == "N1-Fq+Fq1":
                F_value = N1 - Fq + Fq1
            elif F_str == "N2-N1-Fq-Fq1":
                F_value = N2 - N1 - Fq - Fq1
            values[key] = float(F_value)
        else:
            values[key] = float(entry.get()) # получаем значение из поля ввода и преобразуем его в число
    return values


def calculate(values): # считаем по формулам
    q = values['q']
    a1 = values['a1']
    b1 = values['b1']
    zox = values['zox']
    zoy = values['zoy']
    N1 = values['N1']
    N2 = values['N2']
    q1 = values['q1']
    Asw = values['Sw']
    Sw = values['Sw']
    Rs = values['Rs']
    Rbt = values['Rbt']
    h = values['h']

    Asw = Asw / (10**4) # в м2
    Rs = Rs * 1000 # в кн/м2
    Rbt = Rbt * 1000 # в кн/м2

    hox = h - zox
    hoy = h - zoy
    h0 = 1/2 * (hox + hoy)
    Aq = h0 * (a1 + b1 + h0)
    Fq = q * Aq
    Aq1 = (a1 + h0) * (b1 + h0)
    Fq1 = q1 * Aq1
    F = values['F']
    a = a1 + h0
    b = b1 + h0
    Ub = 2 * (a + b)
    Fb_ult = Rbt * Ub * h0

    results = {} #словарь для результатов

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
    

    if F <= Fb_ult:
        results["Fb_check"] = "Несущая способность удовлетворительна, арматура не нужна"
        return results

    results['Fb_check'] = 'Несущая способность неудовлетворительна, добавляем арматуру'
    Us = Ub
    Rsw  = 0.8 * Rs
    qsw = (Rsw * Asw) / Sw
    F_sw_ult = 0.8 * qsw * Us

    results["Us"] = Us
    results["Rsw"] = Rsw
    results["qsw"] = qsw
    results["F_sw_ult"] = F_sw_ult


    if F_sw_ult < Fb_ult:
        results["F_sw_ult_check"] = "F_sw_ult < Fb_ult, проверка пройдена"
    else:
        results["F_sw_ult_check"] = "F_sw_ult > Fb_ult, проверка не пройдена!"

    if F_sw_ult > 0.5 * Fb_ult:
        results["F_sw_ult_half_check"] = "F_sw_ult > 0.5Fb_ult, проверка пройдена"
    else:
        results["F_sw_ult_half_check"] = "F_sw_ult < 0.5Fb_ult, проверка не пройдена!"

    if F <= Fb_ult + F_sw_ult:
        results["F_strength_check"] = "F <= Fb_ult + F_sw_ult, условие прочности выполнено, прочность обеспечена"
    else:
        results["F_strength_check"] ="F => Fb_ult + F_sw_ult, Условие прочности не выполнено. Прочность не обеспечена!"




    return results


        
def show_values(): # выводим результаты на экран приложения
    values = get_entry_values(entries) # получаем словарь значений
    results = calculate(values)
    print(results)
    for i, (key, value) in enumerate(results.items()):
        label = tk.Label(win, text=f"{key}: {value}")
        label.grid(row=i+1, column=3, sticky="w")


win = tk.Tk()
##photo = tk.PhotoImage(file='fit.png')
##win.iconphoto(False, photo)
win.title('Расчёт плиты на продавливание')
win.geometry('1100x600+250+50') # задаем размер и адрес окна
win.resizable(False, False) # запрещаем менять размер

label_1 = tk.Label(win, text = 'Введите данные согласно указанным единицам: ',justify ='center',font='bold')
label_1.grid(row=0,column=0,columnspan=2,stick='we')

label_2 = tk.Label(win, text = 'Введите нагрузку действующую на плиту q, кН/м2: ')
label_2.grid(row=1,column=0,stick='e')
q = tk.Entry(win)
q.grid(row=1,column=1)

label_3 = tk.Label(win, text = 'Первый размер стороны поперечного сечения колонны a1, м: ')
label_3.grid(row=2,column=0,stick='e')
a1 = tk.Entry(win)
a1.grid(row=2,column=1)

label_4 = tk.Label(win, text = 'Второй размер стороны поперечного сечения колонны b1, м: ')
label_4.grid(row=3,column=0,stick='e')
b1 = tk.Entry(win)
b1.grid(row=3,column=1)

label_5 = tk.Label(win, text = 'Защитный слой плиты для продольной арматуры zox, м: ')
label_5.grid(row=4,column=0,stick='e')
zox = tk.Entry(win)
zox.grid(row=4,column=1)

label_6 = tk.Label(win, text = 'Защитный слой плиты для продольной арматуры zoy, м: ')
label_6.grid(row=5,column=0,stick='e')
zoy = tk.Entry(win)
zoy.grid(row=5,column=1)

label_7 = tk.Label(win, text = 'Продольная сила действующая в колонне под плитой N1, кН: ')
label_7.grid(row=6,column=0,stick='e')
N1 = tk.Entry(win)
N1.grid(row=6,column=1)

label_8 = tk.Label(win, text = 'Продольная сила действующая в колонне над плитой N2, кН: ')
label_8.grid(row=7,column=0,stick='e')
N2 = tk.Entry(win)
N2.grid(row=7,column=1)

label_9 = tk.Label(win, text = 'Нагрузка от собственного веса плиты q1, кН/м2: ')
label_9.grid(row=8,column=0,stick='e')
q1 = tk.Entry(win)
q1.grid(row=8,column=1)

label_10 = tk.Label(win, text = 'Площадь сечения поперечной арматуры  Asw с шагом Sw, см2: ')
label_10.grid(row=9,column=0,stick='e')
Asw = tk.Entry(win)
Asw.grid(row=9,column=1)

label_11 = tk.Label(win, text = 'Шаг арматуры вдоль расчетного контура Sw, м: ')
label_11.grid(row=10,column=0,stick='e')
Sw = tk.Entry(win)
Sw.grid(row=10,column=1)

label_12 = tk.Label(win, text = 'Расчетное сопротивление арматуры Rs, мПа: ')
label_12.grid(row=11,column=0,stick='e')
Rs = tk.Entry(win)
Rs.grid(row=11,column=1)

label_13 = tk.Label(win, text = 'Расчетное сопротивление бетона Rbt, МПа: ')
label_13.grid(row=12,column=0,stick='e')
Rbt = tk.Entry(win)
Rbt.grid(row=12,column=1)

label_14 = tk.Label(win, text = 'Толщина плиты h, м (не менее 0.18м!): ')
label_14.grid(row=13,column=0,stick='e')
h = tk.Entry(win)
h.grid(row=13,column=1)

label_15 = tk.Label(win, text = 'Тип сопряжения перекрытия с колонной (формула), F = ')
label_15.grid(row=14,column=0,stick='e')
F = ttk.Combobox(win, values=formuls)
F.grid(row=14,column=1)

entries = {"q": q, "a1": a1, "b1": b1, "zox": zox, "zoy": zoy, "N1": N1, "N2": N2, "q1": q1, "Asw": Asw, "Sw": Sw, "Rs": Rs, "Rbt": Rbt, "h": h, "F": F}

btn_start = tk.Button(win, text = 'Рассчитать', command=show_values, bg='orange',activebackground='orange',bd=5)
btn_start.grid(row=15,column=0,columnspan=2,stick='we')

win.grid_columnconfigure(0, minsize=200)
win.grid_columnconfigure(0, minsize=100)


win.mainloop()
