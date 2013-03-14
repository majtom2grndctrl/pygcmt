define([
    "dojo/dom", "dojo/query", "dojo/dom-construct", "dojo/request", "dojo/json", "dojo/_base/array", "dojo/on", "dojox/validate", "dojo/html"
], function(dom, query, domConstruct, request, json, arrayUtil, on, validate, html) {

    return {

        pageInit: function() {
            domConstruct.destroy(dom.byId("gcmt-JsRequired"));
            this.loadNavBar(0);
        },

        loadNavBar: function(page) {
            var sidebarList = dom.byId("gcmtMainSidebarList");
            var destroyFunction = function() {
                manage.destroyEditor();
            }
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
                            request("/manage/blogposts/editor").then(
                                function(editor) {
                                    html.set(dom.byId("gcmtMainWorkspaceContainer"), editor, { parseContent: true });
                                }
                            );
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
            console.log("Foo");
        },
        destroyEditor: function() {
            domConstruct.empty(dom.byId("gcmtMainWorkspaceContainer"));
        },
    };
});
