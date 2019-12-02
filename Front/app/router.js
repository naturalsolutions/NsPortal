/**

  TODO:
  - set login as marionette.application

**/
define(['jquery', 'marionette', 'backbone', 'config', './base/login/lyt-login',
  './base/header/lyt-header','i18n', 'translater'], 
  function($, Marionette, Backbone, config, LytLogin, LytHeader,i18n, translater) {

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
         // _this.insertHeader();
          // debugger;
          var lng = translater.getUserLng()
          // console.log('lng', lng)
          translater.setTranslater(lng, function(t) {
            _this.$el.i18n();
          });
          callback.apply(_this, args);
        }
      });
    }).fail(function(msg) {
      $('body').removeClass('app');
      //window.app.rootView.rgHeader.empty();
      window.app.rootView.rgMain.show(new LytLogin());
      Backbone.history.navigate('login', {trigger: true});
    }).always(function(){
      $("body").css('background-image', 'none');
    });
  },

  /* insertHeader: function() {
    if (!window.app.rootView.rgHeader.hasView()) {
      window.app.rootView.rgHeader.show(
        new LytHeader({app: this.options.app}));
    }
  }, */

});
});
