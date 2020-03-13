import bottle
from tools.mapper import apigamestate_to_simu
from service.snake_controller import *
from api_model.apigamestate import *
from api import ping_response, start_response, move_response, end_response

mode = 'TEST'

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json
    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """

    color = "#9933ff"
    headtype = "pixel"
    tailtype = "pixel"

    return start_response(color, headtype, tailtype)


@bottle.post('/move')
def move():
    data = bottle.request.json
    gamestate = APIGameState(data)
    controller = SnakeController(ControllerMode.ALGO)
    if mode == 'NN':
        pass
    else:
        direction = controller.move(gamestate)
        dir_str = ""
        if direction == Direction.UP:
            dir_str = 'up'
        elif direction == Direction.DOWN:
            dir_str = 'down'
        elif direction == Direction.LEFT:
            dir_str = 'left'
        elif direction == Direction.RIGHT:
            dir_str = 'right'
        else:
            return Direction.NONE
        guiboard = apigamestate_to_simu(gamestate)
        guiboard.render()

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    return move_response(dir_str)


@bottle.post('/end')
def end():
    # """
    # TODO: If your snake AI was stateful,
    #     clean up any stateful objects here.
    # """
    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':

    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True),
        reloader=True
    )
