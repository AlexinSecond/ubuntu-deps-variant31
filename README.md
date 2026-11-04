# Практическая работа 2. Вариант 31. Этап 2

Это начало программы для просмотра зависимостей пакетов Ubuntu.
Программа скачивает индекс Ubuntu и выводит прямые зависимости пакета.
Обход графа и рисунки будут добавлены на следующих этапах.

ЗАПУСК

Нужен Python 3.10 или новее. Откройте PowerShell в этой папке.

    .\run.bat --package bash

Если Python не найден, укажите путь к своему установленному Python:

    $env:PYTHON_EXE = "C:\Users\etadl\AppData\Local\Programs\Python\Python314\python.exe"

После этого повторите запуск. В Linux и macOS: sh run.sh --package bash.

ПАРАМЕТРЫ

- --package: имя пакета, обязательный параметр.
- --repo: адрес индекса Packages, Packages.gz, Packages.xz или его папки.
  По умолчанию Ubuntu 24.04, main, amd64.
- --test-repo: вместо адреса использовать файл учебного графа.
- --output: имя рисунка PNG, по умолчанию output/graph.png.
- --ascii: дополнительно показывать текстовое дерево.
- --max-depth: глубина от 0 до 100, по умолчанию 3.
- --exclude: не учитывать имена с такой подстрокой.

Флаги --test-repo и --ascii вводятся без значений yes или true.
На этапе 2 глубина, фильтр и рисунок ещё не используются. Тестовый режим появится на этапе 3.

ПРИМЕР ДЛЯ UBUNTU

    .\run.bat --package bash

Появятся прямые зависимости bash, в том числе libc6 и libtinfo6. Нужен интернет. Подробности формата и ограничения: docs/format.md.

ПРОВЕРКА

    .\test.bat
    .\run.bat --package bash --max-depth -1
    .\run.bat --package bash --output graph.jpg
    .\run.bat --package bash --ascii yes

Первая команда запускает тесты. Остальные специально показывают ошибки.
Все семь параметров проверяются в tests/test_config.py.
В Linux: python3 -m unittest discover -s tests -v.

ГДЕ ЧТО НАХОДИТСЯ

src/config.py проверяет настройки. src/__main__.py запускает программу.
tests содержит тесты, examples содержит учебный граф.
Сборка и установка дополнительных Python-библиотек не нужны.


Проверка ошибок всех семи параметров:

    .\scripts\demo_errors.bat
