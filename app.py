"""Pequena API HTTP usada na pratica de automacao de build."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class AppHandler(BaseHTTPRequestHandler):
    """Atende as rotas da aplicacao sem dependencias externas."""

    server_version = "BuildAutomationApp/1.0"

    def do_GET(self) -> None:  # noqa: N802 - nome exigido por BaseHTTPRequestHandler
        routes = {
            "/": (
                HTTPStatus.OK,
                {
                    "aplicacao": "Automacao de Build",
                    "mensagem": "Aplicacao executando com sucesso",
                    "versao": os.getenv("APP_VERSION", "local"),
                },
            ),
            "/health": (HTTPStatus.OK, {"status": "ok"}),
        }

        status, body = routes.get(
            self.path,
            (HTTPStatus.NOT_FOUND, {"erro": "rota nao encontrada"}),
        )
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        """Mantem o log HTTP simples e compativel com containers."""
        print(f"{self.address_string()} - {format % args}")


def create_server(host: str = "0.0.0.0", port: int = 8000) -> ThreadingHTTPServer:
    """Cria o servidor para execucao normal e para os testes automatizados."""
    return ThreadingHTTPServer((host, port), AppHandler)


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = create_server(port=port)
    print(f"Servidor iniciado em http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
