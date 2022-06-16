# Класс c методами проверок строк, адаптированные под цели программы на базе класса str()
class mystr(str):
    # Функция проверки на наличие цифр в строке (если хотябы одна есть, то возвращает True)
    def have_digit(self):
        for i in self:
            if i.isdigit():
                return True
        return False

    # Функция проверки на пустотю строку или строку с одними пробелами
    def is_empty(self):
        if not self or self.isspace():
            return True
        return False

    # Функция совмещающая в себя 2 проверки (на пустоту и цифры) - если хоть одна проверка True, то строка не валидна
    def is_valid(self):
        if self.is_empty() or self.have_digit():
            return False
        return True


# Нормализация формата Даты к виду ЧЧ-ММ-ГГГГ (при выводе в консоль)
class normdate:
    def __init__(self, date):
            str = date.split('-')
            self.normdate =  '-'.join(str[::-1])

    def __str__(self):
        return self.normdate