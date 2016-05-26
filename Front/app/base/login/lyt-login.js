/**

	TODO:
	- error msg
	- autocomplete vincent plugin (bb collection)

**/
define(['marionette', 'backbone', 'sha1', 'config', 'jqueryui','i18n'],
function(Marionette, Backbone, JsSHA, config, $ui) {
  'use strict';
  return Marionette.LayoutView.extend({
    template: 'app/base/login/tpl/tpl-login.html',
    collection: new Backbone.Collection(),
    className: 'full-height',

    events: {
      'submit': 'login',
      'change #UNportal': 'isValidUserName',
      'focus input': 'clear',
    },

    ui: {
      err: '#help-password',
      logo: '#logo',

      userName: '#UNportal',
      password: '#password',
    },

    pwd: function(pwd) {

      pwd = window.btoa(unescape(decodeURIComponent( pwd )));
      var hashObj = new JsSHA('SHA-1', 'B64', 1);

      hashObj.update(pwd);
      pwd = hashObj.getHash('HEX');
      return pwd;
    },

    initialize: function() {
      this.model = window.app.siteInfo;

      var tmp = this.model.get('label').split('^');
      if (tmp.length > 1) {
        this.model.set({'sup' : tmp[1]});
      }else {
        this.model.set({'sup' : ''});
      }
      this.model.set({'title' : tmp[0]});
    },

    style: function() {
      var _this = this;
      
      if(window.doNotloadBg){
        $(this.$el[0]).css('background', 'grey');
      } else {
        var imgBackPortal = this.model.get('imgBackPortal');
        var bg = 'url(data:image/png;base64,' + imgBackPortal + ')';
        $(this.$el[0]).css('background', bg + ' center center no-repeat');
        $(this.$el[0]).css({
          'background-position': 'center',
          'background-attachment': 'fixed',
          'background-size': 'cover',
        });
      }
      var imgLogoPrtal = this.model.get('imgLogoPortal');
      var logo = 'url(data:image/png;base64,' + imgLogoPrtal + ')';
      this.ui.logo.css('background', logo + 'center center no-repeat');
      this.ui.logo.css({
        'background-size': 'contain',
      });
    },

    onShow: function() {
      this.style();
      var ctx = this;
      this.collection.url = config.coreUrl + 'user';
      this.collection.fetch({
        success: function(data) {
          ctx.users = [];
          data.each(function(m) {
            ctx.users.push(m.get('fullname'));
          });

          $('#UNportal').autocomplete({
            source: function(request, response) {
              var exp = '^' + $.ui.autocomplete.escapeRegex(request.term);
              var matcher = new RegExp(exp, 'i');
              response($.grep(ctx.users, function(item) {
                return matcher.test(item);
              }));
            },
          });
        },
      });
       this.$el.i18n();
    },

    isValidUserName: function() {
      var user = this.collection.findWhere({fullname: this.ui.userName.val()});
      if (!user) {
        this.displayError(true, this.ui.userName, 'Invalid username');
        return false;
      } else {
        return user;
      }
    },

    login: function(elt) {
      var _this = this;
      elt.preventDefault();
      elt.stopPropagation();
      var url = config.coreUrl + 'security/login';
      var user = this.isValidUserName();
      
      if (!$('#password').val().length) {
        this.displayPwdError(true, this.ui.password, 'Invalid password');
        this.shake();
      }

      if (user) {
        $.ajax({
          context: this,
          type: 'POST',
          url: url,
          data: {
            userId: user.get('PK_id'),
            password: this.pwd($('#password').val()),
          },
        }).done(function() {
          $('.login-form').addClass('rotate3d');
          window.app.user.set('name', $('#UNportal').val());
          setTimeout(function() {
            Backbone.history.navigate('', {trigger: true});
          }, 500);
        }).fail(function() {
          this.displayPwdError(true, this.ui.password, 'Invalid password');
          this.shake();
		  $('#password').val('');
        });
      } else {
        this.shake();
      }
    },

    clear: function(evt) {
      $(evt.target).removeClass('help-error');
      $(evt.target).val('');

      this.ui.password.attr('placeholder', 'Password');
      this.ui.password.val('');
      this.ui.password.removeClass('help-error');
    },

    displayError: function(error, elt, placeholder){
      if(error){
        elt.addClass('help-error');
        elt.val(placeholder);
      } else {
        elt.removeClass('help-error');
      }
    },

    displayPwdError: function(error, elt, placeholder){
      if(error){
        elt.addClass('help-error');
        elt.val('');
        elt.attr('placeholder', 'Invalid password');
      }
    },

    shake: function() {
      $('.login-form').addClass('animated shake');
      setTimeout(function() {
        $('.login-form').removeClass('animated shake');
      }, 1000);
    },

  });
});
