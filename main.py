from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

app = FastAPI(
    title="Sistema de Previsão de Fluxo de Caixa",
    description="API para gerenciamento de vendas e previsão de comissões",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Sistema de Previsão de Fluxo de Caixa API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running!"}

