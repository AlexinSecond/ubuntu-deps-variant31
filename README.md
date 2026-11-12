Практическая работа 2. Вариант 31

Программа показывает зависимости пакетов Ubuntu. Она читает индекс Packages или учебный JSON, обходит связи рекурсивным DFS и сохраняет граф в DOT и PNG. По желанию выводит текстовое дерево.

Программа не устанавливает пакеты и не изменяет входные JSON-файлы. Каждый запуск выполняет одну задачу и завершается.

Подготовка

Нужен Python 3.10 или новее. Для создания PNG нужен Graphviz. Дополнительные библиотеки Python и сборка проекта не требуются.

Все команды для Windows ниже вводятся в PowerShell, открытом в папке проекта. Не нужно вводить перед ними текст приглашения PS C:\...>.

На этом компьютере перейти в папку можно так:

    cd "C:\Users\etadl\Desktop\vuz\sem3\cfg\ubuntu-deps-variant31"

Если Python не находится автоматически, укажите установленный интерпретатор:

    $env:PYTHON_EXE = "C:\Users\etadl\AppData\Local\Programs\Python\Python314\python.exe"

Если Graphviz не найден, задайте полный путь к своему dot.exe. Например, при обычной установке:

    $env:GRAPHVIZ_DOT = "C:\Program Files\Graphviz\bin\dot.exe"

Путь зависит от места установки. В комплекте работы также есть переносной Graphviz в папке tools. Если сохранить структуру комплекта, программа найдёт его автоматически.

Настройки переменных действуют в текущем терминале. В новом окне их при необходимости нужно задать снова.

Справка

    .\run.bat --help

Короткая форма той же команды:

    .\run.bat -h

Все параметры запуска

--package задаёт исходный пакет. Это обязательный параметр.

--repo задаёт URL индекса Packages, Packages.gz, Packages.xz или папки, содержащей Packages.xz. В учебном режиме указывается путь к JSON-файлу.

--test-repo включает учебный режим. Имена пакетов в JSON должны состоять из больших латинских букв. Все упомянутые пакеты должны быть объявлены в файле.

--output задаёт путь к рисунку PNG. По умолчанию output/graph.png. Рядом сохраняется DOT-файл с таким же именем.

--ascii включает вывод текстового дерева в терминал. Без него программа сохраняет файлы и выводит сведения о результате.

--max-depth задаёт глубину от 0 до 100. По умолчанию 3. Корень имеет глубину 0, прямые зависимости — 1. При разных путях учитывается кратчайший.

--exclude исключает пакеты, имена которых содержат указанную подстроку. Регистр важен. По умолчанию фильтр выключен. Исключение самого исходного пакета считается ошибкой.

--help или -h выводит справку.

Флаги --test-repo и --ascii вводятся без значений yes или true. Символы -- являются частью команд, их нужно сохранять.

Обычный учебный граф

    .\run.bat --package A --repo examples/tree.json --test-repo --ascii --output output/tree.png

A зависит от B и C. B зависит от D. Поэтому D является транзитивной зависимостью A.

Открыть рисунок:

    Invoke-Item .\output\tree.png

Посмотреть текстовое описание графа:

    Get-Content .\output\tree.dot

Только исходный пакет

    .\run.bat --package A --repo examples/tree.json --test-repo --max-depth 0 --ascii --output output/root.png

В результате будет только A.

Только прямые зависимости

    .\run.bat --package A --repo examples/tree.json --test-repo --max-depth 1 --ascii --output output/depth1.png

В результате будут A, B и C. Пакета D не будет.

Фильтр по имени

    .\run.bat --package A --repo examples/tree.json --test-repo --exclude B --ascii --output output/filtered.png

Останутся A и C. Ветвь B и её зависимость D исключается.

Циклические зависимости

    .\run.bat --package A --repo examples/cycle.json --test-repo --max-depth 10 --ascii --output output/cycle.png

В графе есть цикл A -> B -> C -> A. Программа не зависает. В текстовом дереве появляется отметка cycle.

    Invoke-Item .\output\cycle.png

Разные пути к одному пакету

    .\run.bat --package A --repo examples/diamond.json --test-repo --max-depth 3 --ascii --output output/diamond.png

К D ведут пути разной длины. При более коротком пути программа повторно рассматривает его зависимости, поэтому E не теряется.

Отдельные компоненты графа

    .\run.bat --package A --repo examples/disconnected.json --test-repo --ascii --output output/disconnected.png

Показываются только A и B. Недостижимые из A пакеты C, D и E в результат не входят.

Пакет без зависимостей

    .\run.bat --package E --repo examples/disconnected.json --test-repo --ascii --output output/isolated.png

В результате будет один узел E.

Рисунок без текстового дерева

    .\run.bat --package A --repo examples/tree.json --test-repo --output output/image.png

Создаются DOT и PNG. Дерево в терминал не выводится, потому что нет --ascii.

Настоящий пакет Ubuntu

    .\run.bat --package bash --max-depth 2 --ascii --output output/bash.png

Нужен интернет. По умолчанию читается индекс Ubuntu 24.04, компонент main, архитектура amd64.

    Invoke-Item .\output\bash.png

Явное указание адреса репозитория

    .\run.bat --package bash --repo https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz --max-depth 2 --ascii --output output/bash.png

Фильтр для настоящих пакетов

    .\run.bat --package bash --max-depth 2 --exclude libc --ascii --output output/bash-filtered.png

