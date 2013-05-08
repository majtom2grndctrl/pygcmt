<form id="gcmtBlogPostForm">
    <div class="gcmtIoMain">

        <dl class="gcmtIoField gcmtIoTitle " id="title_field">
            <dt><label for="title">Title</label></dt>
            <dd>
                <input type="text" id="title" name="title" value="{{post['title']}}" placeholder="Click here to add a headline">
            </dd>
        </dl>

        <dl class="gcmtIoField gcmtIoContent " id="content_field">
            <dt><label for="content">Content</label></dt>
            <dd>
                <textarea id="content" name="content" >{{post['content']}}</textarea>
            </dd>
        </dl>

    </div>
    <div class="gcmtIoSidebar">

        <dl class="gcmtIoField gcmtIoTeaser " id="teaser_field">
            <dt><label for="teaser">Teaser (Optional)</label></dt>
            <dd>
                <textarea id="teaser" name="teaser" >{{post['content']}}</textarea>
            </dd>
        </dl>

        <dl class="gcmtIoField gcmtIoText " id="published_field">
            <dt><label for="published">Date</label></dt>
            <dd>
                <input type="date" id="published" name="published" value="" >
            </dd>
        </dl>

            <dl class="gcmtIoField gcmtIoText " id="slug_field">
                <dt><label for="slug">Slug</label></dt>
                <dd>
                <input type="text" id="slug" name="slug" value="{{post['slug']}}" >
            </dd>

        </dl>
        <input type="hidden" name="id" value="{{post['id']}}" />
        <button type="submit">Save</button>

    </div>
</form>
