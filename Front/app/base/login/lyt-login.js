/**

	TODO:
	- error msg
	- autocomplete vincent plugin (bb collection)

**/
define(['marionette', 'backbone', 'sha1', 'config', 'jqueryui'],
function(Marionette, Backbone, sha1, config, $ui) {
  'use strict';
  return Marionette.LayoutView.extend({
    template: 'app/base/login/tpl/tpl-login.html',
    collection: new Backbone.Collection(),
    className: 'full-height',

    events: {
      'submit': 'login',
      'change #username': 'checkUsername',
      'focus input': 'clear',
    },

    ui: {
      err: '#help-password',
      pwd: '#pwd-group',
      logo: '#logo',
    },

    initialize: function() {
      this.model = window.app.siteInfo;
      console.log(this.model);
    },

    clear: function(evt) {
      var group = $(evt.target).parent();
      group.removeClass('has-error');
      group.find('.help-block').text('');
    },

    style: function() {
      var imgBackPortal = this.model.get('imgBackPortal');
      var imgLogoPrtal = this.model.get('imgLogoPrtal');
      var logo = 'url(data:image/png;base64,' + imgBackPortal + ')';
      $(this.$el[0]).css('background', logo + ' center center no-repeat');
      var bg = 'url(data:image/png;base64,' + imgLogoPrtal + ')';
      this.ui.logo.css('background', bg + 'center center no-repeat');

      $(this.$el[0]).css({
        'background-position': 'center',
        'background-attachment': 'fixed',
        'background-size': 'cover',
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

          $('#username').autocomplete({
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
    },

    checkUsername: function() {
      var user = this.collection.findWhere({fullname: $('#username').val()});
      if (!user) {
        this.fail('#login-group', 'Invalid username');
      }
    },

    login: function(elt) {
      var _this = this;
      elt.preventDefault();
      elt.stopPropagation();
      var user = this.collection.findWhere({fullname: $('#username').val()});
      var url = config.coreUrl + 'security/login';
      var self = this;

      if (user) {
        $.ajax({
          context: this,
          type: 'POST',
          url: url,
          data: {
            userId: user.get('PK_id'),
            password: sha1.hash($('#password').val()),
          },
        }).done(function() {
          $('.login-form').addClass('rotate3d');
          window.app.user.set('name', $('#username').val());

          setTimeout(function() {
            Backbone.history.navigate('', {trigger: true});
          }, 500);

        }).fail(function() {
          this.fail('#pwd-group', 'Invalid password');
          this.shake();
        });
      } else {
        this.fail('#login-group', 'Invalid username');
        this.shake();
      }
    },

    fail: function(elt, text) {
      $(elt).addClass('has-error');
      $(elt + ' .help-block').text(text);
    },

    shake: function() {
      $('.login-form').addClass('animated shake');
      setTimeout(function() {
        $('.login-form').removeClass('animated shake');
      }, 1000);
    },

  });
});
