<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700" rel="stylesheet">
        <link rel="stylesheet" href="../../library/main.css">
    </head>
    <body>
        % include('header.tpl')

        <ul class="event_list_holder">
            recently posted events
            % if len(data['events']) > 0:
                % for event in event_list:
                    % event_date = datetime.datetime.fromtimestamp(float(event['event_date']))
                    <li><a href="/events/show/{{event['event_id']}}">{{event['event_title'].lower()}} <span class="date">{{event_date.strftime('%m-%d-%Y')}}</span><br><span class="location"> {{event['event_location'].lower()}}</span></a></li>
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


<!-- this page still needs to be built, it is just a shell -->
