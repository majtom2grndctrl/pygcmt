define([
    "dojo/dom", "dojo/query", "dojo/dom-construct", "dojo/request", "dojo/json", "dojo/_base/array", "dojo/on", "dojox/validate", "dojo/html"
], function(dom, query, domConstruct, request, json, arrayUtil, on, validate, html) {

    var loadFunction = {};

    return {

        pageInit: function() {
            domConstruct.destroy(dom.byId("gcmt-JsRequired"));
            this.loadNavBar(0);
            loadFunction = this.loadEditor;
//            console.log("loadFunction defined");
        },

        loadNavBar: function(page) {
            var sidebarList = dom.byId("gcmtMainSidebarList");

            request("/manage/blogposts/json/" + page).then(
                function(response) {
                    jsonObject = JSON.parse(response);
                    console.log(jsonObject.blogposts);
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
        loadEditor: function(id) {
            request("/manage/blogposts/edit/" + id).then(
                function(editor) {
                    html.set(dom.byId("gcmtMainWorkspaceContainer"), editor, { parseContent: true });
                }
            );
//            console.log("loadEditor was run");
        },
    };
});
