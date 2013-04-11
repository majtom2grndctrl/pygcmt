<h1>{{site_title}}</h1>
%for post in blogposts:
    <h2>{{post['title']}}</h2>
    <div>{{post['date']}}</div>
    <div>
        {{post['content']}}
    </div>
%end
