from views import *
from utils import get_models


class path:
    """
        Класс для роутинга:
            Поле method - поле определяет метод http запроса к примеру 'GET'.
            Поле url - поле для оперделения ссылки.
            Поле handler - функция обработчик (view)
            Поле private - Булева переменная, если True то для получения
            доступа нужна авторизация.
    """
    def __init__(self, method, url, handler, private):
        self.method = method
        self.url = url
        self.handler = handler
        self.private = private


urlpatterns = [
    path('POST', '/token-auth', auth_token, False),
    path('GET', '/current-user', current_user, True),
    path('POST', '/token-refresh', refresh_token, True),
    path('GET', '/token-verify', verify_token, True),
    path('POST', '/user', add_user, True),
]


async def auth_middleware(app, handler):
    async def middleware(request):
        for path in urlpatterns:
            if path.private is False:
                if str(request.url).find(path.url) != -1:
                    return await handler(request)
        else:
            request.user = None
            try:
                jwt_token = request.headers['authorization']
                if jwt_token:
                    try:
                        payload = jwt.decode(jwt_token, JWT_SECRET,
                                             algorithms=[JWT_ALGORITHM])
                    except (jwt.DecodeError, jwt.ExpiredSignatureError):
                        return json_response({'message': 'Token is invalid'},
                                             status=400)

                    request.user = get_models(User).filter(
                        User.id == payload['user_id']
                    ).first()
                return await handler(request)
            except Exception as e:
                response_obj = {'status': 'failed', 'reason': str(e)}
                return json_response(response_obj, status=500)
    return middleware
