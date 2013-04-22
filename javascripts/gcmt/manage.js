define([
    "dojo/dom", "dojo/query", "dojo/dom-construct", "dojo/request", "dojo/json", "dojo/_base/array", "dojo/on", "dojox/validate", "dojo/html"
], function(dom, query, domConstruct, request, json, arrayUtil, on, validate, html) {

    return {

        pageInit: function() {
            domConstruct.destroy(dom.byId("gcmt-JsRequired"));
            this.loadNavBar(0);
            loadFunction = this.loadBlogEditor;
            submitBlogpost = this.submitBlogpost;

// DAN! Turn the following into its own method next time.
            on(dom.byId("gcmtBlogPostForm"), "submit", function(evt) {
                console.log("submitBlogpost() was NOT run");
//                submitBlogpost();
                return false;
            });
        },

        loadNavBar: function(page) {
            var sidebarList = dom.byId("gcmtMainSidebarList");

            request("/manage/blogposts/json/" + page).then(
                function(response) {
                    jsonObject = JSON.parse(response);
//                    console.log(jsonObject.blogposts);
                    arrayUtil.forEach(jsonObject.blogposts, function(post, index) {
                        domConstruct.create("li", {
                            innerHTML: post.title,
                            id: "sidebar-nav-id-" + post.id
                        }, sidebarList);

                        on(dom.byId("sidebar-nav-id-" + post.id), "click", function(evt) {
                            loadFunction(post.id);
                        });
                    console.log(post.id);
                    });
                },
                function(error) {
                    console.log("Sidebar failed to download JSON")
                }
            );
        },
        loadBlogEditor: function(id) {
            request("/manage/blogposts/edit/" + id).then(
                function(editor) {
                    html.set(dom.byId("gcmtMainWorkspaceContainer"), editor, { parseContent: true });
                }
            );
        },
        submitBlogpost: function() {
            console.log("submitBlogpost function has been called");
            var dataObject = new FormData(dom.byId("gcmtBlogPostForm"));
            return false;
        },
    };
});
