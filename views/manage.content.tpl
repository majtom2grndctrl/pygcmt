%def editor():
  %include manage.editor
%end
%rebase manage.main editor=editor, title=title
