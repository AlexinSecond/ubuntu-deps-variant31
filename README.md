# Практическая работа 2. Вариант 31. Этап 4

Этот этап показывает обратные зависимости: кто использует данный пакет.
Если A зависит от B, то обратная связь для B ведёт к A.
Сначала переворачиваются все связи, затем выполняется тот же DFS.

ЗАПУСК

Нужен Python 3.10+. Откройте PowerShell в этой папке.

    .\run.bat --package D --repo examples/tree.json --test-repo

Ожидается цепочка D -> B -> A. Это означает: B использует D, A использует B.
Если Python не найден, укажите путь и повторите запуск:

    $env:PYTHON_EXE = "C:\Users\etadl\AppData\Local\Programs\Python\Python314\python.exe"

В Linux: sh run.sh с теми же параметрами.

ПРОВЕРКА РАЗНЫХ СЛУЧАЕВ

    .\test.bat
    .\run.bat --package D --repo examples/tree.json --test-repo --max-depth 1
    .\run.bat --package D --repo examples/tree.json --test-repo --exclude B
    .\run.bat --package A --repo examples/cycle.json --test-repo --max-depth 10
    .\run.bat --package A --repo examples/tree.json --test-repo

Глубина 1 даёт D -> B. Фильтр B оставляет только D.
Циклический граф даёт A -> C -> B -> A и не зависает.
Последний пример показывает A без потребителей.

ПАРАМЕТРЫ

--package задаёт пакет, --repo задаёт URL индекса Ubuntu или учебный JSON.
--test-repo включает учебный режим без интернета.
--max-depth задаёт глубину 0..100, по умолчанию 3.
--exclude исключает имена с данной подстрокой, регистр важен.
--output задаёт имя PNG, --ascii включает дерево; они нужны на этапе 5.
--help показывает справку. Флаги вводятся без значений true или yes.
Учебный JSON: {"A": ["B"], "B": []}. Все узлы объявляются явно.

НАСТОЯЩИЙ ПАКЕТ

    .\run.bat --package bash --max-depth 2

По умолчанию читается индекс Ubuntu 24.04, main, amd64; нужен интернет.
Потребители ищутся только внутри выбранного индекса.
Подробности формата и ограничений: docs/format.md.

КОД

src/reverse.py переворачивает связи, src/graph.py выполняет обход.
src/config.py проверяет настройки. src/download.py загружает индекс.
src/packages.py разбирает поля. src/repository.py выбирает источник.
src/__main__.py запускает программу. tests содержит тесты.
Сборка и сторонние Python-библиотеки не нужны.
В Linux тесты запускаются так: python3 -m unittest discover -s tests -v.

Обратные зависимости выводятся именно в версии stage4, как требует задание.
В этапе 5 программа снова строит обычные зависимости и рисует их.

Проверка ошибок всех семи параметров:

    .\scripts\demo_errors.bat
