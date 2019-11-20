from sanic import Sanic
from sanic.response import json, text
from src.bind import session_scope
from src.model import Time, Player, InvalidParameter
from src.constants import nyt_tz
import datetime as dt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sanic.exceptions import InvalidUsage, SanicException, add_status_code
from sanic_openapi import swagger_blueprint, doc


@add_status_code(422)
class ResourceExists(SanicException):
    pass


application = Sanic(__name__)
application.blueprint(swagger_blueprint)


@application.route('/time', methods=['POST'])
@doc.summary("Post your time for the day")
@doc.consumes({"time": {
    "name": str,
    "game": str,
    "time": float
}}, location="body", content_type='application/json', required=True)
async def time(request):
    try:
        with session_scope() as sesh:
            try:
                player = sesh.query(Player).filter(Player.name == request.json['player']).one()
            except KeyError as e:
                raise InvalidUsage('player parameter must be passed in request')
            except NoResultFound as e:
                raise InvalidUsage(f'{request.json["player"]} is not a registered player')
            try:
                time = Time(
                    player_id=player.id,
                    time=float(request.json['time']),
                    game=request.json['game']
                )
            except InvalidParameter as e:
                raise InvalidUsage(e)
            sesh.add(time)
    except IntegrityError as e:
        raise ResourceExists('time already posted')
    return text('time posted')


@application.route('/player', methods=['POST'])
@doc.summary("Register player")
@doc.consumes({"player": {
    "name": str
}}, location="body", content_type='application/json', required=True)
async def player(request):
    try:
        with session_scope() as sesh:
            name = request.json['name']
            player = Player(name=name)
            sesh.add(player)
    except IntegrityError as e:
        raise ResourceExists(f'player {name} already registered')
    return text(f'player {name} now registered')


@application.route('/players', methods=['GET'])
@doc.summary("List of registered players")
@doc.produces([str], content_type='application/json')
async def players(request):
    with session_scope() as sesh:
        players = sesh.query(Player.name).all()
        return json([p[0] for p in players])


@application.route('/winner', methods=['GET'])
@doc.summary("Who won today?")
@doc.produces([str], content_type='application/json')
async def winner(request):
    with session_scope() as sesh:
        with open('src/query/winner.sql', 'r') as f:
            winners = list(sesh.execute(
                f.read(),
                {'date': dt.datetime.now(tz=nyt_tz).date(), 'game': request.args['game'][0]}
            ))
    winners = [dict(zip(('player', 'game', 'date', 'time'), w)) for w in winners]
    for w in winners:
        w['date'] = w['date'].strftime('%Y-%m-%d')
    return json(winners)


@application.route('/healthz', methods=['GET'])
@doc.summary("Check if service is up")
@doc.produces({
    "healthy": bool
}, content_type='application/json')
async def healthz(request):
    """Check if service is up.
    """
    with session_scope() as sesh:
        sesh.execute('SELECT 1')
    return json({'healthy': True})


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80)
