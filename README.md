# apalii_testtask

### Test credentials:
```
Login    : 9999-8888-7777-6666
Password : 1234
```
###Description

#### Работа банкомата:

1. Начальная страница банкомата – страница ввода номера карты. Как только пользователь 
вводит номер карты и нажимает кнопку ОК, посылается запрос в базу. Если найдена 
незаблокированная карта, то переходим к странице ввода пин-кода, иначе – выводим 
страницу с сообщением об ошибке.
2. Как только пользователь вводит пин-код и нажимает ОК, введённый им пин-код 
сравнивается с пин-кодом из базы. Если коды соответствуют, то загружается страница 
«Операции», иначе – сообщение об ошибке. Пользователь может вводить неправильные 
пин-коды не более 4 раз. На четвёртый раз должна быть загружена страница с 
сообщением о блокировке карты, послан в базу запрос о блокировке карты.
3. В зависимости от того, какую операцию выберет пользователь, загружается либо страница 
«Баланс», либо «Снятие денег».
4. Если пользователь выбирает просмотр баланса, то в таблицу операций добавляется 
соответствующая запись с ID карты, временем и кодом операции.
5. Если пользователь выбрал «Снятие денег», то после ввода им в окне снятия денег суммы 
и нажатия кнопки «ОК» проверяется, не превышает ли введённая сумма остатка на счету. 
В случае превышения загружается страница сообщения об ошибке, иначе – в таблицу 
операций добавляется запись с ID карты, кодом операции и снимаемой суммой, а в 
таблице карт изменяется сумма на счету, после чего загружается страница отчёта о 
результате операции.


#### Интерфейс:

1. Страница ввода номера карты. В ней находится поле, в котором выводится номер карты, 
клавиатура ввода (цифры 0-9) кнопка «ОК» и кнопка «Очистить». Пользователю 
предлагается ввести 16-значный номер карты. Единственный возможный способ ввода – 
нажимать на кнопки с цифрами. В поле вывода номера цифры разделяются на группы по 4, 
например номер «1111111111111111» должен отображаться, как «1111-1111-1111-1111». 
При нажатии на кнопку «Очистить» введённые цифры сбрасываются.
2. Страница ввода ПИН-кода. В ней находится поле, в котором выводятся символы пин-кода, 
клавиатура ввода, кнопки «Очистить», «OK» и «Выход». Пользователю предлагается 
ввести четырёхзначный пин-код. Процедура аналогична вводу номера карты, за 
исключением того, что в поле вывода отображаются не вводимые пользователем цифры, а 
одинаковые символы пароля, например «*».При нажатии на кнопку «Очистить» введённые 
цифры сбрасываются.
3. Страница операций. Содержит 3 кнопки «Баланс», «Снять сумму», «Выход».
4. Страница баланса. Содержит информацию о номере карты, сегодняшнем числе, сумме на 
счету и две кнопки «Назад» и «Выход».
5. Страница снятия денег. Содержит поле ввода суммы, цифровую клавиатуру, кнопки 
«Очистить», «ОК» и «Выход».
6. Страница отчета о результате операции. Содержит информацию о номере карты, 
дате/времени, снятой сумме, остатке на счету, а также кнопки «Назад» и «Выход».
7. Страница сообщения об ошибке. Содержит текст сообщения и кнопку «Назад».


#### Задание:

1. Создать базу данных и все необходимые с вашей точки зрения объекты в ней для работы 
данного приложения.
2. Внести в базу данных небольшое количество тестовых данных.
3. Написать web приложение в соответствии с описанными пожеланиями заказчика.
