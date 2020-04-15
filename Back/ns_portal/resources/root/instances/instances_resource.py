from ns_portal.core.resources import (
    MetaEndPointResource
)
from ns_portal.database.main_db import (
    TInstance,
    TApplications,
    TAutorisations,
    TUsers,
    TRoles,
    TSite
)
from ns_portal.utils.utils import (
    my_get_authentication_policy
)
from pyramid.security import (
    Allow,
    Authenticated
)


class InstancesResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Authenticated, 'read')
        ]

    def GET(self):
        policy = my_get_authentication_policy(self.request)
        tsiteName = getattr(policy, 'TSit_Name')
        userId = self.request.authenticated_userid.get('TUse_PK_ID')

        colsToRet = [
            TInstance.TIns_PK_ID,
            TInstance.TIns_Label,
            TInstance.TIns_ApplicationPath,
            TInstance.TIns_Theme,
            TInstance.TIns_Database,
            TInstance.TIns_Order,
            TInstance.TIns_ReadOnly,
            TApplications.TApp_ClientID,
            TApplications.TApp_Description,
            TRoles.TRol_Label,
            TUsers.TUse_PK_ID,
            TSite.TSit_Name,
            TSite.TSit_Project,
            TSite.TSit_ImagePathMainLogo,
            TSite.TSit_ImagePathMainMenu,
            TAutorisations.TUse_Observer
        ]

        VAllUsersApplications = self.request.dbsession.query(TInstance)
        VAllUsersApplications = VAllUsersApplications.join(TApplications)
        VAllUsersApplications = VAllUsersApplications.join(
            TAutorisations,
            TInstance.TIns_PK_ID == TAutorisations.TAut_FK_TInsID
            )
        VAllUsersApplications = VAllUsersApplications.join(TRoles)
        VAllUsersApplications = VAllUsersApplications.join(TUsers)
        VAllUsersApplications = VAllUsersApplications.join(
            TSite,
            TInstance.TIns_FK_TSitID == TSite.TSit_PK_ID
            )

        VAllUsersApplications = VAllUsersApplications.with_entities(*colsToRet)

        VAllUsersApplications = VAllUsersApplications.filter(
                (TSite.TSit_Name == tsiteName),
                (TUsers.TUse_PK_ID == userId),
                (TRoles.TRol_Label != 'Interdit')
            )
        VAllUsersApplications = VAllUsersApplications.order_by(
            TInstance.TIns_Order
            )

        result = VAllUsersApplications.all()

        return [row._asdict() for row in result]
