from typing import Optional
from PyPDF2 import PdfReader

async def extract_text_from_upload(filename: Optional[str], content: bytes) -> str:
    if not content:
        return ""
    if filename and filename.lower().endswith('.pdf'):
        try:
            import io
            reader = PdfReader(io.BytesIO(content))
            texts = []
            for page in reader.pages:
                try:
                    texts.append(page.extract_text() or '')
                except Exception:
                    continue
            return "\n".join(texts).strip()
        except Exception:
            return ""
    # default: treat as text
    try:
        return content.decode('utf-8', errors='ignore')
    except Exception:
        return ""
