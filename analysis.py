def validate_todos(data):
    if not isinstance(data, list):
        raise ValueError("Корень JSON должен быть списком")

    seen_ids = set()
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Элемент с индексом {index} не является словарём")

        if "id" not in item or type(item["id"]) is not int or item["id"] <= 0:
            raise ValueError(f"Элемент с индексом {index}: поле 'id' должно быть положительным целым числом")

        task_id = item["id"]
        if task_id in seen_ids:
            raise ValueError(f"Обнаружен дубликат идентификатора id: {task_id}")
        seen_ids.add(task_id)

        if "userId" not in item or type(item["userId"]) is not int or item["userId"] <= 0:
            raise ValueError(f"Элемент с индексом {index}: поле 'userId' должно быть положительным целым числом")

        if "title" not in item or type(item["title"]) is not str or not item["title"]:
            raise ValueError(f"Элемент с индексом {index}: поле 'title' должно быть непустой строкой")

        if "completed" not in item or type(item["completed"]) is not bool:
            raise ValueError(f"Элемент с индексом {index}: поле 'completed' должно быть логического типа")


def completion_counts(todos):
    counts = {}
    for task in todos:
        user_id = task["userId"]
        if user_id not in counts:
            counts[user_id] = 0
        if task["completed"]:
            counts[user_id] += 1
    return counts


def top_users(counts):
    if not counts:
        return []
    max_completed = max(counts.values())
    if max_completed == 0:
        return []
    leaders = []
    for user_id in sorted(counts.keys()):
        if counts[user_id] == max_completed:
            leaders.append(user_id)
    return leaders


def select_tasks(todos, user_id, parameter=None):
    selected = []
    for task in todos:
        if task["userId"] == user_id:
            selected.append(task)
    return selected
