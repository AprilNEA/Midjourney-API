import os
import uvicorn
from config import Config

if __name__ == "__main__":
    # Determine the current running environment,
    # and in a PaaS environment,
    # read the environment variables set in the platform directly
    if Config.environment == "production":
        uvicorn.run(
            "app.app:app",
            port=8080,
            host="0.0.0.0",
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
    else:
        # When debugging locally
        # Recommended to start reloading in the terminal
        # poetry run uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload
        uvicorn.run(
            "app.app:app",
            port=8080,
            host="127.0.0.1",
            reload_dirs="./app",
            reload=True,
            proxy_headers=True,
            forwarded_allow_ips="*",  # allow WSGI to forward ip address
        )
