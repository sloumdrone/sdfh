<html>
    <head>
        <title>sdfh</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,400i,700" rel="stylesheet">
        <link rel="stylesheet" href="../../../library/main.css">
    </head>
    <body>
        % include('header.tpl')
        % if user == comment['user']:
            <div class="add_event">
                <a href="/thread/delete/{{user}}/{{comment['time']}}">delete_thread()</a>
            </div>
        % end

        % page_data = page_title.split(':')
        % form_action = page_data[0].strip()
        % parent_user = page_data[2].strip()
        % parent_time = page_data[3].strip()

        <ul class="nostyle">
            <li><span>thread initializer</span> {{comment['user']}}</li>
            <li><span>thread</span> {{!comment['comment']}}</li>
        </ul>
        <hr>
        <div class="quote">{{saying.lower()}}</div>
        <div class="commentBurger">
            <div class="rarrow"></div>
            <form class="comment" action="/add_thread/{{parent_user}}/{{parent_time}}" method="post" autocomplete="off">
                <input type="text" name="comment" value="" placeholder="add input here" autocomplete="off"><input type="submit" value="execute">
            </form>
        </div>

        <ul class="nostyle commentListing">
            % for thread in threads:
                <li><span><a href="/directory/show/{{thread['user']}}">{{thread['user']}}</a></span> {{!thread['comment']}}</li>
            % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
