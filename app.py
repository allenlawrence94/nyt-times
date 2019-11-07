from sanic import Sanic
from sanic.response import json
from src.bind import session_scope
from src.model import Model


class BaseAppException(Exception):
    """Identify exceptions raised in app for app handler

    Adapted from <http://flask.pocoo.org/docs/1.0/patterns/apierrors/>
    """
    default_status_code = 500

    def __init__(self, message, status_code=None, payload=()):
        super(BaseAppException, self).__init__()
        self.message = message
        self.status_code = status_code or self.default_status_code
        self.payload = payload

    def to_dict(self):
        d = dict(self.payload)
        d['message'] = self.message
        return d


application = Sanic(__name__)


@application.exception(BaseAppException)
def handle_app_exception(error):
    resp = json(error.to_dict())
    resp.status_code = error.status_code
    return resp


@application.route('/model', methods=['GET'])
async def model(request):
    with session_scope() as sesh:
        m_model = sesh.query(Model).get(request.args['id'])
    return json({
        'id': m_model.id,
        'time_created': m_model.time_created,
        'foo': m_model.foo,
        'bar': m_model.bar
    })


@application.route('/healthz', methods=['GET'])
async def healthz(request):
    """Check if service is up.
    """
    with session_scope() as sesh:
        sesh.execute('SELECT 1')
    return json({'healthy': True})


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000)
