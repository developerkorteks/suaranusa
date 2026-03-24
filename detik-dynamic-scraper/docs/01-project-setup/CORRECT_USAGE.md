# ✅ CORRECT WAY TO USE SIMPLE PAGE

## ❌ WRONG:
```
http://localhost:8000/simple_article_page.html
→ Error: 404 Not Found
```

**Why:** FastAPI doesn't serve HTML files by default.

---

## ✅ CORRECT - Method 1: Open File Directly (EASIEST)

### Step 1: Start API Server
```bash
cd detik-dynamic-scraper
source ../venv_detik/bin/activate
python3 -m uvicorn src.api.main:app --reload
```
Leave this running.

### Step 2: Open HTML File (New Terminal)
```bash
cd detik-dynamic-scraper

# Mac:
open simple_article_page.html

# Linux:
xdg-open simple_article_page.html

# Windows:
start simple_article_page.html

# Or: Double-click file in file explorer
```

**Result:** Page opens in browser at `file:///path/to/simple_article_page.html`

**How it works:**
- HTML file opens from filesystem
- JavaScript inside HTML calls API at http://localhost:8000
- API returns data
- Page displays articles

---

## ✅ CORRECT - Method 2: Python HTTP Server

### Terminal 1: Start API
```bash
cd detik-dynamic-scraper
python3 -m uvicorn src.api.main:app --reload
```

### Terminal 2: Start HTTP Server
```bash
cd detik-dynamic-scraper
python3 -m http.server 8080
```

### Open in Browser:
```
http://localhost:8080/simple_article_page.html
```

**How it works:**
- HTTP server serves HTML at port 8080
- HTML calls API at port 8000
- Both servers work together

---

## ✅ CORRECT - Method 3: Add Static Files to FastAPI

I can add static file serving to FastAPI so you can access:
```
http://localhost:8000/
→ Shows simple_article_page.html
```

Want me to implement this?

---

## 🎯 RECOMMENDED APPROACH

**For Development:** Method 1 (Open file directly)
- Simplest
- No extra server needed
- Works immediately

**For Production:** Method 3 (FastAPI serves HTML)
- Professional
- Single server
- Easier deployment

---

## 📝 QUICK TEST

### 1. Start API:
```bash
cd detik-dynamic-scraper
source ../venv_detik/bin/activate
python3 -m uvicorn src.api.main:app --reload &
```

### 2. Check API Working:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### 3. Open HTML:
```bash
# Mac/Linux:
open simple_article_page.html

# Or in browser, press Ctrl+O and select file
```

### 4. Verify:
- See articles loading
- Search works
- Statistics show

---

## ❓ Which method do you want?

1. ✅ Use Method 1 (open file directly) - Works now!
2. 🔧 Implement Method 3 (FastAPI serves HTML) - I can add this
3. 📚 Just explain how to use - Already done above

