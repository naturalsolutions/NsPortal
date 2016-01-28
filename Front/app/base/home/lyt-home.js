define([
  'underscore', 'marionette', 'jquery', 'config',
  'moment', './lyt-tile', 'i18n'
],
function(_, Marionette, $, config, Moment, LytTile) {
  'use strict';

  return Marionette.LayoutView.extend({
    template: 'app/base/home/tpl/tpl-home.html',
    className: 'home-page ns-full-height',
    events: {
      'click #nextPage': 'nextPage',
      'click #prevPage': 'prevPage',
    },

    ui: {
      'tileContainer': '#tileContainer',
      'user': '#user'
    },

    initialize: function() {
      this.model = window.app.user;
            var locale = config.language;
      if(locale == 'fr'){
        require(['momentLocale/fr']);
      }
    },

    animateIn: function() {
      this.$el.find('#tiles').removeClass('zoomOutDown');
      this.$el.find('#tiles').addClass('zoomInDown');
      this.$el.find('#tiles').animate(
      {opacity: 1},
      500,
      _.bind(this.trigger, this, 'animateIn')
      );
    },

    // Same as above, except this time we trigger 'animateOut'
    animateOut: function() {
      this.$el.find('#tiles').removeClass('zoomInUp');
      this.$el.animate(
        {opacity: 0},
        500,
        _.bind(this.trigger, this, 'animateOut')
      );
    },

    style: function() {
      var imgBackHomePage = window.app.siteInfo.get('imgBackHomePage');
      $(this.$el[0]).css('background',
        'url(data:image/png;base64,' + imgBackHomePage + ') ');

      $(this.$el[0]).css({
        'background-position': 'center',
        'background-attachment': 'fixed',
        'background-size': 'cover',
      });

    },

    onShow: function(options) {
      this.style();
      this.startTime();
      this.displayTiles();
      this.$el.i18n();

    },

    ripple: function() {
      var ink;
      var d;
      var x;
      var y;
      $('.ripplelink').click(function(e) {
        if ($(this).find('.ink').length === 0) {
          $(this).prepend('<span class="ink"></span>');
        }

        ink = $(this).find('.ink');
        ink.removeClass('animate');

        if (!ink.height() && !ink.width()) {
          d = Math.max($(this).outerWidth(), $(this).outerHeight());
          ink.css({height: d, width: d});
        }

        x = e.pageX - $(this).offset().left - ink.width() / 2;
        y = e.pageY - $(this).offset().top - ink.height() / 2;

        ink.css({top: y + 'px', left: x + 'px'}).addClass('animate');
      });
    },

    startTime: function() {
      
      var locale = config.language;
      var dateNow ;
      if(locale == 'fr'){
        //require(['momentLocale/fr']);
        dateNow = new Moment().locale('fr').format('LLLL');
      } else {
        dateNow = new Moment().format('MMMM Do YYYY, h:mm:ss a').replace(/([rdths]{2})\s2015/,"<sup>\$1</sup> 2015");
      }
      var _this = this;
      this.$el.find('time').html(dateNow);
      var t = setTimeout(function() {
        _this.startTime();
      }, 1000);
    },

    displayTiles: function() {
      var _this = this;
      var TileColl = Backbone.Collection.extend({
        url: config.coreUrl + '/tiles',
      });

      this.tileColl = new TileColl();

      this.tileColl.url = config.coreUrl + 'instance';

      var TileCollView = Backbone.Marionette.CollectionView.extend({
        className: 'tiles-wrapper',
        childView: LytTile,

        _renderChildren: function() {
          this.destroyEmptyView();
          this.destroyChildren();
          if (this.isEmpty(this.collection)) {
            this.showEmptyView();
          } else {
            this.triggerMethod('before:render:collection', this);
            this.startBuffering();
            this.showCollection();
            this.endBuffering();
            this.triggerMethod('render:collection', this);
            if (!this.children.length) {
              this.filter = null;
              this.render();
            }

            // If we have shown children and none have passed the filter, show the empty view
            if (this.children.isEmpty()) {
              this.showEmptyView();
            }
          }
        },

        attachBuffer: function(collectionView) {
          if (collectionView.children.length != 0) {
            var html = $(this._createBuffer(collectionView));
            var page = '';
            var perPageTab = _.chunk(html.children(), 10);
            collectionView.$el.empty();
            for (var i = 0; i < html.children().length; i++) {
              if (i % 10 == 0) {
                page = '<div class="page clearfix hidden"></div>';
                collectionView.$el.append(page);
              }
            };

            collectionView.$el.find('.page').each(function(index) {
              $(this).append(perPageTab[index]);
              if (index === 0) {
                $(this).removeClass('hidden');
              }
            });

            if (collectionView.$el.find('.page').length > 1) {
              _this.$el.find('#nextPage').removeClass('hidden');
            }else {
              _this.$el.find('#nextPage').addClass('hidden');
            }
            _this.$el.find('#prevPage').addClass('hidden');
          }
        },
      });
      this.tileCollView = new TileCollView({
        collection: this.tileColl
      });

      //keyboard events
      var timer;
      $(document).keydown(function(e) {
        var char = String.fromCharCode(e.keyCode || e.charCode);
        var code = e.keyCode;
        if ((code >= 65 && code <= 90) || (code >= 97 && code <= 122)) {
          _this.tileCollView.filter = function(child, index, collection) {
            var tmp = child.get('TIns_Label').toUpperCase();
            return tmp.lastIndexOf(char, 0) === 0;
          },
          _this.tileCollView.render();
          clearTimeout(timer);
          timer = setTimeout(function() {
            _this.tileCollView.filter = null;
            _this.tileCollView.render();
          }, 2000);
        }
        return;
      });
      this.tileColl.fetch({
        success: function() {
          _this.tileCollView.render();
          _this.ui.tileContainer.html(_this.tileCollView.el);
        }
      });
    },

    //a bit dirty
    nextPage: function() {
      var current = this.$el.find('.tiles-wrapper').find('.page:not(.hidden)');
      var index = parseInt(current.index());
      var nbPage = this.$el.find('.tiles-wrapper').find('.page').length;
      if (nbPage !== (index + 1)) {
        current.addClass('hidden');
        current.next().removeClass('hidden');
        if ((current.next().index() + 1) == nbPage) {
          this.$el.find('#nextPage').addClass('hidden');
        }
        this.$el.find('#prevPage').removeClass('hidden');
      }
    },

    prevPage: function() {
      var current = this.$el.find('.tiles-wrapper').find('.page:not(.hidden)');
      var nbPage = this.$el.find('.tiles-wrapper').find('.page').length;
      var index = current.index();
      if (index >= 1) {
        current.addClass('hidden');
        current.prev().removeClass('hidden');
        this.$el.find('#nextPage').removeClass('hidden');
        if (current.prev().index() == 0) {
          this.$el.find('#prevPage').addClass('hidden');
        }
      }
    },

  });
});
