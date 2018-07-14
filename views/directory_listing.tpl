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
        % if user == usr['user_ident']:
            <div class="add_event"><a href="/directory/edit/{{usr['user_ident']}}">edit_ident()</a></div>
        % end
        <ul class="nostyle">
            <li><span>user identification</span> {{usr['user_ident']}}</li>
            <li><span>bio // notes</span> {{!usr['bio']}}</li>
            % tool_list = usr['tools'].split(',')
            % if len(tool_list) > 0:
                <li>
                    <span>tools of the trade</span>
                    <ul class="sublist">
                        <li>
                            % for x in tool_list:
                                <span class="clusterListItem">{{x.strip()}}</span>
                            %end
                        </li>
                    </ul>
                </li>
            % end
            % skill_list = usr['skills'].split(',')
            % if len(skill_list) > 0:
                <li>
                    <span>skills and proficiencies</span>
                    <ul class="sublist">
                        <li>
                            % for x in skill_list:
                                <span class="clusterListItem">{{x.strip()}}</span>
                            %end
                        </li>
                    </ul>
                </li>
            % end
        </ul>
        <hr>
        % page_data = page_title.split(':')
        % form_action = page_data[0].strip()
        % form_id = page_data[2].strip()

        project ideas // links
        % if usr['user_ident'] == user:
            <div class="commentBurger">
                <div class="rarrow"></div>
                <form class="comment" action="/add_comment/{{form_action}}/{{form_id}}" method="post" autocomplete="off" enctype="text/html">
                    <input type="text" name="comment" value="" placeholder="add input here" autocomplete="off"><input type="submit" value="execute">
                </form>
            </div>
        % end
        <ul class="nostyle commentListing">
            % for index, comment in enumerate(comments,1):
                <li><span> {{index}} </span> <a href="/thread/show/{{usr['user_ident']}}/{{comment['time']}}">{{!comment['comment']}}</a></li>
            % end
        </ul>
        <footer class="hamburger">
            <div class="circlefill"></div>
            % include('general_nav.tpl')
        </footer>
    </body>
</html>
