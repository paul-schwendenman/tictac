<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>tictac</title>
<link rel="stylesheet" href="/static/main.css" type="text/css" />
<style type="text/css">
table.tic {
	border-style: none;
	text-size: larger;
}
td.middle {
	color: #ff0000;
}
tr.middle {
	color: #00ff00;
}

</style>
</head>
<body>
<div id="body">
<table class="tic">
<tr>
<td>{{table[0]}}</td><td class="middle">{{table[1]}}</td><td>{{table[2]}}</td>
</tr>
<tr class="middle">
<td>{{table[3]}}</td><td class="middle">{{table[4]}}</td><td>{{table[5]}}</td>
</tr>
<tr>
<td>{{table[6]}}</td><td class="middle">{{table[7]}}</td><td>{{table[8]}}</td>
</tr>

</table>
{{content}}
</div>
</body>
</html>