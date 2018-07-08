<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        % include('header.tpl')
        % if error:
            <aside class="error">
                error code: 37<br>
                form execution failure. check input values and try again, or contact the system administrator.
            </aside>
        % end
        <form action="/new_event" method="post" autocomplete="off" id="add_event">
            <input type="text" name="event_title" placeholder="event name" required><br>
            <input type="text" name="event_location" placeholder="event location" required><br>
            <input type="text" name="event_date" placeholder="date/time: mm-dd-yyyy" required pattern="^\d{1,2}\-\d{1,2}\-[1-2][0-9]{3}$" title="mm-dd-yyyy"><br>
            <textarea name="event_description" placeholder="event description" rows="8" cols="80"></textarea><br><br>
            <input type="hidden" name="event_creator" value="{{user}}">
            <input type="submit" value="execute">
        </form>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
