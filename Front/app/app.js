
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

  Backbone.Marionette.Renderer.render = function(template, data) {
    if (!JST[template]) throw 'Template \'' + template + '\' not found!';
    return JST[template](data);
  };

  app = new Marionette.Application();

  $.ajaxSetup({
  });

  function authAndRedirect(params) {
    $.ajax({
      context: this,
      type: 'POST',
      url: config.coreUrl +'security/oauth2/v1/authorize',
      data: JSON.stringify(params),
      dataType: 'json',
      contentType: 'application/json',
      success: function(data) {
        search = '?code=' + data.code
        window.location = document.referrer + search
      },
      error: function(data) {

      }
    })
  }

  function queryStringExistAndValid() {
      var toRet = {
        "client_id" : null,
        "redirect_uri": null,
        "img": 1
      }
      var qs = window.location.search.substring(1)
      if ( qs == '') {
        toRet = {
          "img": 1
        }
      }
      else {
        var pairs = qs.split('&')
        for (var i = 0; i < pairs.length; i++) {
          var tmp = pairs[i].split('=');
          var key = tmp[0];
          var value = tmp[1]

          for (var keyTofind in toRet) {
            if (keyTofind == decodeURIComponent(key)) {
              toRet[keyTofind] = decodeURIComponent(value)
            }
          }
        }
      }
      return toRet

  }

  function removeAllTokensWithPrefix(prefix) {
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
  }

  function checkIfCookie(model, params, app) {
    $.ajax({
      context: this,
      type: 'GET',
      url: config.coreUrl +'instance',
      dataType: 'json',
      contentType: 'application/json',
      success : function(data) {
        //cookie is valid
        var qsParams = queryStringExistAndValid()
        if (qsParams.client_id != null && qsParams.redirect_uri != null) {
          //shortcut flow app will be redirected
          authAndRedirect(qsParams)
        }
      },
      error : function(data) {
        removeAllTokensWithPrefix('NSAPP_')
        //cookie not valid
      },
      complete: function(data) {
        //will not be executed if we have cookie and qs for redirect
        model.fetch(params);
      }
    })
  }


  app.on('start', function() {

    // oauth2.cookieIsValid()
    // var params = oauth2.queryStringExistAndValid()
    // oauth2.authAndRedirect(params=params)

    var qsParams = queryStringExistAndValid()
    var qsParamsNoImg = ""
    if (qsParams.img == 0) {
      qsParamsNoImg = '?img=0'
    }

    var Patern = Backbone.Model.extend({
      urlRoot: config.coreUrl + 'site'+ qsParamsNoImg
    });
    var model = new Patern();
    var params = {
      success: function() {
        model.set('siteClassName', model.get('title').replace(/ /g,'-'));
        model.set('errorAPI500', false);
      },
      error: function() {
        var defaultConfig ={
          title: "NS-Marseille",
          country: "France",
          locality: "Marseille",
          legend: "Natural Solutions",
          label: "NS",
          siteClassName: "NS-Marseille",
          errorAPI500 : true
        }
        model.set(defaultConfig);
      },
      complete: function() {
        app.siteInfo = model;
        app.rootView = new LytRootview();
        app.rootView.render();
        app.controller = new Controller({app: app});
        app.router = new Router({
          controller: app.controller,
          app: app
        });
        app.siteInfos = model;
        app.user = new Backbone.Model();
        app.user.url = config.coreUrl + 'me';
        Backbone.history.start();
      }
    }

    checkIfCookie(model, params, app)
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
