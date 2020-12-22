# flake8: noqa: S104
import uvicorn

from tttddd.app import create_app

app = create_app()

if __name__ == '__main__':
    import sys
    from funcy import second

    port = int(second(sys.argv) or 8000)

    uvicorn.run(app, host='0.0.0.0', port=port)
