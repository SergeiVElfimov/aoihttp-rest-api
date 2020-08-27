from models import session, User, GroupUsers
from datetime import datetime, timedelta
import jwt
from utils import *

JWT_SECRET = 'j3vs0$6()biq#czpc89f6a_3s8*yvi9&)7o(@pza@&b=5mx4p#'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = timedelta(days=2)


async def current_user(request):
    return json_response(request.user.to_dict(), status=200)


async def verify_token(request):
    return json_response({'message': 'Token is valid'}, status=200)


async def refresh_token(request):
    user = request.user
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + JWT_EXP_DELTA_SECONDS
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return json_response({'token': jwt_token.decode('utf-8')}, status=200)


async def add_user(request):
    try:
        data = await request.json()
        u = User(data['username'],
                 data['firstname'],
                 data['lastname'],
                 int(data['groupusers_id']))
        u.set_password(data['password'])
        session.add(u)
        session.commit()
        response_obj = {'status': 'success'}
        return json_response(response_obj, status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        session.rollback()
        return json_response(response_obj, status=500)


async def auth_token(request):
    post_data = await request.json()
    try:
        user = get_models(User).filter(
            User.username == post_data['username']
        ).first()
        if (user is None):
            return json_response({'message': 'Неверный логин'}, status=400)
        if (user.check_password(post_data['password']) is False):
            return json_response({'message': 'Неверный пароль'}, status=400)
    except Exception as e:
        return json_response({'error': str(e)}, status=500)

    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + JWT_EXP_DELTA_SECONDS
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return json_response({'token': jwt_token.decode('utf-8')}, status=200)
