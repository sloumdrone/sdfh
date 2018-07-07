<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="library/main.css">
    </head>
    <body>
        <section>
            %if loginissue:
                <div class="wordBubble">
                    invalid identity or pass key
                </div>
            %end
            <div class="logotext"><span>sdfh</span></div>
            <div class="hamburger">
                <form id="loginform" class="login" action="/login" method="post">
                    <input type="text" name="ident" value="" placeholder="identity"><br />
                    <input type="password" name="pass" value="" placeholder="pass key"><br />
                    <input type="submit" name="submit" value="execute">
                </form>
            </div>

        </section>
    </body>
</html>
