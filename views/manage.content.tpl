%def editor():
  %include manage.blogposts.new
%end
%rebase manage.main editor=editor, title=title
