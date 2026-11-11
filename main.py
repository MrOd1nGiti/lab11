import json
from pathlib import Path
from analysis import completion_counts, select_tasks, top_users, validate_todos


def read_positive_integer(prompt):
    while True:
        raw_val = input(prompt).strip()
        try:
            val = int(raw_val)
        except ValueError:
            print("Ошибка: введено не целое число")
            continue

        if val <= 0:
            print("Ошибка: число должно быть больше нуля")
            continue

        return val


def main():
    folder = Path(__file__).resolve().parent
    todos_path = folder / "todos.json"
    leaders_path = folder / "leaders.json"
    selected_path = folder / "selected.json"

    try:
        with open(todos_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл {todos_path.name} не найден")
        return
    except UnicodeError:
        print("Ошибка: неверная кодировка файла. Ожидается UTF-8")
        return
    except json.JSONDecodeError as error:
        print(f"Ошибка синтаксиса JSON: {error}")
        return
    except OSError as error:
        print(f"Ошибка доступа к файлу: {error}")
        return

    try:
        validate_todos(data)
    except ValueError as error:
        print(f"Ошибка структуры данных: {error}")
        return

    counts = completion_counts(data)
    leaders = top_users(counts)

    print("Статистика завершённых задач по пользователям:")
    for user_id in sorted(counts.keys()):
        print(f"Пользователь {user_id} - {counts[user_id]} завершённых задач")

    leaders_str = ", ".join(str(u) for u in leaders) if leaders else "Нет лидеров"
    print(f"Лидеры - {leaders_str}")

    leader_task_ids = []
    for task in data:
        if task["userId"] in leaders and task["completed"]:
            leader_task_ids.append(task["id"])

    try:
        with open(leaders_path, "w", encoding="utf-8") as file:
            json.dump(leader_task_ids, file, ensure_ascii=False, indent=2)
        print(f"Результаты лидеров сохранены в {leaders_path.name}")
    except OSError as error:
        print(f"Ошибка записи leaders.json: {error}")

    target_user_id = read_positive_integer("Введите ID пользователя для выборки: ")
    user_tasks = select_tasks(data, target_user_id)
    selected_task_ids = [task["id"] for task in user_tasks]

    try:
        with open(selected_path, "w", encoding="utf-8") as file:
            json.dump(selected_task_ids, file, ensure_ascii=False, indent=2)
        print(f"Выборка задач пользователя сохранена в {selected_path.name}")
    except OSError as error:
        print(f"Ошибка записи selected.json: {error}")


if __name__ == "__main__":
    main()
