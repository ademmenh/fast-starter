from fastapi import APIRouter
from src.shared.presentation.responses import Response


class AppController:
    def __init__(self, router: APIRouter) -> None:
        self.router = router
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.get("/health", response_model=Response[str])(self.health_check)

    async def health_check(self) -> Response[str]:
        return Response(
            message="Service Healthy",
            status_code=200,
            data="ok",
        )
