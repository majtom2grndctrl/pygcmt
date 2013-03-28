<h1>Blog posts:</h1>
%for post in blogposts:
    <h2>{{post['title']}}</h2>
    <div>{{post['date']}}</div>
    <div>
        {{post['content']}}
    </div>
%end
