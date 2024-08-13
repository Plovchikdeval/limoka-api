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
    git = get_githubusercontent(git)

    req = requests.get(f"{git}/{module_name}.py")

    if req.status_code == 200:
        return req.text
    else:
        return []


def get_module_info(code: str):
    commands = []
    pic = None
    banner = None
    description = None

    last_line = None

    desc_parser_active = False
    for line in code.split("\n"):
        if line.startswith("# meta"):
            line = line.replace("# meta", "").strip()
            key, value = line.split(":", 1)
            value = value.strip()

            if key == "pic":
                pic = value
            elif key == "banner":
                banner = value
            elif key == "description":
                description = value

        line = " ".join(line.split())

        if "async def" in line and "cmd" in line or "class" in line and "Mod" in line:
            desc_parser_active = True
            if "async def" in line:
                commands.append(
                    {
                        "command": line.split("async def ")[1].split("cmd")[0],
                        "description": None,
                    }
                )
            continue

        if desc_parser_active and "#" in line:
            if commands:
                commands[-1]["description"] = line.split("#")[1].strip()
            else:
                description = line.split("#")[1].strip()
            desc_parser_active = False

        if "\"\"\"" in line:
            text = None
            if description:
                if description.replace("\n", "") == "":
                    description = ""
            check = commands[-1]["description"] if commands else description
            if line.count("\"\"\"") == 2:
                text = line.replace("\"\"\"", "")
                desc_parser_active = False
            else:
                if check and '"""' in line:
                    desc_parser_active = False

            if commands:
                commands[-1]["description"] = f"{commands[-1]['description'] if commands[-1]['description'] else ''}{text if text else ''}\n"
            else:
                description = f"{description if description else ''}{text if text else ''}\n"

        elif "\"\"\"" not in line and desc_parser_active:
            last = commands[-1]["description"] if commands else description
            text = f"{last if last else ''}\n{line}"
            if commands:
                commands[-1]["description"] = text if text else ""
            else:
                description = text if text else ""

    while description and description.startswith("\n"):
        description = description[1:]

    for command in commands:
        while command["description"] and command["description"].startswith("\n"):
            command["description"] = command["description"][1:]

    return {
        "pic": pic,
        "banner": banner,
        "description": description,
        "commands": commands
    }
