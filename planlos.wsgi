import sys
import os
import site


BASE_DIR = os.path.join(os.path.dirname(__file__))
sys.path.append(BASE_DIR)


from planlos import create_app

app = create_app()


if __name__ == '__main__':
    app.debug = True
    app.run()
