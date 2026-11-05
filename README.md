# Практическая работа 2. Вариант 31. Этап 3

Программа строит граф зависимостей рекурсивным обходом DFS.
Есть ограничение глубины, фильтр по подстроке и защита от циклов.

ЗАПУСК

Нужен Python 3.10+. Откройте PowerShell в этой папке.

    .\run.bat --package A --repo examples/tree.json --test-repo

Если Python не найден, укажите установленный Python и повторите запуск:

    $env:PYTHON_EXE = "C:\Users\etadl\AppData\Local\Programs\Python\Python314\python.exe"

В Linux: sh run.sh с теми же параметрами.
Результат: A зависит от B и C, B зависит от D. C и D — листья.
Программа выводит результат и завершается. Команд ls и exit здесь нет.

ПРОВЕРКА

    .\test.bat
    .\run.bat --package A --repo examples/tree.json --test-repo --max-depth 1
    .\run.bat --package A --repo examples/tree.json --test-repo --exclude B
    .\run.bat --package A --repo examples/cycle.json --test-repo --max-depth 10
    .\run.bat --package A --repo examples/diamond.json --test-repo --max-depth 3

Тесты должны завершиться словом OK.
Глубина 1 оставляет A, B, C; фильтр B оставляет A и C.
Цикл A-B-C-A не приводит к зависанию.
В diamond узел D достигается разными путями; его ребёнок E не теряется.

ПАРАМЕТРЫ

--package: имя пакета, обязательное.
--repo: URL индекса Packages, Packages.gz, Packages.xz или его папки.
В тестовом режиме это путь к JSON.
--test-repo: учебный режим, интернет не нужен.
--max-depth: глубина 0..100, по умолчанию 3.
--exclude: не учитывать имена с данной подстрокой, регистр важен.
--output: имя PNG; на этом этапе только проверяется.
--ascii: на этом этапе только принимается, дерево появится в этапе 5.
--help: справка. Флаги --test-repo и --ascii не требуют значений.

Корень имеет глубину 0. Если есть разные пути, учитывается кратчайший.
Исключение самого корня считается ошибкой.

Учебный файл: {"A": ["B"], "B": []}.
Все имена — большие латинские буквы. Все узлы должны быть объявлены.

НАСТОЯЩИЕ ДАННЫЕ

    .\run.bat --package bash --max-depth 2

По умолчанию Ubuntu 24.04, main, amd64. Нужен интернет.
Учитываются Depends и Pre-Depends. Подробности: docs/format.md.

КОД

src/config.py — параметры; src/download.py — загрузка.
src/packages.py — разбор Ubuntu; src/repository.py — выбор источника.
src/graph.py — рекурсивный обход; src/__main__.py — запуск.
Сборка не нужна. Сторонние Python-библиотеки не нужны.
Тесты в Linux: python3 -m unittest discover -s tests -v.

Проверка ошибок всех семи параметров:

    .\scripts\demo_errors.bat
