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
        % import datetime
        % event = event[0]
        % event_date = datetime.datetime.fromtimestamp(float(event['date']))
        <form action="/edit_event" method="post" autocomplete="off" id="add_event" enctype="text/html">
            <input type="text" name="event_title" placeholder="event name" value="{{event['title']}}" required><br>
            <input type="text" name="event_location" placeholder="event location" value="{{event['location']}}" required><br>
            <input type="text" name="event_date" placeholder="date/time: mm-dd-yyyy" required pattern="^\d{1,2}\-\d{1,2}\-[1-2][0-9]{3}$" title="mm-dd-yyyy" value="{{event_date.strftime('%m-%d-%Y')}}"><br>
            <textarea name="event_description" placeholder="event description" rows="8" cols="80">{{!event['description']}}</textarea><br><br>
            <input type="hidden" name="event_creator" value="{{user}}">
            <input type="hidden" name="event_id" value="{{event_id}}">
            <input type="submit" value="execute">
        </form>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
