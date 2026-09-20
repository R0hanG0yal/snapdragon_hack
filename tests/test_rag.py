"""
Unit tests for Private Neural Vault (Local RAG Engine).
"""

import pytest
from rag.neural_vault import NeuralVault

def test_neural_vault_ingest_and_query():
    vault = NeuralVault()
    initial_chunks = len(vault.chunks)
    
    # Ingest custom document
    doc_res = vault.add_document("Test Confidential Document", "Qualcomm Hexagon NPU delivers high efficiency for enterprise workflows.")
    assert doc_res["status"] == "indexed"
    assert len(vault.chunks) > initial_chunks
    
    # Query knowledge base
    query_res = vault.query("What does Qualcomm Hexagon NPU deliver?")
    assert "response" in query_res
    assert len(query_res["retrieved_sources"]) > 0
    assert "On-Device" in query_res["privacy_status"]
