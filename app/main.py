from fastapi import FastAPI

from .api.routes.summary import router as summary_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="SEBIT Summary API",
        version="0.1.0",
        description="Aggregates SEBIT model outputs into financial reporting payloads.",
    )

    app.include_router(summary_router, prefix="/summary", tags=["Reporting"])

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
