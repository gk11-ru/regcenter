%import time
<p>Пользователь: <b>{{user}}</b></p>
<p>Адрес: <b>{{addr}},{{uid}}</b></p>
<p>Дата регистрации: {{time.strftime('%d %m %Y %H:%M', time.gmtime(int(ts)))}} UTC</p>

<hr>

<form method="post" action="{{forumurl}}">
<input type="submit" value="Войти на форум gk11.ru">
<input type="hidden" name="kvitok" value="{{kvitok}}">
</form>

<hr>

<p>Квиток на регистрацию:</p>
<p><input type="text" style="width:100%" value=":{{kvitok}}:"></p>