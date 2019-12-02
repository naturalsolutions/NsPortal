
define([
  'marionette', 'backbone', 'moment',
  './base/rootview/lyt-rootview',
  'router',
  'controller',
  'config',
],
function(Marionette, Backbone, Moment, LytRootview, Router,
Controller, config) {

  var app = {};
  var JST = window.JST = window.JST || {};

    // HEADER STENCIL
	function initHeader() {
		var header = document.getElementsByTagName('reneco-header')[0];
		header.options = {
			appTitle: "Portail",
			appIcon: "worldsmall",
			langCode: 'fr',
			user: {
				nickname: 'User name'
			}
		};
	};

  Backbone.Marionette.Renderer.render = function(template, data) {
    if (!JST[template]) throw 'Template \'' + template + '\' not found!';
    return JST[template](data);
  };

  app = new Marionette.Application();

  $.ajaxSetup({ cache: false });

  app.on('start', function() {
    var _this = this;
    var params={};
    window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(str,key,value) {
        params[key] = value;
      }
    );
    var val;
    if(params.img){
      val = params.img;
    }
    if (params.image){
      val = params.image;
    }
    var url = config.coreUrl + 'site';
    if(val=="0" || val=="false" || val == false){
      url = url + '?noimage=true';
    }
    var Patern = Backbone.Model.extend({
      urlRoot: url
    });
    var model = new Patern();
    model.fetch({
      success: function() {
        model.set('siteClassName', model.get('title').replace(/ /g,'-'));
        app.siteInfo = model;
        app.rootView = new LytRootview();
        app.rootView.render();
        initHeader();
        app.controller = new Controller({app: app});
        app.router = new Router({
          controller: app.controller,
          app: app
        });
        app.siteInfos = model;
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
