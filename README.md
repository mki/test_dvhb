Used:
* Django 1.9
* Sqlite3
* Python 3.4

Запуск:
* Запускаем ./build.sh
* Запускаем [path]/manage.py migrate
* Запускаем [path]/manage.py runserver

Реализовать бэкенд с минимальным фронтендом (можно на голом HTML).

* Имеется база стандартных пользователей Django (добавляются через админку, регистрацию делать не надо).
* У каждого пользователя есть персональный блог. Новые создавать он не может.
* Пост в блоге — элементарная запись с заголовком, текстом и временем создания.
* Пользователь может подписываться (отписываться) на блоги других пользователей (любое количество).
* У пользователя есть персональная лента новостей, в которой в обратном хронологическом порядке выводятся посты из блогов, на которые он подписан.
* Пользователь может помечать посты в ленте прочитанными.
* При добавлении/удалении подписки содержание ленты меняется (при удалении подписки пометки о "прочитанности" сохранять не нужно).
* При добавлении поста в ленту — подписчики получают почтовое уведомление со ссылкой на новый пост.
* Изменение содержания лент подписчиков (и рассылка уведомлений) должно происходить как при стандартной публикации поста пользователем через интерфейс сайта, так при добавлении/удалении поста через админку.