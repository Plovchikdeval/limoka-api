import ast
import requests


def get_githubusercontent(git: str):
    # https://raw.githubusercontent.com/vsecoder/hikka_modules/main/full.txt
    if git.startswith("https://github.com/"):
        git = git.replace("https://github.com/", "https://raw.githubusercontent.com/")

    if git.endswith("/"):
        git += "main"
    else:
        git += "/main"

    return git

def get_git_modules(git: str):
    git = get_githubusercontent(git)

    req = requests.get(f"{git}/full.txt")

    if req.status_code == 200:
        return req.text.split("\n")
    else:
        return None


def get_module(module_name: str, git: str):
    try:
        git = get_githubusercontent(git)
        req = requests.get(f"{git}/{module_name}.py")
        return req.text
    except Exception as e:
        print(e)
        return ""


def get_module_info(module_content):
    meta_info = {"pic": None, "banner": None}
    # Извлечение мета-информации из комментариев
    for line in module_content.split("\n"):
        # Если строка начинается с "# meta", то это мета-информация
        if line.startswith("# meta"):
            # Извлечение ключа и значения
            key, value = line.replace("# meta ", "").split(": ")
            meta_info[key] = value

    # Парсинг файла в абстрактное синтаксическое дерево
    tree = ast.parse(module_content)

    def get_decorator_names(decorator_list):
        """Извлечение имен декораторов из списка."""
        return [ast.unparse(decorator) for decorator in decorator_list]

    result = {}
    # Проход по всем узлам дерева
    for node in ast.walk(tree):
        # Если узел - это определение класса
        if isinstance(node, ast.ClassDef):
            # Если не Mod, то пропускаем
            if "Mod" not in node.name:
                continue

            # Извлечение докстринга класса
            class_docstring = ast.get_docstring(node)

            # Подготовка записи для класса
            class_info = {
                "name": node.name,
                "description": class_docstring,
                "meta": meta_info,
                "commands": [],
            }

            # Проход по элементам класса (методам и атрибутам)
            for class_body_node in node.body:
                # Если узел - это обычная функция или асинхронная функция
                if isinstance(class_body_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Извлечение декораторов
                    decorators = get_decorator_names(class_body_node.decorator_list)

                    # Если у функции нет декоратора loader.command или cmd в названии, то пропускаем
                    is_loader_command = [
                        decorator for decorator in decorators if "command" in decorator
                    ]
                    if not is_loader_command and "cmd" not in class_body_node.name:
                        continue

                    # Извлечение докстринга метода
                    method_docstring = ast.get_docstring(class_body_node)

                    # Добавление информации о методе
                    class_info["commands"].append(
                        {class_body_node.name: method_docstring}
                    )

            # Записываем результат
            result = class_info

    return result
