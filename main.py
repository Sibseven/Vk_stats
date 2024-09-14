from sqlite3 import *
from tkinter import *
import difflib
import vk_api
import datetime
from Levenshtein import distance
root=Tk()
root.title('Vk stats')
root.geometry('500x500+600+300')
main_menu= Menu(root)
root.config(menu=main_menu)

class Search_main():
    def __init__(self):
        self.TOKEN  =  "8c3c49e78c3c49e78c3c49e7858c48f07788c3c8c3c49e7d39d004c7ba1090c4d55fe13"
        self.vk_session  =  vk_api.VkApi(app_id = 7649680, token=self.TOKEN)
        self.vk  =  self.vk_session.get_api()
        self.spliter  =  ','
        self.sexes  =  []
        self.interests  =  []
        self.bdates = []
    def search(self,need_sex,group,search_interests,min_age,max_age):
        self.need_sex = need_sex
        self.group  =  group
        self.search_interests = search_interests
        self.min_age = min_age
        self.max_age = max_age
        self.count_members = self.vk.groups.getMembers(group_id=self.group)['count']
        self.count_for = self.count_members//1000+1
        self.members = {}
        self.sexes  =  []
        self.interests  =  []
        self.bdates = []
        self.count_interest = 0
        self.count_interest_good = 0
        self.count_age = 0
        self.count_ideals_members = 0
        for i in range(1,self.count_for):
            self.now_members_ids = self.vk.groups.getMembers(group_id=self.group,offset=i*1000)['items']
            self.now_members_ids = self.spliter.join(map(str,self.now_members_ids))
            self.now_members_1000=self.vk.users.get(user_ids=self.now_members_ids, fields='sex,interests,bdate')
            for j in range(0,len(self.now_members_1000)):
                self.member = self.now_members_1000[j]
                self.id = self.member['id']
                self.members[self.id]=[ ]
                self.members[self.id].append(self.member['sex'])
                self.sexes.append(self.member['sex'])
                try:
                    if self.member['bdate'].count('.') == 2:
                        self.list_date = self.member['bdate'].split('.')
                        self.date_data = datetime.datetime(int(self.list_date[2]),int(self.list_date[1]),int(self.list_date[0]))
                        self.now_date = datetime.datetime.today()
                        self.delta_date = self.now_date - self.date_data
                        self.final_age=self.delta_date.days//365
                        self.bdates.append(self.final_age)
                        self.members[self.id].append(self.final_age)
                except KeyError:
                    pass
                try:
                    if self.member['interests']!='':
                        self.interests.append(self.member['interests'])
                        self.count_interest+= 1
                        self.members[self.id].append(self.member['interests'])
                except KeyError:
                    pass
                if len(self.members[self.id])!=3:
                    self.members.pop(self.id)
        self.count_male = 0
        if self.need_sex==2: # Если пол мужской
            if self.search_interests==[] or self.search_interests==['']:
                for i in self.members.values():
                    if i[0]==2 and i[1]>=self.min_age and i[1]<=self.max_age:
                        self.count_ideals_members+=1
                        print(i)
            else:
                for i in self.members.values():
                    for j in self.search_interests:
                        if len(j)<=2:
                            if j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                        elif len(j)>3:
                            if distance(j,i[2])<= 2 or j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                    if i[0]==2 and i[1]>=self.min_age and i[1]<=self.max_age and self.now_member_good_interest==1:
                        self.count_ideals_members+=1
        elif self.need_sex==1:# Если пол женский
            if self.search_interests==[] or self.search_interests==['']:
                for i in self.members.values():
                    if i[0]==1 and i[1]>=self.min_age and i[1]<=self.max_age:
                        self.count_ideals_members+=1                                             
            else:
                for i in self.members.values():
                    for j in self.search_interests:
                        if len(j)<=2:
                            if j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                        elif len(j)>3:
                            if distance(j,i[2])<= 2 or j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                    if i[0]==1 and i[1]>=self.min_age and i[1]<=self.max_age and self.now_member_good_interest==1:
                        self.count_ideals_members+=1
        elif self.need_sex==0: #Если пол не важен
            if self.search_interests==[] or self.search_interests==['']:
                for i in self.members.values():
                    if i[0]==2 and i[1]>=self.min_age and i[1]<=self.max_age:
                        self.count_ideals_members+=1                                           
            else:
                for i in self.members.values():
                    for j in self.search_interests:
                        if len(j)<=2:
                            if j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                        elif len(j)>3:
                            if distance(j,i[2])<= 2 or j in i[2]:
                                self.now_member_good_interest=1
                            else:
                                self.now_member_good_interest=0
                    if i[0]==0 and i[1]>=self.min_age and i[1]<=self.max_age and self.now_member_good_interest==1:
                        self.count_ideals_members+=1
        for i in self.sexes:
            if i == 2:
                self.count_male+= 1
        self.count_female = self.count_members-self.count_male
        if search_interests==[]:
            self.count_interest_good=self.count_members
        else:
            for i in self.interests:
                for j in self.search_interests:
                    if len(j)<= 2:
                        if j in i:
                            self.count_interest_good+= 1
                    else:
                        if distance(j,i)<= 2 or j in i:
                            self.count_interest_good+= 1
        for i in self.bdates:
            if i >= self.min_age and i <= self.max_age:
                self.count_age+=1
        if need_sex==1:
            return self.count_female, self.count_age,self.count_interest_good,self.count_ideals_members
        elif need_sex==2:
            return self.count_male, self.count_age,self.count_interest_good,self.count_ideals_members
        else:
            return self.count_members, self.count_age,self.count_interest_good,self.count_ideals_members
        
