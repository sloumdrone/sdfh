<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        % include('header.tpl')
        <ul class="user_list_holder">
            % if len(user_list) > 0:
                % for usr in user_list:
                    <li><a href="/directory/show/{{usr}}">{{usr}}</a>
                        % if usr == user:
                            <span> (self)</span>
                        % end
                    </li>
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
