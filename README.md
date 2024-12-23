## Задание 
https://docs.google.com/document/d/1GKvzuQcRVdCYVpS90vg_Oi2Syk-m1qkJmr8RpU4alIw/edit?tab=t.0

## Что надо было сделать:
  1.  Написать checklist.txt
  2.  5-7 авто тестов (Frontend, Backend):
      - Frontend: Playwright№
      - Backend: no frameworks 
  4.  Все тесты должны быть асинхронными - asyncio
  5.  Придерживаться паттерна Page Object, и принципам ООП
  6.  Тест должы быть упакованы в докер контейнер
      - Результат работы контейнера : запуск тестов с отчетом в allure
      - По упавшим отчетам: должен быть скриншот и видео  (несколько отчетов должны намерено упасть) 

## Что было выполнено:
- [x] Написать checklist.txt (см. файл в репе)
- [x] 5-7 авто тестов
    /tests.py
    ```
    test_positive_user_first_attempt 
    test_positive_user_prompt
    test_after_reload_test_not_disappear
    test_widget_closing
    test_buttons_to_be_clickable_that_will_fail
    test_benchmark_for_menu
    test_benchmark_for_price
    ```
- [ ] Тесты асинхронные
- [x] Придерживаться паттерна Page Object, и принципам ООП
- [ ] Тест должы быть упакованы в докер контейнер

## Что помешало выполнить задание:
Недостаточно времени и в каких-то моментах компетенции

## Как запустить автотесты через github
1. В репе = https://github.com/curiousdenis/docker_tests переходим в Actions -> Automated tests -> Run workflow
2. По окончания выполнения тестов -> Settings -> Pages -> По ссылке переходим на генерацию отчета в allure = https://curiousdenis.github.io/docker_tests/
 
