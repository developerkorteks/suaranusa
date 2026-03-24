module.exports = {
  apps: [
    {
      name: "suaranusa-api",
      script: "./venv_detik/bin/python",
      args: "src/api/main.py",
      cwd: "./detik-dynamic-scraper",
      interpreter: "none",
      env: {
        PYTHONPATH: "./src",
        API_PORT: 65080,
        API_HOST: "127.0.0.1"
      }
    },
    {
      name: "suaranusa-portal",
      script: "./venv_detik/bin/python",
      args: "manage.py runserver 127.0.0.1:65081 --noreload",
      cwd: ".",
      interpreter: "none",
      env: {
        API_BASE_URL: "http://localhost:65080"
      }
    },
    {
      name: "suaranusa-scheduler",
      script: "./venv_detik/bin/python",
      args: "manage.py run_scheduler",
      cwd: ".",
      interpreter: "none"
    }
  ]
};
