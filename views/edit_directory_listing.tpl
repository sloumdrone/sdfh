<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700" rel="stylesheet">
        <link rel="stylesheet" href="../../library/main.css">
    </head>
    <body>
        % include('header.tpl')
        % if error:
            <aside class="error">
                error code: 37<br>
                form execution failure. check input values and try again, or contact the system administrator.
            </aside>
        % end
        <form action="/edit_directory_listing" method="post" autocomplete="off" id="add_event">
            <textarea name="bio" placeholder="bio // notes" rows="8" cols="80">{{!usr['bio']}}</textarea><br>
            <input type="text" name="tools" placeholder="available tools (comma separated list)" value="{{usr['tools']}}"><br>
            <input type="text" name="skills" placeholder="skills and proficiencies (comma separated list)" value="{{usr['skills']}}"><br><br>
            <input type="submit" value="execute">
        </form>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
