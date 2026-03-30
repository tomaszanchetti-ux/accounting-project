from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response

from app.repositories import PsycopgRunsRepository
from app.schemas.runs import (
    RunCreateRequest,
    RunDrilldownResponse,
    RunExecuteRequest,
    RunExecuteResponse,
    RunFileReferenceRequest,
    RunResponse,
    RunResultDetailResponse,
    RunResultsResponse,
    RunSummaryResponse,
    UploadedFileResponse,
)
from app.services.runs import (
    RunNotFoundError,
    RunResultNotFoundError,
    RunsService,
)

router = APIRouter(prefix="/runs", tags=["runs"])


def get_runs_service() -> RunsService:
    return RunsService(PsycopgRunsRepository())


@router.post("", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
def create_run(
    request: RunCreateRequest,
    service: RunsService = Depends(get_runs_service),
) -> RunResponse:
    return service.create_run(request)


@router.post(
    "/{run_id}/upload",
    response_model=UploadedFileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_uploaded_file(
    run_id: str,
    request: Request,
    service: RunsService = Depends(get_runs_service),
) -> UploadedFileResponse:
    try:
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("multipart/form-data"):
            form = await request.form()
            uploaded_file = form.get("file")
            file_type = form.get("file_type")
            if (
                uploaded_file is None
                or not hasattr(uploaded_file, "read")
                or not isinstance(file_type, str)
            ):
                raise HTTPException(
                    status_code=422,
                    detail="Multipart upload requires fields 'file' and 'file_type'.",
                )

            try:
                file_bytes = await uploaded_file.read()
                return service.upload_file_bytes(
                    run_id,
                    file_name=uploaded_file.filename or "uploaded.csv",
                    file_type=file_type,
                    file_bytes=file_bytes,
                    content_type=uploaded_file.content_type or "text/csv",
                )
            finally:
                await uploaded_file.close()

        payload = RunFileReferenceRequest.model_validate(await request.json())
        return service.register_file_reference(run_id, payload)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error


@router.post("/{run_id}/execute", response_model=RunExecuteResponse)
def execute_run(
    run_id: str,
    request: RunExecuteRequest | None = None,
    service: RunsService = Depends(get_runs_service),
) -> RunExecuteResponse:
    try:
        return service.execute_run(run_id, request)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/{run_id}/summary", response_model=RunSummaryResponse)
def get_run_summary(
    run_id: str,
    service: RunsService = Depends(get_runs_service),
) -> RunSummaryResponse:
    try:
        return service.get_summary(run_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error


@router.get("/{run_id}/results", response_model=RunResultsResponse)
def list_run_results(
    run_id: str,
    service: RunsService = Depends(get_runs_service),
) -> RunResultsResponse:
    try:
        return service.list_results(run_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error


@router.get("/{run_id}/results/{result_id}", response_model=RunResultDetailResponse)
def get_run_result(
    run_id: str,
    result_id: str,
    service: RunsService = Depends(get_runs_service),
) -> RunResultDetailResponse:
    try:
        return service.get_result_detail(run_id, result_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error
    except RunResultNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=f"Run result not found: {error}",
        ) from error


@router.get(
    "/{run_id}/results/{result_id}/drilldown",
    response_model=RunDrilldownResponse,
)
def get_run_result_drilldown(
    run_id: str,
    result_id: str,
    service: RunsService = Depends(get_runs_service),
) -> RunDrilldownResponse:
    try:
        return service.get_drilldown(run_id, result_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error
    except RunResultNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=f"Run result not found: {error}",
        ) from error


@router.get("/{run_id}/exports/summary")
def export_run_summary(
    run_id: str,
    service: RunsService = Depends(get_runs_service),
) -> Response:
    try:
        export = service.export_summary_csv(run_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error

    return Response(
        content=export.content,
        media_type=export.media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{export.filename}"',
        },
    )


@router.get("/{run_id}/results/{result_id}/exports/detail")
def export_run_result_detail(
    run_id: str,
    result_id: str,
    service: RunsService = Depends(get_runs_service),
) -> Response:
    try:
        export = service.export_exception_detail_csv(run_id, result_id)
    except RunNotFoundError as error:
        raise HTTPException(status_code=404, detail=f"Run not found: {error}") from error
    except RunResultNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=f"Run result not found: {error}",
        ) from error

    return Response(
        content=export.content,
        media_type=export.media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{export.filename}"',
        },
    )
