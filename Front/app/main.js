require.config({
  baseUrl: 'app',
  paths: {

    tmp: './tmp',

    app: 'app',
    config: 'config',
    router: 'router',
    controller: 'controller',
    models: './models',
    collections: './collections',
    templates: '../build/templates',
    lytRootview: './base/rootview/lyt-rootview',
    transitionRegion: './base/transition-region/transition-region',
    translater: 'translater',

    /*==========  Bower  ==========*/
    jquery: '../bower_components/jquery/dist/jquery.min',
    jqueryui: '../bower_components/jqueryui/jquery-ui.min',
    underscore: '../bower_components/lodash/lodash',
    backbone: '../bower_components/backbone/backbone',
    marionette: '../bower_components/marionette/lib/core/backbone.marionette',
    'backbone.babysitter': '../bower_components/backbone.babysitter/' +
    'lib/backbone.babysitter',
    'backbone.wreqr': '../bower_components/backbone.wreqr/lib/backbone.wreqr',
    radio: '../bower_components/backbone.radio/build/backbone.radio',
    bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
    sha1: '../bower_components/jsSHA/src/sha1',
    moment: '../bower_components/moment/min/moment.min',
    momentLocale: '../bower_components/moment/locale',
    i18n: '../bower_components/i18n/i18next',
    utf8: '../bower_components/utf8/utf8',

  },

  shim: {
    jquery: {
      exports: '$',
    },
    jqueryui: {
      exports: 'ui',
    },
    underscore: {
      exports: '_',
    },
    backbone: {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone',
    },
    marionette: {
      exports: 'Marionette',
    },
    radio: {
      exports: 'Radio',
    },
    bootstrap: {
      deps: ['jquery'],
      exports: 'Bootstrap',
    },
    templates: {
      deps: ['underscore'],
      exports: 'Templates',
    },
    sha1: {
      exports: 'sha1',
    },
    moment: {
      exports: 'moment',
    },
    i18n: {
      deps: ['jquery'],
      exports: '$',
    },
  },
});

require(['app', 'templates','translater'],
function(app, templates, Translater) {
  app.start();
  this.translater = Translater.getTranslater();
});
