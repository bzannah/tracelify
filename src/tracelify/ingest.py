"""Document ingestion and chunking for Tracelify."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Chunk:
    """A chunk of text from a document."""

    text: str
    doc_id: str
    chunk_index: int
    metadata: dict

    @property
    def id(self) -> str:
        """Unique identifier for this chunk."""
        return f"{self.doc_id}::{self.chunk_index}"


def load_document(file_path: Path) -> tuple[str, dict]:
    """Load a text or markdown file and return its content with metadata."""
    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    metadata = {
        "filename": file_path.name,
        "path": str(file_path),
        "extension": file_path.suffix,
    }
    return content, metadata


def chunk_text(
    text: str,
    doc_id: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    metadata: Optional[dict] = None,
) -> list[Chunk]:
    """
    Split text into overlapping chunks.

    Args:
        text: The document text to chunk
        doc_id: Unique identifier for the source document
        chunk_size: Target number of characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
        metadata: Additional metadata to attach to each chunk

    Returns:
        List of Chunk objects
    """
    if not text.strip():
        return []

    metadata = metadata or {}
    chunks = []

    segments = split_into_segments(text, chunk_size, chunk_overlap)

    for i, segment in enumerate(segments):
        chunks.append(
            Chunk(
                text=segment.strip(),
                doc_id=doc_id,
                chunk_index=i,
                metadata=metadata.copy(),
            )
        )

    return chunks


def split_into_segments(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    TODO(human): Implement the chunking logic.

    Split the input text into overlapping segments.

    Args:
        text: The full document text
        chunk_size: Target number of characters per chunk
        overlap: Number of characters to overlap between consecutive chunks

    Returns:
        List of text segments (strings)

    Example:
        text = "Hello world. This is a test."
        chunk_size = 15, overlap = 5
        -> ["Hello world. Th", "d. This is a te", "s a test."]

    Hint: Use a sliding window approach:
        - Start at position 0
        - Take chunk_size characters
        - Move forward by (chunk_size - overlap)
        - Repeat until you've processed all text
    """
    raise NotImplementedError("Implement this function!")


def ingest_document(
    file_path: Path,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    """
    Load and chunk a document in one step.

    Args:
        file_path: Path to the document
        chunk_size: Target characters per chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of Chunk objects ready for embedding
    """
    content, metadata = load_document(file_path)
    doc_id = file_path.stem  # Use filename without extension as doc_id

    return chunk_text(
        text=content,
        doc_id=doc_id,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        metadata=metadata,
    )
