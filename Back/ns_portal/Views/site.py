

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from sqlalchemy import select
from ns_portal.Models import DBSession, User, dbConfig, Base, Site
import base64

@view_config(
    route_name='core/site',
    permission=NO_PERMISSION_REQUIRED,
    renderer='json'
)
def site(request):
    print('portal request')
    print('************ noimage ***********')
    noimage = request.params.get('noimage')
    print(noimage)
    print('************ ')
    if(noimage):
        query = select([
        Site.Name.label('title'),
        Site.Country.label('country'),
        Site.Locality.label('locality'),
        Site.LongName.label('legend'),
        Site.UILabel.label('label')
        ]).where(Site.Name == dbConfig['siteName'])
    else :
       query = select([
        Site.Name.label('title'),
        Site.Country.label('country'),
        Site.Locality.label('locality'),
        Site.LongName.label('legend'),
        Site.ImageBackPortal.label('imgBackPortal'),
        Site.ImageLogoPortal.label('imgLogoPortal'),
        Site.BackgroundHomePage.label('imgBackHomePage'),
        Site.UILabel.label('label')
        ]).where(Site.Name == dbConfig['siteName']) 
    result = DBSession.execute(query).fetchone()
    print('*************************')
    #print(dict(result))
    return dict(result)

@view_config(
    route_name='core/instance',
    renderer='json'
)
def instance(request):
    table = Base.metadata.tables['VAllUsersApplications']
    query = select([
        table
    ]).where((table.c['TSit_Name'] == dbConfig['siteName']) & (table.c['TUse_PK_ID'] == request.authenticated_userid) & (table.c['TRol_Label'] != 'Interdit')).order_by(table.c['TIns_Order'])
    result = DBSession.execute(query).fetchall()
    return [dict(row) for row in result]
