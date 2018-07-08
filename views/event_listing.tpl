<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        % include('header.tpl')
        % import datetime
        % if len(event) > 0:
            % event = event[0]
            % if user == event['creator']:
                <div class="add_event"><a href="/edit_event">edit_event()</a></div>
            % end
            % event_date = datetime.datetime.fromtimestamp(float(event['date']))
            <ul class="nostyle">
                <li><span>title</span> {{event['title']}}</li>
                <li><span>date</span> {{event['date']}}</li>
                <li><span>location</span> {{event['location']}}</li>
                <li><span>creator</span> {{event['creator']}}</li>
                <li><span>description</span> {{event['description']}}</li>
            </ul>

        % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
