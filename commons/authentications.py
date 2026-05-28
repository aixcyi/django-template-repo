import logging

from rest_framework.authentication import BaseAuthentication

from apps.core.models import User
from utils.cache import cacher

logger = logging.getLogger('project.auth')


class WeChatAppletAuthentication(BaseAuthentication):
    """
    微信小程序用户认证。
    """

    model = None

    def authenticate(self, request):
        # TODO: 这里使用 Session-ID 头读取认证信息，可根据需要更换。
        if not (auth := request.META.get('HTTP_SESSION_ID', '')):
            return None
        if (user := self.authenticate_credentials(auth)) is None:
            return None
        return user, auth

    def authenticate_credentials(self, sessionid: str) -> User | None:
        if isinstance(user := cacher[f'WeChat:User:{sessionid}'], User):
            return user
        match (users := User.members.filter(wx_session=sessionid)).count():
            case 1:
                return users.first()
            case 0:
                return None
            case c if c > 1:
                logger.warning(f'多个 User 实例拥有相同的微信 Session ID "{sessionid}"')
                return None
            case _:
                logger.error(f'查询集行数异常：User.members.filter(wx_session="{sessionid}").count()')
                return None
