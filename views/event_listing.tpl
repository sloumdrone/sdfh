<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        % include('imports.tpl')
    </head>
    <body>
        % include('header.tpl')
        % import datetime
        % if error:
            <aside class="error">
                error code: 37<br>
                form execution failure. check input values and try again, or contact the system administrator.
            </aside>
        % end
        % if len(event) > 0:
            % event = event[0]
            % if user == event['creator']:
                <div class="add_event"><a href="/events/edit/{{event_id}}">edit_event()</a></div>
            % end
            % event_date = datetime.datetime.fromtimestamp(float(event['date']))
            <ul class="nostyle eventListing">
                <li><span>title</span> {{event['title']}}</li>
                <li><span>date</span> {{event_date.strftime('%m-%d-%Y')}}</li>
                <li><span>location</span> {{event['location']}}</li>
                <li><span>creator</span> {{event['creator']}}</li>
                <li><span>description</span> {{!event['description']}}</li>
            </ul>
            <hr>
            <ul class="nostyle commentListing">
                <!-- <div class="page_title section">i/o feed</div> -->
                % page_data = page_title.split(':')
                % form_action = page_data[0].strip()
                % form_id = page_data[2].strip()
                <div class="commentBurger">
                    <div class="rarrow"></div>
                    <form class="comment" action="/add_comment/{{form_action}}/{{form_id}}" method="post" autocomplete="off">
                        <input type="text" name="comment" value="" placeholder="add input here" autocomplete="off"><input type="submit" value="execute">
                    </form>
                </div>
                % for comment in comments:
                    <li><span><a href="/directory/show/{{comment['user']}}">{{comment['user']}}</a></span> {{!comment['comment']}}</li>
                % end
            </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
