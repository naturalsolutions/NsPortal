define(['marionette', 'i18n'],
function(Marionette) {
  'use strict';

  return Marionette.LayoutView.extend({
    template: 'app/base/home/tpl/tpl-tile.html',
    className: 'tile small-tile',

    initialize: function(){
      if(this.model.get('TIns_Theme')){
        var tmp = this.model.get('TIns_Theme').split('-');
        switch(tmp[0]){
          case 'track':
            this.model.set({'icon' : 'reneco-trackbird'});
            break;
          case 'securite':
            this.model.set({'icon' : 'reneco-security'});
            break;
          case 'formbuilder':
            this.model.set({'icon' : 'reneco-releve'});
            break;
          case 'thesaurus':
            this.model.set({'icon' : 'reneco-thesaurus'});
            break;
          case 'ecoll':
            this.model.set({'icon' : 'reneco-ecollectionbig'});
            break;
          case 'position':
            this.model.set({'icon' : 'reneco-positions'});
            break;
          default:
            this.model.set({'icon' : 'reneco-releve'});
            break;
        }
      }else{
        this.model.set({'icon' : 'reneco-releve'});
      }
    }
  });



});
