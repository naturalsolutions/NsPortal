define(['marionette', 'moment', 'i18n'],
function(Marionette, moment) {
	'use strict';

	return Marionette.LayoutView.extend({
		template: 'app/base/home/tpl/tpl-home.html',
		className: 'home-page ns-full-height',
		events: {
		},


		initialize: function(){
			this.model = window.app.user;
		},

		animateIn: function() {
			this.$el.find('#tiles').removeClass('zoomOutDown');

			this.$el.find('#tiles').addClass('zoomInDown');

			this.$el.find('#tiles').animate(
				{ opacity: 1 },
				500,
				_.bind(this.trigger, this, 'animateIn')
			);
		},

		// Same as above, except this time we trigger 'animateOut'
		animateOut: function() {
			this.$el.find('#tiles').removeClass('zoomInUp');
			this.$el.animate(
				{ opacity : 0 },
				500,
				_.bind(this.trigger, this, 'animateOut')
			);
		},

		style: function(){
			var imgBackHomePage = window.app.siteInfo.get('imgBackHomePage');
			$(this.$el[0]).css('background', 'url(data:image/png;base64,'+ imgBackHomePage +') ');

			$(this.$el[0]).css({
				'background-position': 'center',
				'background-attachment': 'fixed',
				'background-size': 'cover',
			});

		},

		onShow : function(options) {

			this.style();

			this.$el.find('#tiles').i18n();

			var popup = this.$el.find('#trackPopup');
			this.$el.find('#track').on('click', function(){
				popup.fadeIn('fast');
			})
			popup.find('#close').on('click', function(){
				popup.fadeOut('fast');
			});
			$(document).mouseup(function (e)
			{
				if (!popup.is(e.target) // if the target of the click isn't the container...
					&& popup.has(e.target).length === 0) // ... nor a descendant of the container
				{
					popup.fadeOut('fast');
				}
			});


			var ink, d, x, y;
			$('.ripplelink').click(function(e){
				if($(this).find('.ink').length === 0){
					$(this).prepend('<span class="ink"></span>');
				}
				ink = $(this).find('.ink');
				ink.removeClass('animate');

				if(!ink.height() && !ink.width()){
					d = Math.max($(this).outerWidth(), $(this).outerHeight());
					ink.css({height: d, width: d});
				}

				x = e.pageX - $(this).offset().left - ink.width()/2;
				y = e.pageY - $(this).offset().top - ink.height()/2;
				
				ink.css({top: y+'px', left: x+'px'}).addClass('animate');
			});
			this.startTime();
		},

		startTime: function() {
			var _this = this;
			this.$el.find('time').html(new moment().format('MMMM Do YYYY, h:mm:ss a'));
			var t = setTimeout(function () {
				_this.startTime();
			}, 1000);
		}
		
	});
});
