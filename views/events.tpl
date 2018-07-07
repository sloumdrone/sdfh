<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        % include('header.tpl')
        <div class="add_event"><a href="#">add_event()</a></div>
        <ul class="event_list_holder">
            % if len(event_list) > 0:
                % for event in event_list:
                    <li><a href="/event/{{event_id}}">{{event_title.lower()}} <span class="date">{{event_date}}</span><br><span class="location"> {{event_location.lower()}}</span></a></li>
                    <li>--</li>
                % end
             % else:
                <li>there are no events scheduled</li>
             % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