class Groups_menu:
    def __init__(self):
        
        self.groups_window=Toplevel()
        self.groups_window.title('Groups')
        self.groups_window.geometry('150x200+448+300')
        self.e_groups=Entry(self.groups_window)
        self.l_groups=Listbox(self.groups_window)
        self.b_save=Button(self.groups_window, text='Save', command=self.Save_group)
        self.sqlite_connection=connect('vk.db')
        self.cursor=self.sqlite_connection.cursor()
        self.groups=(self.cursor.execute('SELECT * FROM Groups')).fetchall()
        for i in self.groups:
            self.l_groups.insert(END,i[0])
        self.e_groups.pack()
        self.l_groups.pack()
        self.b_save.pack()
        self.e_groups.bind('<Return>',self.Add_group)
        self.l_groups.bind('<Double-Button-1>',self.Delete_group)
    def Add_group(self,event):
        self.l_groups.insert(END,self.e_groups.get())
    def Delete_group(self,event):
        self.selected=self.l_groups.curselection()
        self.l_groups.delete(self.selected)
    def Save_group(self):
        now_groups=self.l_groups.get(0,END)
        self.cursor.execute('DELETE FROM Groups')
        for i in now_groups:
            self.cursor.execute('INSERT INTO Groups VALUES(?)',[i])
        self.sqlite_connection.commit()
def Create_groups_menu():
    new_group=Groups_menu()
