from fastapi import FastAPI,HTTPException, status
from libs.NaturalNumber import NaturalNumber

app = FastAPI()

natural = NaturalNumber()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/numero-natural/{numero}",  status_code=status.HTTP_202_ACCEPTED)
async def remover_numero(numero: int):
    try:
        natural.remover_numero(numero=numero)
        return {"message": f"Número {numero} extraído correctamente."}
    except Exception as e:  
        raise HTTPException(status_code=400, detail=str(e))    
    
@app.get("/numero-natural/mostrar-todo", status_code=status.HTTP_200_OK)
async def mostrar_numeros():
    return {"message": natural.mostrar()}

@app.post("/numero-natural/calcular-faltante", status_code=status.HTTP_201_CREATED)
async def calcular_faltantes():
    try:
        return {"message": natural.calcular_faltantes()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/numero-natural/encontrados", status_code=status.HTTP_102_PROCESSING)
async def mostrar_encontrados():
    try:
        return {"message": natural.mostrar_encontrados()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))