import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog, pickle
windows = tkinter.Tk()
windows.geometry("400x300")
windows.title("Войти в систему")
rows = 10
cols = 10
mines = 10
login_pass_save ={}
field = []  # поле
buttons = []  # кнопки

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

gameover = False
customsizes = []  # Параметры пользователя

def start():
    text1 = tkinter.Label(text="Приветствуем вас в игре Сапер")
    button_registr1 = tkinter.Button(text="Зарегистрироваться", command=lambda: registration())
    button_login1 = tkinter.Button(text="Войти в свой аккаунт", command=lambda: login())
    text1.pack()
    button_registr1.pack()
    button_login1.pack()

    def registration():
        text = tkinter.Label(text="Для входа в игру зарегистрируйтесь!")
        text_login = tkinter.Label(text="Введите ваш логин:")
        registr_login = tkinter.Entry()
        text_password1 = tkinter.Label(text="Введите ваш пароль")
        registr_password1 = tkinter.Entry()
        text_password2 = tkinter.Label(text="Введите пароль повторно:")
        registr_password2 = tkinter.Entry(show="*")
        button_registr = tkinter.Button(text="Зарегистрироваться в игре!", command=lambda: save())
        text.pack()
        text_login.pack()
        registr_login.pack()
        text_password1.pack()
        registr_password1.pack()
        text_password2.pack()
        registr_password2.pack()
        button_registr.pack()
        text1.pack_forget()
        button_registr1.pack_forget()
        button_login1.pack_forget()

        def save():
            f = open("logins.txt", "rb")
            login_pass_save = pickle.load(f)
            login_pass_save[registr_login.get()] = registr_password1.get()
            f.close()
            f = open("logins.txt", "wb")
            pickle.dump(login_pass_save, f)
            text.pack_forget()
            text_login.pack_forget()
            registr_login.pack_forget()
            text_password1.pack_forget()
            registr_password1.pack_forget()
            text_password2.pack_forget()
            registr_password2.pack_forget()
            button_registr.pack_forget()
            f.close()
            login()



    def login():
        text_login = tkinter.Label(text="Вы зарегистрированы в игре! Теперь вы можете войти в систему игры!")
        text_enter_login = tkinter.Label(text="Введите ваш логин:")
        enter_login = tkinter.Entry()
        text_enter_password = tkinter.Label(text="Введите ваш пароль:")
        enter_password = tkinter.Entry(show="*")
        button_login = tkinter.Button(text="Войти", command=lambda: check())
        text_login.pack()
        text_enter_login.pack()
        enter_login.pack()
        text_enter_password.pack()
        enter_password.pack()
        button_login.pack()
        text1.pack_forget()
        button_registr1.pack_forget()
        button_login1.pack_forget()

        def check():
            f = open("logins.txt", "rb")
            a = pickle.load(f)
            f.close()
            if enter_login.get() in a:
                if enter_password.get() == a[enter_login.get()]:
                    tkinter.messagebox.showinfo("Все правильно", "Вы ввели все правильно,можете начать игру")
                    windows.destroy()
                    window = tkinter.Tk()

                    window.title("Сапер на Python")

                    def createMenu():  # Создаем меню с уровнями и возможностью выйти
                        menubar = tkinter.Menu(window)  # Создаем меню
                        menusize = tkinter.Menu(window, tearoff=0)  # tearoff=0,чтобы меню не имело функции открепления(отрыва) и выбор с 0 позиции
                        menusize.add_command(label="Новичок (9x9 с 10 минами)", command=lambda: setSize(9, 9, 10))  # Lambda передает целые числа в другую функцию
                        menusize.add_command(label="Любитель (16x16 с 40 минами)", command=lambda: setSize(16, 16, 40))
                        menusize.add_command(label="Профессионал (16x30 с 90 минами)", command=lambda: setSize(16, 30, 90))
                        menusize.add_command(label="Ваши параметры", command=setCustomSize)
                        menusize.add_separator()  # Добавляет линию разделитель в меню(визуальное разделение групп команд).
                        for x in range(0, len(customsizes)):  # Если пользователь выберет кастомный режим
                            menusize.add_command(label=str(customsizes[x][0]) + "x" + str(customsizes[x][1]) + " с " + str(customsizes[x][2]) + " минами",command=lambda customsizes=customsizes: setSize(customsizes[x][0],customsizes[x][1],customsizes[x][2]))
                        menubar.add_cascade(label="функции поля", menu=menusize)  # Подвязывает новый экземпляр меню и добавляет к главному меню(add_cascade)
                        menubar.add_command(label="Выйти из игры", command=lambda: window.destroy())  # Lambda>функция выйти
                        window.config(menu=menubar)  # Config устанавливает меню в окно

                    def setCustomSize():  # функция для создания параметров пользователя(кастомного поля)
                        global customsizes  # глобальная переменная
                        r = tkinter.simpledialog.askinteger("Ваши параметры", "Введите количество строк")
                        c = tkinter.simpledialog.askinteger("Ваши параметры", "Введите количество столбцов")
                        m = tkinter.simpledialog.askinteger("Ваши параметры", "Введите количество мин")
                        while m > r * c:  # Проверка,если пользователь ввведет количество мин больше,чем размер поля
                            m = tkinter.simpledialog.askinteger("Ваши параметры", "Максимальное допустимое количесвто мин при ваших параметрах- " + str( r * c) + "\nВведите допустимое количество мин")
                        customsizes.insert(0, (r, c, m))  # Метод insert используется,чтобы добавить елементы r,c,m на 0 позицию в списке
                        customsizes = customsizes[0:5]
                        setSize(r, c, m)  # Вводим размеры
                        createMenu()  # Создаем меню

                    def setSize(r, c, m):
                        global rows, cols, mines
                        rows = r  # Меняем значения на определенные пользователем через уровень или кастом
                        cols = c
                        mines = m
                        saveConfig()  # Сохраняем значения в файл
                        restartGame()  # После ввдеения и сохранения пармметров,перезагружаем игру и выводим поле с этими значениями

                    def saveConfig():  # Сохранения поля,запись в файл
                        global rows, cols, mines
                        config = configparser.ConfigParser()
                        config.add_section("game")  # Создаем секцию
                        config.set("game", "rows", str(rows))  # Создаем подпункты в секции game
                        config.set("game", "cols", str(cols))
                        config.set("game", "mines", str(mines))
                        config.add_section("sizes")
                        config.set("sizes", "amount", str(len(customsizes)))
                        for x in range(0, min(5, len(customsizes))):
                            config.set("sizes", "row" + str(x), str(customsizes[x][0]))
                            config.set("sizes", "cols" + str(x), str(customsizes[x][1]))
                            config.set("sizes", "mines" + str(x), str(customsizes[x][2]))

                        with open("parameters_field.ini", "w") as file:
                            config.write(file)  # Вносим изменения в файл

                    def loadConfig():  # Загрузка поля
                        global rows, cols, mines, customsizes
                        config = configparser.ConfigParser()
                        config.read("parameters_field.ini")
                        rows = config.getint("game", "rows")  # Параметры поля из файла
                        cols = config.getint("game", "cols")
                        mines = config.getint("game", "mines")
                        amountofsizes = config.getint("sizes", "amount")  # загружаем количество модификаций
                        for x in range(0, amountofsizes):
                            # Добавляем модификации из файла
                            customsizes.append((config.getint("sizes", "row" + str(x)),config.getint("sizes", "cols" + str(x)),config.getint("sizes", "mines" + str(x))))

                    def prepareGame():  # Подготовка игры(мины,поле)
                        global rows, cols, mines, field
                        field = []
                        # Мы создаем поле у которого будет система координат x,y
                        for x in range(0, rows):  # x-коордианты поля по столбцу
                            field.append([])  # Создаем двумерный список,где каждый одномерный список-строка поля
                            for y in range(0, cols):  # y-координаты поля по строке
                                # Ставим начальное значение для поля 0
                                field[x].append(0)
                        # Раставление мин
                        for true in range(0, mines):
                            x = random.randint(0, rows - 1)
                            y = random.randint(0, cols - 1)
                            # Чтобы мины не попались на одну клетку(то есть не совпали)
                            while field[x][y] == -1:
                                x = random.randint(0, rows - 1)
                                y = random.randint(0, cols - 1)
                            field[x][y] = -1
                            if x != 0:  # x-1
                                if y != 0:  # -1
                                    if field[x - 1][y - 1] != -1:
                                        field[x - 1][y - 1] = int(field[x - 1][y - 1]) + 1
                                if field[x - 1][y] != -1:
                                    field[x - 1][y] = int(field[x - 1][y]) + 1
                                if y != cols - 1:  # y+8
                                    if field[x - 1][y + 1] != -1:
                                        field[x - 1][y + 1] = int(field[x - 1][y + 1]) + 1
                            if y != 0:  # y-1
                                if field[x][y - 1] != -1:
                                    field[x][y - 1] = int(field[x][y - 1]) + 1
                            if y != cols - 1:  # y+1
                                if field[x][y + 1] != -1:
                                    field[x][y + 1] = int(field[x][y + 1]) + 1
                            if x != rows - 1:  # x+1
                                if y != 0:  # y-1
                                    if field[x + 1][y - 1] != -1:
                                        field[x + 1][y - 1] = int(field[x + 1][y - 1]) + 1
                                if field[x + 1][y] != -1:
                                    field[x + 1][y] = int(field[x + 1][y]) + 1
                                if y != cols - 1:  # y+1
                                    if field[x + 1][y + 1] != -1:
                                        field[x + 1][y + 1] = int(field[x + 1][y + 1]) + 1

                    def prepareWindow():  # Подготовка окна
                        global rows, cols, buttons
                        # Создаем кнопку перезагрузки
                        tkinter.Button(window, text="Перезагрузка", command=restartGame).grid(row=0, column=0,columnspan=cols, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # columnspan=cols,чтобы соединялось с кнопками поля sticky=N+S+W+E,чтобы разтянуть в весть объем
                        buttons = []
                        # Создаем кнопки
                        for x in range(0, rows):
                            buttons.append([])
                            for y in range(0, cols):
                                b = tkinter.Button(window, text=" ", width=2, command=lambda x=x, y=y: clickOn(x, y))
                                b.bind("<Button-3>", lambda e, x=x, y=y: onRightClick(x,y))  # lambda спользуется,чтобы передать доп аргумент в метод bind Button-3(ПКМ)
                                b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # row=x+1 потому что еще кнопка перезагрузки
                                buttons[x].append(b)  # Добавляем кнопки

                    def restartGame():
                        global gameover
                        gameover = False
                        # window.winfo_children(уничтажает виджеты frame) используется,чтобы изменить или убрать в окне
                        for x in window.winfo_children():
                            if type(x) != tkinter.Menu:
                                x.destroy()  # Удаляем поле
                        # Начинаем игру с новыми параметрами
                        prepareWindow()
                        prepareGame()

                    # Нажжатие кнопок поля
                    def clickOn(x, y):
                        global field, buttons, colors, gameover, rows, cols
                        if gameover:
                            return
                        buttons[x][y]["text"] = str(field[x][y])
                        if field[x][y] == -1:
                            buttons[x][y]["text"] = "*"
                            buttons[x][y].config(background='red', disabledforeground='black')  # disabledforeground-цвет текста,после нажатия
                            gameover = True
                            tkinter.messagebox.showinfo("Игра окончена", "Вы проиграли,попробуйте снова.")
                            # Выводим остальные мины на поле
                            for _x in range(0, rows):
                                for _y in range(cols):
                                    if field[_x][_y] == -1:
                                        buttons[_x][_y]["text"] = "*"
                        else:
                            buttons[x][y].config(disabledforeground=colors[field[x][y]])
                        if field[x][y] == 0:
                            buttons[x][y]["text"] = " "
                            autoClickOn(x, y)
                        buttons[x][y]['state'] = 'disabled'
                        buttons[x][y].config(relief=tkinter.SUNKEN)  # Кнопка выводится как нажатая
                        checkWin()

                    def autoClickOn(x, y):
                        global field, buttons, colors, rows, cols
                        if buttons[x][y]["state"] == "disabled":
                            return
                        if field[x][y] != 0:
                            buttons[x][y]["text"] = str(field[x][y])
                        else:
                            buttons[x][y]["text"] = " "
                        buttons[x][y].config(disabledforeground=colors[field[x][y]])
                        buttons[x][y].config(relief=tkinter.SUNKEN)
                        buttons[x][y]['state'] = 'disabled'
                        if field[x][y] == 0:
                            if x != 0 and y != 0:
                                autoClickOn(x - 1, y - 1)
                            if x != 0:
                                autoClickOn(x - 1, y)
                            if x != 0 and y != cols - 1:
                                autoClickOn(x - 1, y + 1)
                            if y != 0:
                                autoClickOn(x, y - 1)
                            if y != cols - 1:
                                autoClickOn(x, y + 1)
                            if x != rows - 1 and y != 0:
                                autoClickOn(x + 1, y - 1)
                            if x != rows - 1:
                                autoClickOn(x + 1, y)
                            if x != rows - 1 and y != cols - 1:
                                autoClickOn(x + 1, y + 1)

                    def onRightClick(x, y):
                        global buttons
                        if gameover:
                            return
                        if buttons[x][y]["text"] == "?":
                            buttons[x][y]["text"] = " "
                            buttons[x][y]["state"] = "normal"
                        elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
                            buttons[x][y]["text"] = "?"
                            buttons[x][y]["state"] = "disabled"

                    def checkWin():  # Проверка состояния игры
                        global buttons, field, rows, cols
                        win = True
                        for x in range(0, rows):
                            for y in range(0, cols):
                                if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                                    win = False
                        if win:
                            tkinter.messagebox.showinfo("Игра окончена", "Вы победили,поздравляю.")

                    if os.path.exists("parameters_field.ini"):
                        loadConfig()
                    else:
                        saveConfig()

                    createMenu()

                    prepareWindow()
                    prepareGame()
                    window.mainloop()
                else:
                    tkinter.messagebox.showerror("Ошибка!", "Вы ввели неверный логин или пароль")
            else:
                tkinter.messagebox.showerror("Ошибка!", "Вы ввели неверный логин")

start()
windows.mainloop()