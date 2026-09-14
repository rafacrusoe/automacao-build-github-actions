"""Testes funcionais da API HTTP."""

from __future__ import annotations

import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from app import create_server


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def read_json(self, path: str) -> tuple[int, dict[str, str]]:
        try:
            with urlopen(f"{self.base_url}{path}", timeout=2) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def test_home_returns_application_data(self) -> None:
        status, body = self.read_json("/")
        self.assertEqual(status, 200)
        self.assertEqual(body["aplicacao"], "Automacao de Build")
        self.assertEqual(body["mensagem"], "Aplicacao executando com sucesso")

    def test_health_returns_ok(self) -> None:
        status, body = self.read_json("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})

    def test_unknown_route_returns_404(self) -> None:
        status, body = self.read_json("/inexistente")
        self.assertEqual(status, 404)
        self.assertEqual(body, {"erro": "rota nao encontrada"})


if __name__ == "__main__":
    unittest.main()
