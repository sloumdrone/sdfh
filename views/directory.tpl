<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700" rel="stylesheet">
        <link rel="stylesheet" href="../../library/main.css">
    </head>
    <body>
        % include('header.tpl')
        <ul class="user_list_holder">
            % if len(user_list) > 0:
                % for usr in user_list:
                    <li><a href="/directory/show/{{usr}}">{{usr}}</a></li>
                % end
             % else:
                <li>there are no users</li>
             % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
