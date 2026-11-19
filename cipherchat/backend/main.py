"""
CipherChat — FastAPI Backend
Provides cryptographic endpoints for text and image encryption/decryption,
attack simulations, and benchmarks across Jordan RNN, Chaotic Map, and AES-GCM.
"""

import sys
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure workspace root and backend dir are in sys.path
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_WORKSPACE_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, "..", ".."))
for p in (_WORKSPACE_ROOT, _CURRENT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from crypto_engines import (
    encrypt_text,
    decrypt_text,
    encrypt_image,
    decrypt_image,
    run_attack_simulation,
    run_benchmark,
)

app = FastAPI(
    title="CipherChat Cryptography API",
    description="Backend cryptographic engine for CipherChat secure messaging laboratory",
    version="1.0.0"
)

# CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response Schemas
# ---------------------------------------------------------------------------

class EncryptTextRequest(BaseModel):
    message: str
    algorithm: str = "jordan"
    sender: str = "alice"


class DecryptTextRequest(BaseModel):
    ciphertext_hex: str
    key_info: Dict[str, Any]
    algorithm: str


class DecryptImageRequest(BaseModel):
    cipher_image_b64: str
    key_info: Dict[str, Any]
    algorithm: str


class AttackSimulationRequest(BaseModel):
    ciphertext_hex: str
    algorithm: str
    key_info: Dict[str, Any]


class BenchmarkRequest(BaseModel):
    message: str = "Meet me at 5 PM."
    iterations: int = 5


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "CipherChat API", "version": "1.0.0"}


@app.post("/api/encrypt-text")
def api_encrypt_text(req: EncryptTextRequest):
    try:
        algo = req.algorithm.lower()
        res = encrypt_text(req.message, algo)
        res["sender"] = req.sender
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/decrypt-text")
def api_decrypt_text(req: DecryptTextRequest):
    try:
        algo = req.algorithm.lower()
        res = decrypt_text(req.ciphertext_hex, req.key_info, algo)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/encrypt-image")
async def api_encrypt_image(
    file: UploadFile = File(...),
    algorithm: str = Form("chaotic")
):
    try:
        content = await file.read()
        algo = algorithm.lower()
        res = encrypt_image(content, algo)
        res["filename"] = file.filename
        res["algorithm"] = algo
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/decrypt-image")
def api_decrypt_image(req: DecryptImageRequest):
    try:
        algo = req.algorithm.lower()
        res = decrypt_image(req.cipher_image_b64, req.key_info, algo)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/attack-simulation")
def api_attack_simulation(req: AttackSimulationRequest):
    try:
        algo = req.algorithm.lower()
        res = run_attack_simulation(req.ciphertext_hex, algo, req.key_info)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/benchmark")
def api_benchmark(req: BenchmarkRequest):
    try:
        results = run_benchmark(req.message, req.iterations)
        return {"results": results, "iterations": req.iterations, "message": req.message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