Имена с подстрокой libc будут исключены.

Три настоящих пакета одной командой

    .\scripts\demo_real.bat

Создаются рисунки bash.png, grep.png и sed.png в папке output. Нужен интернет.

Все учебные демонстрации одной командой

    .\scripts\demo_test.bat

Проверяются цикл, ограничение глубины, фильтр и разные пути к общему узлу. Интернет не нужен.

Автоматические тесты

    .\test.bat

В подготовленной финальной версии 39 тестов. В конце должно появиться OK. Для проверки создания рисунков нужен Graphviz. Внешний интернет не нужен: HTTP проверяется на локальном тестовом сервере.

Прямой запуск тестов через выбранный Python:

    & $env:PYTHON_EXE -m unittest discover -s tests -v

Демонстрация ошибок всех параметров

    .\scripts\demo_errors.bat

Сообщения об ошибках здесь ожидаются. В конце должна появиться строка All seven invalid inputs were rejected.

Этот же скрипт можно запустить напрямую:

    & $env:PYTHON_EXE scripts/demo_errors.py

Отдельные примеры неправильного ввода

Несуществующий пакет:

    .\run.bat --package Z --repo examples/tree.json --test-repo

Несуществующий файл:

    .\run.bat --package A --repo missing.json --test-repo

Отрицательная глубина:

    .\run.bat --package bash --max-depth -1

Неправильное расширение рисунка:

    .\run.bat --package bash --output graph.jpg

Исключение исходного пакета:

    .\run.bat --package A --repo examples/tree.json --test-repo --exclude A

После любого запуска код завершения можно посмотреть командой:

    $LASTEXITCODE

0 означает успех. 1 означает ошибку данных, сети или Graphviz. 2 означает неправильные параметры запуска.

Проверка отдельных этапов

Следующие команды выполняются в папке соответствующей версии. Финальная программа не переключает этапы параметрами.

В папке stage1:

    .\run.bat --package bash

Показывает семь настроек в формате ключ=значение.

В папке stage2:

    .\run.bat --package bash

Показывает прямые зависимости bash из Ubuntu. Нужен интернет.

В папке stage3:

    .\run.bat --package A --repo examples/tree.json --test-repo

Показывает граф обычных зависимостей списком связей.

В папке stage4:

    .\run.bat --package D --repo examples/tree.json --test-repo

Показывает обратные зависимости: D -> B -> A. Это означает, что B использует D, а A использует B.

Обратные зависимости только первого уровня в stage4:

    .\run.bat --package D --repo examples/tree.json --test-repo --max-depth 1

Останется связь D -> B.

Обратные зависимости с фильтром в stage4:

    .\run.bat --package D --repo examples/tree.json --test-repo --exclude B

Останется только D.

В stage5 работают примеры с рисунками, приведённые выше. В каждой версии тесты запускаются через test.bat, но их количество зависит от этапа.

Linux и macOS

Вместо run.bat используется run.sh. Нужны Python 3 и Graphviz для своей системы.

    sh run.sh --package A --repo examples/tree.json --test-repo --ascii

    python3 -m unittest discover -s tests -v

    python3 scripts/demo_errors.py

    sh scripts/demo_real.sh

В Windows запуск без run.bat возможен из корня проекта:

    & $env:PYTHON_EXE -m src --package A --repo examples/tree.json --test-repo --ascii

Сравнение с APT

Этот пункт выполняется в Ubuntu или WSL с Ubuntu. Нужны python3, apt-cache и Graphviz.

    sh scripts/compare_apt.sh

Скрипт готовит отдельный индекс, запускает штатные средства APT и нашу программу. Результаты сохраняются в output/apt-comparison. Системные источники и установленные пакеты не изменяются.

После успешной подготовки файлов повторно проверить совпадение можно так:

    python3 -m scripts.check_apt_result output/apt-comparison

В comparison.txt должны появиться строки direct dependencies match для трёх пакетов. В исходной проверке проекта этот Linux-скрипт не выполнялся. Подробности находятся в docs/comparison.md.

Как устроена программа

src/__main__.py запускает программу и обрабатывает ошибки.
src/config.py проверяет параметры.
src/download.py скачивает и распаковывает индекс.
src/packages.py извлекает зависимости из полей Ubuntu.
src/repository.py выбирает настоящий или учебный источник.
src/graph.py обходит граф рекурсивным DFS, применяет глубину и фильтр.
src/reverse.py переворачивает связи для этапа 4.
src/visualize.py формирует DOT, PNG и текстовое дерево.

scripts содержит демонстрации и сравнение с APT.
tests содержит автоматические тесты.
examples содержит учебные графы.
output содержит результаты запусков и не включается в Git.

Обозначения и ограничения

cycle означает цикл. shown above означает, что узел уже показан. link означает связь к узлу, раскрываемому на другом уровне дерева.

На рисунке голубым выделен исходный пакет. Ромб обозначает виртуальный пакет. Пунктир provider ведёт к его поставщику. Красный пунктирный узел обозначает зависимость, отсутствующую в выбранном индексе.

Учитываются Depends и Pre-Depends. Обе альтернативы из записи aa | bb показываются в графе. Программа не выбирает версии и не рассчитывает план установки с учётом уже установленных пакетов. Recommends и Suggests не включаются.

Дополнительные пояснения находятся в docs/format.md, docs/verification.md, docs/defense.md и docs/comparison.md.
