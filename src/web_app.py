```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CardRequest(BaseModel):
    cards: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OP TCG Price Finder</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 min-h-screen">
        <div class="container mx-auto max-w-lg px-4 py-6">
            <h1 class="text-2xl font-bold mb-4">One Piece TCG Price Finder</h1>
            
            <div class="bg-white rounded-lg shadow-lg p-4 mb-4">
                <textarea
                    id="cardList"
                    class="w-full h-40 p-2 border rounded-md mb-4 font-mono text-sm"
                    placeholder="Enter cards (example):&#13;1xOP07-079&#13;3xOP02-096&#13;2xST06-010"
                ></textarea>
                
                <button
                    onclick="findPrices()"
                    class="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
                    id="searchButton"
                >
                    Find Prices
                </button>
            </div>
            
            <div id="loading" class="hidden">
                <div class="flex items-center justify-center p-4">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                </div>
            </div>
            
            <div id="results" class="space-y-4"></div>
        </div>

        <script>
        async function findPrices() {
            const cardList = document.getElementById('cardList').value;
            const button = document.getElementById('searchButton');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            button.disabled = true;
            loading.classList.remove('hidden');
            results.innerHTML = '';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cards: cardList })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                results.innerHTML = `
                    <div class="bg-red-50 text-red-600 p-4 rounded-lg">
                        Error: ${error.message}
                    </div>
                `;
            } finally {
                button.disabled = false;
                loading.classList.add('hidden');
            }
        }

        function displayResults(data) {
            const results = document.getElementById('results');
            let html = '';

            if (data.best_prices) {
                html += `
                    <div class="bg-green-50 p-4 rounded-lg">
                        <h2 class="font-bold text-lg mb-2">Best Prices Found</h2>
                        <div class="space-y-2">
                `;
                
                Object.entries(data.best_prices).forEach(([card, info]) => {
                    html += `
                        <div class="flex justify-between items-center">
                            <span>${card}</span>
                            <span class="font-bold">${info.store}: $${info.price.toFixed(2)}</span>
                        </div>
                    `;
                });
                
                html += '</div></div>';
            }

            results.innerHTML = html;
        }
        </script>
    </body>
    </html>
    """

@app.post("/api/search")
async def search_prices(request: CardRequest):
    try:
        # Temporary mock response
        return {
            "best_prices": {
                "OP07-079": {"store": "Cherry Collectables", "price": 3.95},
                "OP02-096": {"store": "Card Bot", "price": 2.50}
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

2. Next, create the requirements file:
- Click "Add file" > "Create new file"
- Name: `requirements.txt`
- Copy and paste:

```text
fastapi
uvicorn
aiohttp
beautifulsoup4
pydantic
python-multipart
```

3. Create Vercel configuration:
- Click "Add file" > "Create new file"
- Name: `vercel.json`
- Copy and paste:

```json
{
    "version": 2,
    "builds": [
        {
            "src": "src/web_app.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "src/web_app.py"
        }
    ]
}
```
