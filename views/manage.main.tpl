<!DOCTYPE html>
<html>
  <head>
    <title>{{title + ' - GrndCtrl2MajTom' or 'GrndCtrl2MajTom'}}</title>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300,300italic,400,400italic,600,600italic,700,700italic' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Varela' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="/stylesheets/gcmt.manage.css" type="text/css" />
  </head>
  <body>

	<div id="gcmt-JsRequired">Javascript is required. Please enable Javascript</div>

    <header class="gcmtHeader">
      <h1 class="gcmtHeaderTitle"><a href="/manage">GrndCtrl2MajTom</a></h1>
      <nav class="gcmtHeaderNav">
        <dl class="gcmtHeaderNavList">
          <dt>Main navigation:</dt>
          <dd id="gcmtHeaderNav-blogPosts"><span class="gcmtAccessibleHide">Manage </span>Blog posts</dd>
          <dd id="gcmtHeaderNav-pages"><span class="gcmtAccessibleHide">Manage </span>Pages</dd>
        </dl>
      </nav>
      <div class="gcmtHeaderAccountNav">
        <div class="gcmtHeaderAccountNavOpener">@user.firstName @user.lastName</div>
      </div>
    </header>

    <div class="gcmtMainSidebar">      
      <ul class="gcmtMainSidebarList" id="gcmtMainSidebarList">
      </ul>
    </div>

    <section class="gcmtMainWorkspaceContainer" id="gcmtMainWorkspaceContainer">
%editor()
    </section>
    <script type="text/javascript">
        var dojoConfig = {
            async: true,
            baseUrl: "/javascripts",
            packages: [
                { name: "gcmt", location: "gcmt" },
                { name: "dojo", location: "lib/dojo" },
                { name: "dojox", location: "lib/dojox"},
                { name: "dijit", location: "lib/dijit"}
            ]
        };
    </script>
    <script type="text/javascript" src="/javascripts/lib/dojo/dojo.js"></script>
    <script type="text/javascript">
        require(["gcmt/manage", "dojo/dom", "dojo/domReady!"], function(manage, dom){
            manage.pageInit();
        });
    </script>
  </body>
</html>
