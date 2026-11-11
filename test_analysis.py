import pytest
from analysis import completion_counts, select_tasks, top_users, validate_todos


def test_validate_todos_valid():
    data = [
        {"id": 1, "userId": 5, "title": "Ввод", "completed": True},
        {"id": 2, "userId": 5, "title": "Циклы", "completed": False}
    ]
    validate_todos(data)


def test_validate_todos_invalid():
    # Не список
    try:
        validate_todos({"id": 1})
        assert False, "Не обнаружено нарушение: корень не список"
    except ValueError:
        pass

    # Повтор id
    try:
        validate_todos([
            {"id": 1, "userId": 5, "title": "A", "completed": True},
            {"id": 1, "userId": 5, "title": "B", "completed": False}
        ])
        assert False, "Не обнаружено нарушение: дубликат id"
    except ValueError:
        pass

    # completed не bool (строка "True")
    try:
        validate_todos([
            {"id": 1, "userId": 5, "title": "A", "completed": "True"}
        ])
        assert False, "Не обнаружено нарушение: completed не boolean"
    except ValueError:
        pass

    # completed не bool (int 1)
    try:
        validate_todos([
            {"id": 1, "userId": 5, "title": "A", "completed": 1}
        ])
        assert False, "Не обнаружено нарушение: completed не boolean"
    except ValueError:
        pass


def test_completion_and_leaders():
    todos = [
        {"id": 1, "userId": 5, "title": "A", "completed": True},
        {"id": 2, "userId": 5, "title": "B", "completed": False},
        {"id": 3, "userId": 10, "title": "C", "completed": True},
        {"id": 4, "userId": 10, "title": "D", "completed": True},
        {"id": 5, "userId": 5, "title": "E", "completed": True}
    ]
    counts = completion_counts(todos)
    assert counts == {5: 2, 10: 2}

    leaders = top_users(counts)
    assert leaders == [5, 10]


def test_empty_and_zero_leaders():
    assert completion_counts([]) == {}
    assert top_users({}) == []

    only_false = [
        {"id": 1, "userId": 5, "title": "A", "completed": False}
    ]
    counts = completion_counts(only_false)
    assert counts == {5: 0}
    assert top_users(counts) == []


def test_variant_selection():
    todos = [
        {"id": 1, "userId": 5, "title": "Ввод", "completed": True},
        {"id": 2, "userId": 5, "title": "Циклы", "completed": False},
        {"id": 3, "userId": 10, "title": "Строки", "completed": True},
        {"id": 5, "userId": 5, "title": "Списки", "completed": True}
    ]
    # Вариант 1 - все задачи пользователя 5
    res = select_tasks(todos, 5)
    assert [t["id"] for t in res] == [1, 2, 5]

    # Неизвестный пользователь
    assert select_tasks(todos, 999) == []


if __name__ == "__main__":
    test_validate_todos_valid()
    test_validate_todos_invalid()
    test_completion_and_leaders()
    test_empty_and_zero_leaders()
    test_variant_selection()
    print("Все тесты для работы 11 успешно пройдены")
