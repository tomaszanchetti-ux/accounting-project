from pathlib import Path

from supabase import Client, create_client

from app.core.settings import get_settings


def get_storage_client() -> Client:
    settings = get_settings()

    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise ValueError("Supabase storage credentials are not configured.")

    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def build_storage_path(run_id: str, filename: str, artifact_type: str = "inputs") -> str:
    safe_name = Path(filename).name
    return f"runs/{run_id}/{artifact_type}/{safe_name}"


def upload_file_to_bucket(bucket_name: str, storage_path: str, file_bytes: bytes) -> None:
    client = get_storage_client()
    client.storage.from_(bucket_name).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": "text/plain", "upsert": "true"},
    )


def download_file_from_bucket(bucket_name: str, storage_path: str) -> bytes:
    client = get_storage_client()
    return client.storage.from_(bucket_name).download(storage_path)


def remove_file_from_bucket(bucket_name: str, storage_path: str) -> None:
    client = get_storage_client()
    client.storage.from_(bucket_name).remove([storage_path])

