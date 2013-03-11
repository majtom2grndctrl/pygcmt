<!DOCTYPE html PUBLIC>
<html>

<head>
	<title>Login to {{site_title}}</title>
	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>
    <h1>Login to {{site_title}}</h1>
	<form action="/manage/login" method="POST">
        <dl>
            <dt><label for="username">Email</label></dt>
            <dd><input type="text" id="username" name="username" /></dd>
            <dt><label for="password">Password</label></dt>
            <dd><input type="password" id="password" name="password" /></dd>
        </dl>
        <input type="submit" value="Login" />
    </form>
</body>

</html>
