from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from train import generate_sample, train # your function that uses the model
app = FastAPI()

# Input structure
class PromptInput(BaseModel):
    prompt: str

# Output structure
class ColorOutput(BaseModel):
    colors: list[str]

@app.post("/generate", response_model=ColorOutput)
def generate_palette(input: PromptInput):
    try:
        result = train()
        return {"colors": result}
    except Exception as e:
        import traceback
        print("ERROR:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))