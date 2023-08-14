import unittest
from unittest import skip

from django.test import tag

from functional_tests.base import FunctionalTest


@tag('functional')
class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
        # Она нажимает Enter на пустом поле ввода
        
        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое говорит,
        # что элементы списка не должны быть пустыми
        
        # Она пробует снова, теперь с неким текстом для элемента, и теперь это срабатывает
        
        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        
        # Она получает аналогичное предупреждение на странице списка
        
        # И она может его исправить, заполнив поле неким текстом
        
        self.fail('Конец теста!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
