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
            this.model.set({'icon' : 'reneco-TRACK-trackbird'});
            break;
          case 'securite':
            this.model.set({'icon' : 'reneco-security'});
            break;
          case 'formbuilder':
            this.model.set({'icon' : 'reneco-FOR-formbuilder'});
            break;
          case 'thesaurus':
            this.model.set({'icon' : 'reneco-THE-thesaurus'});
            break;
          case 'ecoll':
            this.model.set({'icon' : 'reneco-ECO-ecollectionbig'});
            break;
          case 'position':
            this.model.set({'icon' : 'reneco-POS-positions'});
            break;
          case 'repro':
            this.model.set({'icon' : 'reneco-tuile'});
            break;
          case 'centralization':
            this.model.set({'icon' : 'reneco-tuile1'});
            break;
          case 'reneco-apps':
            this.model.set({'icon' : 'reneco-tuile2'});
            break;
          case 'CentralMonitoring':
            this.model.set({'icon' : 'reneco-data-centralisation'});
            break;
          default:
            this.model.set({'icon' : 'reneco-ECO-releve'});
            break;
        }
      }else{
        this.model.set({'icon' : 'reneco-ECO-releve'});
      }
      // set hostname
      var hostname  = window.location.hostname ;
      var appliPath = this.model.get('TIns_ApplicationPath');
      var newPath = appliPath.replace("@@hostname@@", hostname);
      this.model.set('TIns_ApplicationPath', newPath);
    }
  });



});
