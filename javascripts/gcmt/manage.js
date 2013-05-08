define([
    "dojo/dom", "dojo/query", "dojo/dom-construct", "dojo/request", "dojo/json", "dojo/_base/array", "dojo/on", "dojox/validate", "dojo/html", "dojo/dom-form"],
    function(dom, query, domConstruct, request, json, arrayUtil, on, validate, html, domForm) {

    return {

        pageInit: function() {
            domConstruct.destroy(dom.byId("gcmt-JsRequired"));
            this.loadNavBar(0);
            loadFunction = this.loadBlogEditor;

            var blogPostForm = dom.byId("gcmtBlogPostForm");
            on(blogPostForm, "submit", function(event) {
                event.stopPropagation();
                event.preventDefault();

                request.post("/manage/blogposts/save", {
                    data: domForm.toObject("gcmtBlogPostForm"),
                    timeout: 5000
                }).then(function(response){
//
                    alert(response);
                });

            });
            console.log("Init method completed");
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
    };
});
