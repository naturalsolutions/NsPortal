
define([
  'marionette', 'backbone', 'moment',
  './base/rootView/lyt-rootview',
  'router',
  'controller',
  'config',
  
],
function(Marionette, Backbone, Moment, LytRootview, Router,
Controller, config) {

  var app = {};
  var JST = window.JST = window.JST || {};

  Backbone.Marionette.Renderer.render = function(template, data) {
    if (!JST[template]) throw 'Template \'' + template + '\' not found!';
    return JST[template](data);
  };

  app = new Marionette.Application();

  $.ajaxSetup({ cache: false });

  app.on('start', function() {
    var _this = this;
    var Patern = Backbone.Model.extend({
      urlRoot: config.coreUrl + 'site'
    });
    var model = new Patern();
    model.fetch({
      success: function() {
        model.set('siteClassName', model.get('title').replace(/ /g,'-'));
        app.siteInfo = model;
        app.rootView = new LytRootview();
        app.rootView.render();
        app.controller = new Controller({app: app});
        app.router = new Router({
          controller: app.controller,
          app: app
        });
        app.user = new Backbone.Model();
        app.user.url = config.coreUrl + 'currentUser';
        Backbone.history.start();
      },
      error: function() {
      },
    });
  });

  $(document).ajaxStart(function(e) {
    $('#header-loader').removeClass('hidden');
  });

  $(document).ajaxStop(function() {
    $('#header-loader').addClass('hidden');
  });

  window.app = app;
  return app;
});
