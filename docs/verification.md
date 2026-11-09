# Как проверить работу

ПОДГОТОВКА

Распакуйте всю папку practice2-variant31, например на рабочий стол.
Внутри ubuntu-deps-variant31 находится готовая программа.
stages содержит отдельные версии этапов. tools содержит переносной
Graphviz для Windows. Его не нужно устанавливать в систему.

В PowerShell перейдите в папку готовой программы:

    cd "C:\Users\etadl\Desktop\practice2-variant31\ubuntu-deps-variant31"
    $env:PYTHON_EXE = "C:\Users\etadl\AppData\Local\Programs\Python\Python314\python.exe"

Путь в первой команде замените, если распаковали в другое место.
Переменную PYTHON_EXE достаточно задать один раз в новом терминале.
Нужен Python 3.10+. Сборка и установка Python-библиотек не требуются.
Команды ниже вводятся именно в PowerShell, не в эмулятор первой работы.

ПРОВЕРКА БЕЗ ИНТЕРНЕТА

    .\test.bat

В конце должно быть OK, без FAILED и ERROR.
Тесты проверяют параметры, чтение Ubuntu, циклы, фильтры, глубину,
обратные связи, DOT, реальные PNG, запуск CLI, HTTP и ошибки.
HTTP проверяется на локальном тестовом сервере, без внешнего интернета.

    .\run.bat --package A --repo examples/tree.json --test-repo --ascii --output output/tree.png

Ожидаемое дерево:

    A
    |-- B
    |   `-- D
    `-- C

Откройте рисунок:

    Invoke-Item .\output\tree.png

Проверьте ограничение глубины:

    .\run.bat --package A --repo examples/tree.json --test-repo --max-depth 1 --ascii --output output/depth1.png

Должны остаться A, B, C. Пакет D исчезнет.

Проверьте фильтр:

    .\run.bat --package A --repo examples/tree.json --test-repo --exclude B --ascii --output output/filtered.png

Должны остаться A и C. Ветвь B-D исключается.

Проверьте цикл:

    .\run.bat --package A --repo examples/cycle.json --test-repo --max-depth 10 --ascii --output output/cycle.png

Программа завершится. В дереве будет отметка cycle, на рисунке — цикл.
Для автоматического прогона этих случаев:

    .\scripts\demo_test.bat

ПРОВЕРКА НАСТОЯЩИХ ПАКЕТОВ

    .\scripts\demo_real.bat

Нужен интернет. Создаются bash.png, grep.png, sed.png в output.
Рядом сохраняются DOT-файлы с описанием тех же графов.
Данные берутся из Ubuntu 24.04, main, amd64.

Для этого индекса прямые зависимости:

- bash: base-files, debianutils, libc6, libtinfo6.
- grep: libc6, libpcre2-8-0.
- sed: libacl1, libc6, libselinux1.

В демонстрации глубина равна 2, поэтому на рисунке будут также
зависимости этих пакетов. Версии и ограничения описаны в format.md.

ПРОВЕРКА ОШИБОК

Все семь неверных параметров можно показать одной командой:

    .\scripts\demo_errors.bat

Она должна закончиться строкой All seven invalid inputs were rejected.
Также можно выполнить отдельные примеры:

    .\run.bat --package bash --max-depth -1
    .\run.bat --package bash --output image.jpg
    .\run.bat --package A --test-repo --repo missing.json
    .\run.bat --package Z --test-repo --repo examples/tree.json
    .\run.bat --package A --test-repo --repo examples/tree.json --exclude A

Здесь сообщения об ошибке ожидаются. Длинного Traceback быть не должно.
Сразу после команды можно проверить код завершения:

    $LASTEXITCODE

0 — успешно; 1 — ошибка данных, сети или Graphviz; 2 — неверные параметры.
Вводимое имя учебного пакета должно состоять из больших латинских букв.

КАК ПРОВЕРИТЬ КАЖДЫЙ ЭТАП

Откройте терминал внутри соответствующей папки stages/stage1 и так далее.
В каждой папке есть собственный README, исходники, тесты и run.bat.
Запускайте test.bat и примеры из README именно этой версии.

1. stage1 выводит семь параметров ключ=значение.
2. stage2 выводит прямые зависимости bash; нужен интернет.
3. stage3 показывает обычный граф списком связей.
4. stage4 показывает обратный граф. Пакет D в tree.json даёт D -> B -> A.
5. stage5 создаёт DOT, PNG и при флаге --ascii текстовое дерево.

Обратные зависимости включены только в stage4, как написано в задании.
В финальном stage5 снова показываются обычные зависимости.

СРАВНЕНИЕ С APT

Этот пункт выполняется в Ubuntu или WSL с Ubuntu. Основную программу
можно запускать в Windows, но штатный apt-cache нужен для сравнения.
Откройте comparison.md: там команды, ожидаемые связи и объяснение отличий.

ЕСЛИ ЧТО-ТО НЕ ЗАПУСКАЕТСЯ

Python не найден: повторно задайте PYTHON_EXE в текущем терминале.
Graphviz not found: сохраните папку tools рядом с папкой проекта.
Если переносили только репозиторий, установите Graphviz отдельно или
укажите путь к dot.exe:

    $env:GRAPHVIZ_DOT = "C:\Program Files\Graphviz\bin\dot.exe"

Путь должен соответствовать вашей установке. Скачать Graphviz:
https://graphviz.org/download/

Ошибка сети: сначала проверьте учебный режим. Для реального индекса
нужен доступ к archive.ubuntu.com; проверьте интернет и VPN.
Входные JSON-файлы программа не изменяет. Команды vfs-init здесь нет.
