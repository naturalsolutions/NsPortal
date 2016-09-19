/**

  TODO:
  - set login as marionette.application

**/
define(['jquery', 'marionette', 'backbone', 'config', './base/login/lyt-login',
  './base/header/lyt-header'],
  function($, Marionette, Backbone, config, LytLogin, LytHeader) {

'use strict';
return Marionette.AppRouter.extend({
  appRoutes: {
    '*route(/:page)': 'home',
  },

  execute: function(callback, args) {
    var _this = this;
    $.ajax({
      context: this,
      cache:false,
      url: config.coreUrl + 'security/has_access' + '?nocache='+Date.now(),
    }).done(function() {

      window.app.user.fetch({
        success: function() {
          $('body').addClass('app');
          _this.insertHeader();
          callback.apply(_this, args);
        }
      });
    }).fail(function(msg) {
      $('body').removeClass('app');
      window.app.rootView.rgHeader.empty();
      window.app.rootView.rgMain.show(new LytLogin());
      Backbone.history.navigate('login', {trigger: true});
    }).always(function(){
    });
  },

  insertHeader: function() {
    if (!window.app.rootView.rgHeader.hasView()) {
      window.app.rootView.rgHeader.show(
        new LytHeader({app: this.options.app}));
    }
  },

});
});
