<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700" rel="stylesheet">
        <link rel="stylesheet" href="../../library/main.css">
    </head>
    <body>
        % include('header.tpl')
        <ul class="event_list_holder recents">
            <li>users are talking about:</li>
            % if len(data['user_posts']) > 0:
                % for post in data['user_posts']:
                    <li><a href="/thread/show/{{post['user']}}/{{post['thread_id']}}">{{post['user']}}: {{post['comment']}}</a></li>
                % end
             % else:
                <li>there are no recent commentsor links</li>
             % end
        </ul>
        <ul class="event_list_holder recents">
            <li>recently posted events:</li>
            % if len(data['events']) > 0:
                % for event in data['events']:
                    <li><a href="/events/show/{{event['event_id']}}">{{event['title']}}</a></li>
                % end
             % else:
                <li>there are no events scheduled</li>
             % end
        </ul>
        <ul class="event_list_holder recents">
            <li>recent additions to sdfh:</li>
            % if len(data['users']) > 0:
                % for person in data['users']:
                    <li><a href="/directory/show/{{person['user']}}}}">{{person['user']}}</a></li>
                % end
             % else:
                <li>there are no recent users</li>
             % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>


<!-- this page still needs to be built, it is just a shell -->
