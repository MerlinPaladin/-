import sys #Импортирует модуль sys, который позволяет взаимодействовать с интерпретатором Python, например, для получения аргументов командной строки.

#Импортирует необходимые классы из библиотеки PyQt5 для создания графического интерфейса.
#QApplication отвечает за управление приложением, QWidget — базовый класс для всех виджетов, QVBoxLayout — вертикулярный макет,
# QPushButton — кнопка, QListWidget — виджет списка, QLineEdit — однострочное текстовое поле, QLabel — метка, QMessageBox — диалоговое окно сообщений,
# QDateEdit — виджет для выбора даты
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, \
    QMessageBox, QDateEdit
#Импортирует функции для работы с базой данных (создание таблицы, добавление события, получение событий и удаление события)
from database import create_table, add_event, get_events, delete_event

#Определяет класс EventApp, который наследуется от QWidget, представляя основное окно приложения.
class EventApp(QWidget):
    def __init__(self):
        """Инициализирует приложение."""
        # Конструктор класса, где вызывается конструктор родительского класса (super().__init__()) и метод initUI для настройки графического интерфейса.
        super().__init__()
        self.initUI()
        create_table() # Создаем таблицу в базе данных, если она не существует
        self.load_events() # Загружаем данные о событиях из базы данных
        #Создается таблица в базе данных, если она еще не была создана, и загружаются существующие события из базы.

    def initUI(self):
        """Инициализирует графический интерфейс."""
        self.setWindowTitle('Заметки для событий')
        self.setGeometry(900, 500, 800, 600) # Устанавливает размеры окна и место появления

        # Настройка общего стиля для всех элементов
        self.setStyleSheet("""
            background-color: black;
            font-size: 16px;
            color: white;
        """)

        # Создаем вертикальный макет для компоновки элементов
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        #Создается вертикальный макет (QVBoxLayout), и он назначается как основная компоновка для виджетов.

        # Название события:
        self.event_name_label = QLabel('Название события:', self)
        self.layout.addWidget(self.event_name_label)
        self.event_name_input = QLineEdit(self)
        self.event_name_input.setPlaceholderText('Название')
        self.layout.addWidget(self.event_name_input)

        # Дата события (QDateEdit для выбора даты):
        self.event_date_label = QLabel('Дата:', self)
        self.layout.addWidget(self.event_date_label)
        self.event_date_input = QDateEdit(self)
        self.event_date_input.setCalendarPopup(True) # Появляется календарь при клике
        self.event_date_input.setDisplayFormat('yyyy-MM-dd') # Формат даты в поле
        self.layout.addWidget(self.event_date_input)

        # Локация события:
        self.event_location_label = QLabel('Локация проведения:', self)
        self.layout.addWidget(self.event_location_label)
        self.event_location_input = QLineEdit(self)
        self.event_location_input.setPlaceholderText('Локация')
        self.layout.addWidget(self.event_location_input)

        # Кнопка добавления события:
        self.add_button = QPushButton('Добавить событие', self)
        self.add_button.clicked.connect(self.add_event)
        self.layout.addWidget(self.add_button)

        # Список событий:
        self.event_list = QListWidget(self)
        self.event_list.itemDoubleClicked.connect(self.delete_event)
        self.layout.addWidget(self.event_list)

    def load_events(self):
        """Загружает события из базы данных в список."""
        self.event_list.clear() # Очищает список событий
        events = get_events() # Получаем события из базы данных
        for event in events:
            self.event_list.addItem(
                f"{event[0]}: {event[1]} on {event[2]} at {event[3]}"
            ) # Добавляем строку с информацией о событии

    def add_event(self):
        """Добавляет новое событие в базу данных."""
        name = self.event_name_input.text()
        date = self.event_date_input.date().toString('yyyy-MM-dd') # Извлекаем дату в нужном формате
        location = self.event_location_input.text()
        if name and date and location: # Проверка на заполненность полей
            add_event(name, date, location) # Добавляем событие в базу данных
            self.load_events() # Перезагружаем список событий
            self.event_name_input.clear()
            self.event_date_input.clear()
            self.event_location_input.clear()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все поля.')

    def delete_event(self, item):
        """Удаляет событие из базы данных по двойному клику."""
        try:
            event_id = int(item.text().split(':')[0])
            delete_event(event_id)
            self.load_events()
        except (ValueError, IndexError):
            QMessageBox.warning(self, 'Ошибка', 'Невозможно удалить событие.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EventApp()
    ex.show()
    sys.exit(app.exec_())
