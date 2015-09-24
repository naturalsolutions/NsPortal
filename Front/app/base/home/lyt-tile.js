define(['marionette', 'i18n'],
function(Marionette) {
  'use strict';

  return Marionette.LayoutView.extend({
    template: 'app/base/home/tpl/tpl-tile.html',
    className: 'tile small-tile',
  });
});
