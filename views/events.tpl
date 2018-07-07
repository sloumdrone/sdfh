<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="library/main.css">
    </head>
    <body>
        <header class="logotext"><span>sdfh</span></header>
        <h2 class="page_title">events</h2>
        <a href="#"><div class="add_event">add_event</div></a>
        <ul class="list_holder">
            % if len(event_list) > 0:
                % for event in event_list:
                    <a href="/event/{{event_id}}"><li class="list_row"># {{event_title.lower()}} <span class="date">{{event_date}}<br><span class="location">## {{event_location.lower()}}</span> </span></li></a>
                % end
             % else:
                <li class="list_row">// there are no events scheduled</li>
             % end
        </ul>
        <footer class="hamburger">
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
