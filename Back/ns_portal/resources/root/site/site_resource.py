from ns_portal.core.resources import (
    MetaRootResource
)
from ns_portal.database.main_db import (
    TSite
)
from marshmallow import (
    Schema,
    EXCLUDE,
    fields
)
from pyramid.security import (
    Allow,
    Everyone
)


class siteSchema(Schema):
    img = fields.Integer(
        default=1,
        missing=1
        )

    class Meta:
        unknown = EXCLUDE


class SiteResource(MetaRootResource):

    __acl__ = [
        (Allow, Everyone, 'read')
        ]

    def GET(self):
        qsParams = self.__parser__(
            args=siteSchema(),
            location='querystring'
        )

        dictConfigIni = getattr(self.request.registry, 'settings')

        query = self.request.dbsession.query(
            TSite.TSit_Name.label('title'),
            TSite.TSit_Country.label('country'),
            TSite.TSit_Locality.label('locality'),
            TSite.TSit_LongName.label('legend'),
            TSite.TSit_UILabel.label('label')
        )
        if qsParams.get('img') == 1:
            query = query.add_columns(
                    TSite.TSit_ImageBackPortal.label('imgBackPortal'),
                    TSite.Tsit_ImageLogoPortal.label('imgLogoPortal'),
                    TSite.TSit_BackgroundHomePage.label('imgBackHomePage')
            )

        query = query.filter(
            TSite.TSit_Name == dictConfigIni.get(
                'RENECO.SECURITE.TSIT_NAME',
                'Web')
                )
        res = query.one_or_none()

        return res._asdict()
