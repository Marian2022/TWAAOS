from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Gestiune inventar", version="1.0.0")


class Produs(BaseModel):
    id: int
    nume: str
    pret: float
    stoc: int = 0


inventar: list[Produs] = []


@app.get("/produse")
def obtine_toate_produsele(stoc_minim: int | None = None):
    if stoc_minim is None:
        return inventar
    return [produs for produs in inventar if produs.stoc < stoc_minim]


@app.get("/produse/{produs_id}")
def obtine_produs(produs_id: int):
    for produs in inventar:
        if produs.id == produs_id:
            return produs
    raise HTTPException(status_code=404, detail=f"Produsul cu ID-ul {produs_id} nu a fost găsit.")


@app.post("/produse", status_code=201)
def adauga_produs(produs: Produs):
    inventar.append(produs)
    return produs


@app.put("/produse/{produs_id}")
def actualizeaza_produs(produs_id: int, produs_nou: Produs):
    for i, produs in enumerate(inventar):
        if produs.id == produs_id:
            inventar[i] = produs_nou
            return produs_nou
    raise HTTPException(status_code=404, detail=f"Produsul cu ID-ul {produs_id} nu a fost găsit.")


@app.delete("/produse/{produs_id}")
def sterge_produs(produs_id: int):
    for i, produs in enumerate(inventar):
        if produs.id == produs_id:
            return inventar.pop(i)
    raise HTTPException(status_code=404, detail=f"Produsul cu ID-ul {produs_id} nu a fost găsit.")