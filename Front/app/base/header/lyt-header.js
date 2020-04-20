/**

	TODO:
	- header class hide : see router.js & app.js

**/

define(['marionette', 'config','i18n'],
function(Marionette, config) {
  'use strict';
  return Marionette.LayoutView.extend({
    template: 'app/base/header/tpl-header.html',
    className: 'header',
    events: {
      'click #logout': 'logout',
    },

    ui: {
      'user': '#user'
    },

    initialize: function() {
      this.model = window.app.user;
    },

    removeAllTokensWithPrefix(prefix) {
      var keysToRemove = []
      for (var i=0 ; i < localStorage.length; i++) {
        let keyName = localStorage.key(i)
        if (keyName.indexOf(prefix) > -1) {
          keysToRemove.push(keyName)
        }
      }
      for (var i=0; i < keysToRemove.length; i++) {
        localStorage.removeItem(keysToRemove[i]);
      }
    },

    logout: function() {
      var _this = this;
      $.ajax({
        context: this,
        url: config.coreUrl + 'security/oauth2/v1/logout',
      }).done(function() {
        _this.removeAllTokensWithPrefix('NSAPP_')
        Backbone.history.navigate('login', {trigger: true});
      });
    },

    onShow: function() {
      this.$el.i18n();
    },
  });
});
