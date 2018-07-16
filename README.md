[![Build Status](https://travis-ci.com/Ivana-/Liscript-Python.svg?branch=master)](https://travis-ci.com/Ivana-/Liscript-Python)
[![Build Status](https://codecov.io/gh/Ivana-/Liscript-Python/branch/master/graph/badge.svg)](https://codecov.io/gh/Ivana-/Liscript-Python)

# Liscript-Python

Реализация интерпретатора Liscript на Python, консольный REPL

Запуск: `python3 repl.py` , автоматически подгружается стандартная библиотека

Пример интерфейса и простейших команд, детальнее в  [краткое описание языка](https://github.com/Ivana-/Liscript-GUI-Java-Swing/wiki/Liscript-short-overview):
```
t >>> def x 1
OK
t >>> + x 4
5
t >>> cons 1 2 3 4 5
(1 2 3 4 5)
t >>> map (lambda (i) * 10 i) (list-from-to 1 5)
(10 20 30 40 50)
```
Префикс `t` в подсказке ввода сигнализирует включенный режим `TCO` - оптимизации хвостовых вызовов. Режим без оптимизации - префикс `n`

Файлы с расширением `.liscript` - тескты скриптов для загрузки в интерпретатор: `:l demo1.liscript`

REPL воспринимает ввод либо как команды (если введенная строка начинается с символа `:`), либо как выражение для вычисления (во всех остальных случаях)

##### Команды РЕПЛа:

  - `:q` - выход
  - `:l filename` - загрузить файл скрипта на выполнение
  - `:tco` - переключение флага TCO (оптимизация хвостовой рекурсии)
  - `:stat` - переключение флага вывода статистики (глубина стека и количество вызовов эвал-функции)
  - `:` - повтор последней команды

##### Ссылки:

  - [краткое описание языка](https://github.com/Ivana-/Liscript-GUI-Java-Swing/wiki/Liscript-short-overview)
  - [домашняя страничка проекта](http://liscript.herokuapp.com/)
  - [онлайн REPL](http://liscript.herokuapp.com/repl)
  - [REPL-боты в различных мессенжерах](http://liscript.herokuapp.com/bots-about)
  - [реализация на Java](https://github.com/Ivana-/Liscript-GUI-Java-Swing)
  - [реализация на Haskell](https://github.com/Ivana-/Liscript)
  - [реализация на 1С](https://github.com/Ivana-/Liscript-1C)
  - [серия онлайн-стримов по реализации](https://www.youtube.com/channel/UCNFKlZ6uhl4kWfQyXk-jCvg)
  - [пример игры на Java-реализации интерпретатора](https://ivanov-andrey.itch.io/labyrinth)
