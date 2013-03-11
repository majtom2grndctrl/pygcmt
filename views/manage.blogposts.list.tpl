%for post in blogposts:
    <li>
        <button class="gcmtBlogpostNav" onclick="manage.loadBlogPost({{post['id']}})">
            <span class="gcmtBlogpostTitle">{{post['title']}}</span>
            <span class="gcmtBlogpostDate">{{post['date']}}</span>
        </button>
    </li>
%end