class Filter_menu:
    def __init__(self):
        self.filter_window=Toplevel()
        self.filter_window.title('Filter')
        self.filter_window.geometry('200x580+1102+299')
        self.check = 0

        self.sqlite_connection=connect('vk.db')
        self.cursor=self.sqlite_connection.cursor()

        self.f_male=LabelFrame(self.filter_window,text='Male:')
        self.v_male=IntVar()
        self.male_value=(self.cursor.execute('SELECT * FROM male')).fetchall()[0][0]
        if self.male_value==0:
            self.v_male.set(0)
        elif self.male_value==1:
            self.v_male.set(1)
        else:
            self.v_male.set(2)
        self.r_none=Radiobutton(self.f_male,text='Dont matter',value=0,variable=self.v_male)
        self.r_male=Radiobutton(self.f_male,text='Male',value=2,variable=self.v_male)
        self.r_female=Radiobutton(self.f_male,text='Female',value=1,variable=self.v_male)

        self.f_age=LabelFrame(self.filter_window,text='Age:')
        self.l_min_age=Label(self.f_age,text='From')
        self.e_min_age=Entry(self.f_age,width=2)
        self.min_age_value=(self.cursor.execute('SELECT * FROM Age')).fetchall()[0][0]
        self.e_min_age.insert(0,self.min_age_value)
        
        self.l_max_age=Label(self.f_age,text='To')
        self.e_max_age=Entry(self.f_age,width=2)
        self.max_age_value=(self.cursor.execute('SELECT * FROM Age')).fetchall()[0][1]
        self.e_max_age.insert(0,self.max_age_value)

        self.f_interests=LabelFrame(self.filter_window, text="Interests:")
        self.e_interests=Entry(self.f_interests,width=15)
        self.e_interests.bind('<KeyRelease>',self.Search_filter)
        self.list_interests=Listbox(self.f_interests)
        self.list_interests.bind('<Double-Button-1>',self.Select_interest)
        self.list_of_interests_original=['Авто, мото','Автовладельцы','Автомобили','Автомойка','Автопроизводитель','Автосалон','Автосервис','Автотовары','Аренда автомобилей','Велосипеды','Водный транспорт','Мотоциклы и другая мототехника','Услуги для автовладельцев','Бытовые услуги','Баня, сауна','Клининг','Компьютерные услуги','Пошив и ремонт одежды','Прокат','Ремонтная мастерская','Химчистка, прачечная','Города, страны','Городское сообщество','Страна','Дом, ремонт','Дизайн интерьера','Садоводство','Животные','Ветеринарная клиника','Зоомагазин','Товары для животных','Услуги для владельцев животных','Интернет','Веб-студия','Видеоигры','ВКонтакте','Мобильные технологии','Объявления','Приложение','Программирование','Программное обеспечение','Сайты','Хостинг, регистрация доменов','Красота, здоровье','Бассейн','Диеты, здоровое питание','Здоровый образ жизни','Парфюмерия, косметика','Психология','Салон красоты','Спа-салон','Стиль, мода','Тату-салон','Уход за собой','Фитнес','Фитнес-центр','Кулинария, рецепты','Культура, искусство','Архив','Библиотека','Дом культуры','Книга','Культурный центр','Музей, галерея, выставка','Театр','Медицина','Аптека, оптика','Больница','Косметология','Лекарственный препарат','Медицинская услуга','Медицинский центр','Стоматология','Музыка','R&B','Rap, Hip-Hop','Блюз','Джаз','Другая музыка','Инди','Классическая музыка','Латиноамериканская музыка','Метал','Народная музыка, фолк','Обмен музыкой','Рок','Танцевальная музыка','Тексты, аккорды','Электронная музыка','Образование','Автошкола','Гимназия','Детский сад','Дополнительное образование','Институт','Колледж','Лицей','Обучающие курсы','Танцевальная школа','Техникум','Тренинг, семинар','Университет','Школа','Отношения, семья','Беременность, роды','Друзья','Отношения полов','Подготовка к свадьбе','Родители и дети','Родственники','Персона','DJ','Актёр или актриса','Блогер','Ведущий или ведущая','Врач','Вымышленный персонаж','Дизайнер','Журналист или журналистка','Комик','Композитор','Критик','Модель','Музыкальная группа','Музыкант','Общественный деятель','Певец или певица','Писатель или писательница','Политик, госслужащий','Поэт или поэтесса','Предприниматель или предпринимательница','Психолог','Режиссёр, продюсер','Стилист, имиджмейкер','Стример','Танцор, танцовщица','Учёный, преподаватель','Фотограф','Художник или художница','Поиск работы','Профессиональные услуги','Безопасность','Детективное агентство','Дизайн-студия','Другие услуги','Консалтинг, бизнес-услуги','Модельное агентство','Музыкальный лейбл','Недвижимость','Нотариальная контора','Организация праздников','Печать, полиграфия','Поиск работы','Производство контента','Производство, промышленность','Реклама','Строительные и ремонтные работы','Студия звукозаписи','Управляющая компания','Фото- и видеосъёмка','Юридические услуги','Развлечения','Анимация','Бильярдный клуб','Боулинг','Видеоигра','Знакомства','Зоопарк','Игры','Интеллектуальные игры','Каток','Квест','Кино','Кинотеатр','Концерт','Концертный зал','Литература','Лотерея, розыгрыш','Музыка','Мультфильм','Настольные игры','Ночной клуб','Онлайн-игра','Отдых на природе','Парк отдыха','Ролевые игры','Сериал','Танцы','Торгово-развлекательный центр','Фестиваль','Фильм','Цирк','Шоу, передача','Эротика','Юмор','Рестораны','Бар, паб','Доставка еды','Кафе, ресторан','Кофейня','Кулинария','СМИ','Блог','Издательский дом','Интернет-СМИ','Печатное издание','Радиостанция','Телеканал','Шоу, передача','Социальные и общественные организации','Благотворительная организация','Государственная организация','Группа выпускников','Группа коллег','Группа одноклассников','Группа памяти','Группа сокурсников','Дискуссионный клуб','Молодёжное движение','Общественная организация','Однофамильцы и тёзки','Политическая партия','Религиозное учреждение','Соседи','Фан-клуб','Спорт','Автоспорт','Азартные игры','Баскетбол','Баскетбольная команда','Боевые искусства','Водный спорт','Волейбол','Волейбольная команда','Другие виды спорта','Зимние виды спорта','Киберспорт','Киберспортивная команда','Киберспортивная организация','Киберспортсмен','Лёгкая атлетика','Летние виды спорта','Мотоспорт','Ролики','Спортивная команда','Спортивная организация','Спортивное питание','Спортивный клуб','Спортивный комплекс','Спортсмен / Спортсменка','Теннис','Университетский спорт','Футбол','Футбольная команда','Хоккей','Хоккейная команда','Экстремальный спорт','Товары, магазины','Антиквариат','Бытовая техника','Детская одежда и обувь','Детское питание','Другие товары','Игры, игрушки','Интерьер','Книжный магазин','Компьютерная техника','Мебель','Музыкальные инструменты','Оборудование','Одежда, обувь','Продукты питания, напитки','Салоны сотовой связи','Свадебный салон','Спортивная одежда и обувь','Спортивные товары','Строительные материалы, инструменты','Супермаркет','Товары для взрослых','Товары для дачи, огорода','Товары для детей','Товары для дома','Товары для офиса','Товары для праздников','Товары для творчества','Торговый центр','Украшения, бижутерия','Цветы','Часы','Электроника','Ювелирные изделия','Транспортные услуги','Авиакомпания','Аэропорт, вокзал','Грузоперевозки','Курьерская служба','Пассажирские перевозки','Почтовая служба','Прокат','Такси','Туризм и отдых','Активный отдых','Визовый центр','Гостиница','Информационный портал','Летний лагерь','Национальный парк, заповедник','Охота и рыбалка','Продажа билетов, бронирование гостиниц','Санаторий, дом отдыха','Туристическое агентство','Туры, экскурсии','Хостел','Увлечения и хобби','Астрология, эзотерика','Военное дело','Дизайн и графика','Другие хобби','История','Наука','Общество','Охота','Политика','Религия','Рыбалка','Творчество','Философия','Фотография','Языки','Услуги связи','Интернет-провайдер','Оператор мобильной связи','Оператор спутникового телевидения','Оператор стационарной связи','Финансы и страхование','Автострахование','Банк, финансовое учреждение','Бухучёт и налоги','Ломбард','Пенсионный фонд','Платёжная система','Страховая компания','Финансовые рынки']
        self.list_of_interests=['Авто, мото','Автовладельцы','Автомобили','Автомойка','Автопроизводитель','Автосалон','Автосервис','Автотовары','Аренда автомобилей','Велосипеды','Водный транспорт','Мотоциклы и другая мототехника','Услуги для автовладельцев','Бытовые услуги','Баня, сауна','Клининг','Компьютерные услуги','Пошив и ремонт одежды','Прокат','Ремонтная мастерская','Химчистка, прачечная','Города, страны','Городское сообщество','Страна','Дом, ремонт','Дизайн интерьера','Садоводство','Животные','Ветеринарная клиника','Зоомагазин','Товары для животных','Услуги для владельцев животных','Интернет','Веб-студия','Видеоигры','ВКонтакте','Мобильные технологии','Объявления','Приложение','Программирование','Программное обеспечение','Сайты','Хостинг, регистрация доменов','Красота, здоровье','Бассейн','Диеты, здоровое питание','Здоровый образ жизни','Парфюмерия, косметика','Психология','Салон красоты','Спа-салон','Стиль, мода','Тату-салон','Уход за собой','Фитнес','Фитнес-центр','Кулинария, рецепты','Культура, искусство','Архив','Библиотека','Дом культуры','Книга','Культурный центр','Музей, галерея, выставка','Театр','Медицина','Аптека, оптика','Больница','Косметология','Лекарственный препарат','Медицинская услуга','Медицинский центр','Стоматология','Музыка','R&B','Rap, Hip-Hop','Блюз','Джаз','Другая музыка','Инди','Классическая музыка','Латиноамериканская музыка','Метал','Народная музыка, фолк','Обмен музыкой','Рок','Танцевальная музыка','Тексты, аккорды','Электронная музыка','Образование','Автошкола','Гимназия','Детский сад','Дополнительное образование','Институт','Колледж','Лицей','Обучающие курсы','Танцевальная школа','Техникум','Тренинг, семинар','Университет','Школа','Отношения, семья','Беременность, роды','Друзья','Отношения полов','Подготовка к свадьбе','Родители и дети','Родственники','Персона','DJ','Актёр или актриса','Блогер','Ведущий или ведущая','Врач','Вымышленный персонаж','Дизайнер','Журналист или журналистка','Комик','Композитор','Критик','Модель','Музыкальная группа','Музыкант','Общественный деятель','Певец или певица','Писатель или писательница','Политик, госслужащий','Поэт или поэтесса','Предприниматель или предпринимательница','Психолог','Режиссёр, продюсер','Стилист, имиджмейкер','Стример','Танцор, танцовщица','Учёный, преподаватель','Фотограф','Художник или художница','Поиск работы','Профессиональные услуги','Безопасность','Детективное агентство','Дизайн-студия','Другие услуги','Консалтинг, бизнес-услуги','Модельное агентство','Музыкальный лейбл','Недвижимость','Нотариальная контора','Организация праздников','Печать, полиграфия','Поиск работы','Производство контента','Производство, промышленность','Реклама','Строительные и ремонтные работы','Студия звукозаписи','Управляющая компания','Фото- и видеосъёмка','Юридические услуги','Развлечения','Анимация','Бильярдный клуб','Боулинг','Видеоигра','Знакомства','Зоопарк','Игры','Интеллектуальные игры','Каток','Квест','Кино','Кинотеатр','Концерт','Концертный зал','Литература','Лотерея, розыгрыш','Музыка','Мультфильм','Настольные игры','Ночной клуб','Онлайн-игра','Отдых на природе','Парк отдыха','Ролевые игры','Сериал','Танцы','Торгово-развлекательный центр','Фестиваль','Фильм','Цирк','Шоу, передача','Эротика','Юмор','Рестораны','Бар, паб','Доставка еды','Кафе, ресторан','Кофейня','Кулинария','СМИ','Блог','Издательский дом','Интернет-СМИ','Печатное издание','Радиостанция','Телеканал','Шоу, передача','Социальные и общественные организации','Благотворительная организация','Государственная организация','Группа выпускников','Группа коллег','Группа одноклассников','Группа памяти','Группа сокурсников','Дискуссионный клуб','Молодёжное движение','Общественная организация','Однофамильцы и тёзки','Политическая партия','Религиозное учреждение','Соседи','Фан-клуб','Спорт','Автоспорт','Азартные игры','Баскетбол','Баскетбольная команда','Боевые искусства','Водный спорт','Волейбол','Волейбольная команда','Другие виды спорта','Зимние виды спорта','Киберспорт','Киберспортивная команда','Киберспортивная организация','Киберспортсмен','Лёгкая атлетика','Летние виды спорта','Мотоспорт','Ролики','Спортивная команда','Спортивная организация','Спортивное питание','Спортивный клуб','Спортивный комплекс','Спортсмен / Спортсменка','Теннис','Университетский спорт','Футбол','Футбольная команда','Хоккей','Хоккейная команда','Экстремальный спорт','Товары, магазины','Антиквариат','Бытовая техника','Детская одежда и обувь','Детское питание','Другие товары','Игры, игрушки','Интерьер','Книжный магазин','Компьютерная техника','Мебель','Музыкальные инструменты','Оборудование','Одежда, обувь','Продукты питания, напитки','Салоны сотовой связи','Свадебный салон','Спортивная одежда и обувь','Спортивные товары','Строительные материалы, инструменты','Супермаркет','Товары для взрослых','Товары для дачи, огорода','Товары для детей','Товары для дома','Товары для офиса','Товары для праздников','Товары для творчества','Торговый центр','Украшения, бижутерия','Цветы','Часы','Электроника','Ювелирные изделия','Транспортные услуги','Авиакомпания','Аэропорт, вокзал','Грузоперевозки','Курьерская служба','Пассажирские перевозки','Почтовая служба','Прокат','Такси','Туризм и отдых','Активный отдых','Визовый центр','Гостиница','Информационный портал','Летний лагерь','Национальный парк, заповедник','Охота и рыбалка','Продажа билетов, бронирование гостиниц','Санаторий, дом отдыха','Туристическое агентство','Туры, экскурсии','Хостел','Увлечения и хобби','Астрология, эзотерика','Военное дело','Дизайн и графика','Другие хобби','История','Наука','Общество','Охота','Политика','Религия','Рыбалка','Творчество','Философия','Фотография','Языки','Услуги связи','Интернет-провайдер','Оператор мобильной связи','Оператор спутникового телевидения','Оператор стационарной связи','Финансы и страхование','Автострахование','Банк, финансовое учреждение','Бухучёт и налоги','Ломбард','Пенсионный фонд','Платёжная система','Страховая компания','Финансовые рынки']
        for i in ('Авто, мото','Автовладельцы','Автомобили','Автомойка','Автопроизводитель','Автосалон','Автосервис','Автотовары','Аренда автомобилей','Велосипеды','Водный транспорт','Мотоциклы и другая мототехника','Услуги для автовладельцев','Бытовые услуги','Баня, сауна','Клининг','Компьютерные услуги','Пошив и ремонт одежды','Прокат','Ремонтная мастерская','Химчистка, прачечная','Города, страны','Городское сообщество','Страна','Дом, ремонт','Дизайн интерьера','Садоводство','Животные','Ветеринарная клиника','Зоомагазин','Товары для животных','Услуги для владельцев животных','Интернет','Веб-студия','Видеоигры','ВКонтакте','Мобильные технологии','Объявления','Приложение','Программирование','Программное обеспечение','Сайты','Хостинг, регистрация доменов','Красота, здоровье','Бассейн','Диеты, здоровое питание','Здоровый образ жизни','Парфюмерия, косметика','Психология','Салон красоты','Спа-салон','Стиль, мода','Тату-салон','Уход за собой','Фитнес','Фитнес-центр','Кулинария, рецепты','Культура, искусство','Архив','Библиотека','Дом культуры','Книга','Культурный центр','Музей, галерея, выставка','Театр','Медицина','Аптека, оптика','Больница','Косметология','Лекарственный препарат','Медицинская услуга','Медицинский центр','Стоматология','Музыка','R&B','Rap, Hip-Hop','Блюз','Джаз','Другая музыка','Инди','Классическая музыка','Латиноамериканская музыка','Метал','Народная музыка, фолк','Обмен музыкой','Рок','Танцевальная музыка','Тексты, аккорды','Электронная музыка','Образование','Автошкола','Гимназия','Детский сад','Дополнительное образование','Институт','Колледж','Лицей','Обучающие курсы','Танцевальная школа','Техникум','Тренинг, семинар','Университет','Школа','Отношения, семья','Беременность, роды','Друзья','Отношения полов','Подготовка к свадьбе','Родители и дети','Родственники','Персона','DJ','Актёр или актриса','Блогер','Ведущий или ведущая','Врач','Вымышленный персонаж','Дизайнер','Журналист или журналистка','Комик','Композитор','Критик','Модель','Музыкальная группа','Музыкант','Общественный деятель','Певец или певица','Писатель или писательница','Политик, госслужащий','Поэт или поэтесса','Предприниматель или предпринимательница','Психолог','Режиссёр, продюсер','Стилист, имиджмейкер','Стример','Танцор, танцовщица','Учёный, преподаватель','Фотограф','Художник или художница','Поиск работы','Профессиональные услуги','Безопасность','Детективное агентство','Дизайн-студия','Другие услуги','Консалтинг, бизнес-услуги','Модельное агентство','Музыкальный лейбл','Недвижимость','Нотариальная контора','Организация праздников','Печать, полиграфия','Поиск работы','Производство контента','Производство, промышленность','Реклама','Строительные и ремонтные работы','Студия звукозаписи','Управляющая компания','Фото- и видеосъёмка','Юридические услуги','Развлечения','Анимация','Бильярдный клуб','Боулинг','Видеоигра','Знакомства','Зоопарк','Игры','Интеллектуальные игры','Каток','Квест','Кино','Кинотеатр','Концерт','Концертный зал','Литература','Лотерея, розыгрыш','Музыка','Мультфильм','Настольные игры','Ночной клуб','Онлайн-игра','Отдых на природе','Парк отдыха','Ролевые игры','Сериал','Танцы','Торгово-развлекательный центр','Фестиваль','Фильм','Цирк','Шоу, передача','Эротика','Юмор','Рестораны','Бар, паб','Доставка еды','Кафе, ресторан','Кофейня','Кулинария','СМИ','Блог','Издательский дом','Интернет-СМИ','Печатное издание','Радиостанция','Телеканал','Шоу, передача','Социальные и общественные организации','Благотворительная организация','Государственная организация','Группа выпускников','Группа коллег','Группа одноклассников','Группа памяти','Группа сокурсников','Дискуссионный клуб','Молодёжное движение','Общественная организация','Однофамильцы и тёзки','Политическая партия','Религиозное учреждение','Соседи','Фан-клуб','Спорт','Автоспорт','Азартные игры','Баскетбол','Баскетбольная команда','Боевые искусства','Водный спорт','Волейбол','Волейбольная команда','Другие виды спорта','Зимние виды спорта','Киберспорт','Киберспортивная команда','Киберспортивная организация','Киберспортсмен','Лёгкая атлетика','Летние виды спорта','Мотоспорт','Ролики','Спортивная команда','Спортивная организация','Спортивное питание','Спортивный клуб','Спортивный комплекс','Спортсмен / Спортсменка','Теннис','Университетский спорт','Футбол','Футбольная команда','Хоккей','Хоккейная команда','Экстремальный спорт','Товары, магазины','Антиквариат','Бытовая техника','Детская одежда и обувь','Детское питание','Другие товары','Игры, игрушки','Интерьер','Книжный магазин','Компьютерная техника','Мебель','Музыкальные инструменты','Оборудование','Одежда, обувь','Продукты питания, напитки','Салоны сотовой связи','Свадебный салон','Спортивная одежда и обувь','Спортивные товары','Строительные материалы, инструменты','Супермаркет','Товары для взрослых','Товары для дачи, огорода','Товары для детей','Товары для дома','Товары для офиса','Товары для праздников','Товары для творчества','Торговый центр','Украшения, бижутерия','Цветы','Часы','Электроника','Ювелирные изделия','Транспортные услуги','Авиакомпания','Аэропорт, вокзал','Грузоперевозки','Курьерская служба','Пассажирские перевозки','Почтовая служба','Прокат','Такси','Туризм и отдых','Активный отдых','Визовый центр','Гостиница','Информационный портал','Летний лагерь','Национальный парк, заповедник','Охота и рыбалка','Продажа билетов, бронирование гостиниц','Санаторий, дом отдыха','Туристическое агентство','Туры, экскурсии','Хостел','Увлечения и хобби','Астрология, эзотерика','Военное дело','Дизайн и графика','Другие хобби','История','Наука','Общество','Охота','Политика','Религия','Рыбалка','Творчество','Философия','Фотография','Языки','Услуги связи','Интернет-провайдер','Оператор мобильной связи','Оператор спутникового телевидения','Оператор стационарной связи','Финансы и страхование','Автострахование','Банк, финансовое учреждение','Бухучёт и налоги','Ломбард','Пенсионный фонд','Платёжная система','Страховая компания','Финансовые рынки'):
            self.list_interests.insert(END,i)
        self.l_selected=Label(self.f_interests, text='Selected:')
        self.list_selected=Listbox(self.f_interests)
        self.list_selected.bind('<Double-Button-1>',self.Unselect_interest)
        self.list_of_save_selected=(self.cursor.execute('SELECT * FROM Interests')).fetchall()[0][0]
        self.list_of_save_selected=self.list_of_save_selected.split('  ')
        for i in self.list_of_save_selected:
            if i in self.list_of_interests:
                self.list_interests.delete(self.list_of_interests.index(i))
                self.list_of_interests.remove(i)
                self.list_selected.insert(END,i)
            else:
                self.list_selected.insert(END,i)
        self.f_keywords=Frame(self.filter_window)
        self.e_keywords=Entry(self.f_keywords,width=10)
        self.e_keywords.bind('<Return>',self.Select_keyword)
  
        self.b_save=Button(self.filter_window,width=5,command=self.Save_filters,text='Save')
        
        self.f_male.pack()
        self.r_none.pack()
        self.r_male.pack()
        self.r_female.pack()

        self.f_age.pack()
        self.l_min_age.grid(row=0,column=0)
        self.e_min_age.grid(row=0,column=1)

        self.l_max_age.grid(row=1,column=0)
        self.e_max_age.grid(row=1,column=1)
        
        self.f_interests.pack()
        self.e_interests.pack()
        self.list_interests.pack()
        self.l_selected.pack()
        self.list_selected.pack()

        self.f_keywords.pack()
        self.e_keywords.pack()
        self.b_save.pack()
    def Search_filter(self,event):
        self.now_interests=self.e_interests.get()
        self.suitable_interests=[]
        for i in self.list_of_interests:
            if self.now_interests == "":
                self.suitable_interests.append(i)
            elif self.now_interests.lower() in i.lower():
                self.suitable_interests.append(i)
        self.list_interests.delete(0,END)
        for i in self.suitable_interests:
            self.list_interests.insert(END,i)
    def Select_interest(self,event):
        try:
            self.selected=self.list_interests.curselection()
            self.io=self.list_interests.get(self.selected)
            self.list_selected.insert(END,self.io)
            self.list_interests.delete(self.selected)
            self.list_of_interests.pop(self.selected[0])
        except Exception:
            pass
    def Unselect_interest(self,event):
        try:
            self.unselected = self.list_selected.curselection()
            self.unsel = self.list_selected.get(self.unselected)
            if self.unsel in self.list_of_interests_original:
                self.list_interests.insert(END,self.unsel)
                self.list_selected.delete(self.unselected)
                self.list_of_interests.append(self.unsel)
            else:
                self.list_selected.delete(self.unselected)
        except Exception:
            pass
    def Select_keyword(self,event):
        self.keyword = self.e_keywords.get()
        self.list_selected.insert(END,self.keyword)
        self.e_keywords.delete(0,END)
        
    def Save_filters(self):
        self.cursor.execute('UPDATE Male SET male=? ', [self.v_male.get()])
        self.cursor.execute('UPDATE Age SET `rom`=?,`to`=? WHERE `rom`=? AND `to`=?',[self.e_min_age.get(),self.e_max_age.get(),self.min_age_value,self.max_age_value])
        spliter='  '
        self.cursor.execute('UPDATE Interests SET interests=?',[spliter.join(list(self.list_selected.get(0,END)))])
        self.sqlite_connection.commit()
