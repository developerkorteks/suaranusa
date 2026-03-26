module.exports = {
  apps: [
    {
      name: "suaranusa-api",
      cwd: "/root/suaranusa/detik-dynamic-scraper",
      script: "/root/suaranusa/venv_detik/bin/python3",
      args: "-m uvicorn src.api.main:app --port 65080 --host 127.0.0.1",
      env: {
        DATABASE_PATH: "/root/suaranusa/data/comprehensive_full_test.db",
        PYTHONPATH: "/root/suaranusa/detik-dynamic-scraper/src"
      }
    },
    {
      name: "suaranusa-portal",
      cwd: "/root/suaranusa",
      script: "/root/suaranusa/venv_detik/bin/python3",
      args: "manage.py runserver 0.0.0.0:65081",
      env: {
        API_BASE_URL: "http://127.0.0.1:65080",
        DEBUG: "False"
      }
    }
  ]
}
