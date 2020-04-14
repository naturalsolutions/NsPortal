from ns_portal.core.resources import (
    MetaEndPointResource
)
from marshmallow import (
    Schema,
    fields,
    EXCLUDE,
    ValidationError
)
from ns_portal.database.main_db import (
    TUsers
)
from sqlalchemy import (
    and_,
    select
)
from sqlalchemy.orm.exc import (
    MultipleResultsFound
)
from ns_portal.database import (
    Main_Db_Base
)
from pyramid.security import (
    Allow,
    Everyone,
    remember
)
from ns_portal.utils import (
    getCookieToken
)
from pyramid.response import (
    Response
)


class loginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class LoginResource(MetaEndPointResource):

    __acl__ = [
        (Allow, Everyone, 'create')
    ]

    def validateUserCredentials(self, data):
        query = self.request.dbsession.query(TUsers)
        query = query.filter(
            and_(
                TUsers.TUse_Login == data.get('username'),
                TUsers.TUse_Password == data.get('password')
                )
            )
        try:
            res = query.one_or_none()
        except MultipleResultsFound:
            raise ValidationError({
                "error": (
                    'your username and password are'
                    ' not unique in db'
                    ' please report it to an admin'
                    )
                })
        if res:
            # this key is added after validation
            return res
        else:
            raise ValidationError({
                "error": (
                    'your username and/or password'
                    ' are wrongs'
                    )
                })



    def POST(self):
        reqParams = self.__parser__(
            args=loginSchema(),
            location='form'
        )

        userFound = self.validateUserCredentials(data=reqParams)
        if userFound:
            # CRITICAL START
            # this method will return the object that handle
            # policy in pyramid app
            # the policy object store keys from conf for generate token
            # policy = _get_authentication_policy(self.request)
            # CRITICAL END

            # payload = self.buildPayload(params=userFound, policy=policy)
            token = getCookieToken(
                idUser=getattr(userFound, 'TUse_PK_ID'),
                request=self.request
            )
            # toRet = Response(
            #     status=200,
            #     json_body={
            #         "token": token.decode('utf-8')
            #         }
            # )
            # remember(toRet, token)
            # return toRet

            resp = Response(
                status=200
                )
            remember(
                resp,
                token
                )
            self.request.response = resp
            return self.request.response
        else:
            raise ValidationError({
                "error": (
                    'your username and/or password'
                    ' are wrongs'
                    )
                })