def Create_filter_menu():
    new_filter=Filter_menu()
def Clear_filter():
    sqlite_connection = connect('vk.db')
    cursor=sqlite_connection.cursor()
    cursor.execute('UPDATE Interests SET interests=?',[' '])
    cursor.execute('UPDATE Male SET male=?',[0])
    cursor.execute('UPDATE Age SET `rom`=?,`to`=?',[0,0])
    sqlite_connection.commit()

def Search_button():
    sqlite_connection = connect('vk.db')
    cursor=sqlite_connection.cursor()
    need_sex=cursor.execute('SELECT * FROM male').fetchall()[0][0]
    
    group=cursor.execute('SELECT * FROM groups').fetchall()
    interests_s=cursor.execute('SELECT * FROM Interests').fetchall()[0][0]
    spliter='  '
    interests_s=interests_s.split('  ')
    group=list(group)
    min_age=cursor.execute('SELECT * FROM Age').fetchall()[0][0]
    max_age=cursor.execute('SELECT * FROM Age').fetchall()[0][1]
    for i in group:
        x,y,z,l = search_object.search(need_sex,i,interests_s,min_age,max_age)
        search_results_f = Frame(root)
        
        good_male = Label(search_results_f,text=x)
        t_male = Label(search_results_f,text='Male mathes found')
        
        good_age = Label(search_results_f,text=y)
        t_age = Label(search_results_f,text='Age mathes found')
        
        good_interests = Label(search_results_f,text=z)
        t_interests = Label(search_results_f,text='Interests mathes found')
        
        t_group = Label(search_results_f,text=str(i[0]))
        
        t_ideal_mathes = Label(search_results_f,text='Ideal mathes found')
        ideal_member = Label(search_results_f,text=l) 
        search_results_f.pack()
        good_male.grid(row=0, column=2)
        t_male.grid(row=0,column=1)
        good_age.grid(row=1, column=2)
        t_age.grid(row=1,column=1)
        good_interests.grid(row=2, column=2)
        t_interests.grid(row=2,column=1)
        t_group.grid(row=0,column=0,rowspan=4)
        t_ideal_mathes.grid(row=3,column=1)
        ideal_member.grid(row=3,column=2)
search_object=Search_main()

main_menu.add_command(label='Groups',command=Create_groups_menu)
main_menu.add_command(label='Filter',command=Create_filter_menu)
main_menu.add_command(label='Clear Filter',command=Clear_filter)
main_menu.add_command(label='Search',command= Search_button)

root.mainloop()
