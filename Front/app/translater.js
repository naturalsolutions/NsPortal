define(['marionette','config','i18n'], function(Marionette, config) {

  var Translater = Marionette.Object.extend({

    initialize: function(options) {
      this.url = 'app/locales/__lng__/__ns__.json';
      this.initi18n();
    },
    testInit: function() {
      this.initi18n();
    },

    initi18n: function() {
      if(window && window.app && window.app.user){
        var lng = window.app.user.get('language')
          if (lng != null && lng !=undefined) {
            // console.log('lng', lng)
            i18n.init({
              resGetPath: this.url,
              getAsync: true,
              lng:lng
            });
          }else{
            // console.log('2')
          i18n.init({
            resGetPath: this.url,
            getAsync: true,
            lng: 'en'
          })
          // lng: config.language || 'en' //navigator.language || navigator.userLanguagenavigator.language || navigator.userLanguage
        }
      }else{
        // console.log('3')

        i18n.init({
          resGetPath: this.url,
          getAsync: true,
          lng: 'en'
        })
      }
    },

    // getUserLanguage: function(){
    //   if(window && window.app && window.app.user) {
    //     console.log('mescouilles')
    //     return window.app.user.get('language');
    //   }else{
    //     console.log('defaultlanguage')
    //     return 'en';
    //   }
    //   // if(window && window.app && window.app.user) {
    //   //   var lng = window.app.user.get('language')
    //   //   if (lng != null && lng !=undefined) {
    //   //     i18n.init({
    //   //       resGetPath: this.url,
    //   //       getAsync: true,
    //   //       lng:lng
    //   //     });
    //   //     this.initi18n();
    //   //   }  
    //   // }

    // },

    getValueFromKey: function(key) {
      return $.t(key);
    }
  });

  var translater = new Translater();

  return {
    getTranslater: function(options) { return translater; },
    setTranslater: function(options) {
      // console.log('this in translater', this);
      var url = 'app/locales/__lng__/__ns__.json';
      // console.log('options translater', options)
      i18n.init({
        resGetPath: url,
        getAsync: false,
        lng: options
      });
        
      $(document).i18n();
      return this;
    },
    getUserLng: function(){
      if(window && window.app && window.app.user) {
        return window.app.user.get('language');
      }else{
        return 'en';
      }
    }
  };

});
