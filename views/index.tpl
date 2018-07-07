<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        <header>super dev friends huzzah!</header>
        <section>
            %if loginissue:
                <div class="wordBubble">
                    invalid identity or pass key
                </div>
            %end
            <h1>sdfh</h1>
            <div class="hamburger">
                <div class="circlefill"></div>
                <form id="loginform" class="login" action="/login" method="post">
                    <input type="text" name="ident" value="" placeholder="identity"><br />
                    <input type="password" name="pass" value="" placeholder="pass key"><br />
                    <input type="submit" name="submit" value="execute">
                </form>
            </div>

        </section>
    </body>
</html>
