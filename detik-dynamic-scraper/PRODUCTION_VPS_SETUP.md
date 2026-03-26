# 🚀 Production VPS Setup Guide

**VPS Path:** `/root/suaranusa/detik-dynamic-scraper/`  
**Virtual Environment:** `/root/suaranusa/venv_detik/`  
**Status:** ✅ Ready for Production

---

## 📋 Quick Start

### **1. Verify Installation**

```bash
# Check location
cd /root/suaranusa/detik-dynamic-scraper
pwd

# Activate venv
source /root/suaranusa/venv_detik/bin/activate

# Verify Python packages
pip list | grep -i apscheduler
```

### **2. Test Scheduled Sync**

```bash
# Navigate to project
cd /root/suaranusa/detik-dynamic-scraper

# Activate venv (if not already)
source /root/suaranusa/venv_detik/bin/activate

# Run test sync (2 articles per domain)
python3 src/scheduler.py \
    --mode daily \
    --run-now \
    --articles-per-domain 2 \
    --db-path data/comprehensive_full_test.db
```

### **3. Run Production Sync**

```bash
# Using production script
bash /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh
```

---

## ⚙️ Deployment Options

### **Option 1: Cron Job (Recommended for VPS)**

```bash
# Edit root's crontab
crontab -e

# Add one of these lines:

# Run daily at 2:00 AM
0 2 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Run every 6 hours
0 */6 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Run twice daily (2 AM and 2 PM)
0 2,14 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh
```

**Verify cron job:**
```bash
crontab -l | grep detik
```

---

### **Option 2: Python Scheduler as Background Service**

```bash
# Navigate to project
cd /root/suaranusa/detik-dynamic-scraper

# Activate venv
source /root/suaranusa/venv_detik/bin/activate

# Run scheduler in background
nohup python3 src/scheduler.py \
    --mode interval \
    --interval 6 \
    --articles-per-domain 10 \
    --db-path data/comprehensive_full_test.db \
    > logs/scheduler.log 2>&1 &

# Save PID
echo $! > scheduler.pid

# Check if running
ps aux | grep scheduler.py
```

**Stop background scheduler:**
```bash
# Kill process
kill $(cat /root/suaranusa/detik-dynamic-scraper/scheduler.pid)
```

---

### **Option 3: systemd Service**

Create service file:
```bash
sudo nano /etc/systemd/system/detik-sync.service
```

Service content:
```ini
[Unit]
Description=Detik.com Scheduled Sync Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/suaranusa/detik-dynamic-scraper
ExecStart=/root/suaranusa/venv_detik/bin/python3 src/scheduler.py --mode interval --interval 6 --articles-per-domain 10 --db-path data/comprehensive_full_test.db
Restart=always
RestartSec=60
StandardOutput=append:/root/suaranusa/detik-dynamic-scraper/logs/scheduler.log
StandardError=append:/root/suaranusa/detik-dynamic-scraper/logs/scheduler_error.log

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable detik-sync
sudo systemctl start detik-sync

# Check status
sudo systemctl status detik-sync

# View logs
sudo journalctl -u detik-sync -f

# Stop service
sudo systemctl stop detik-sync
```

---

## 📊 Monitoring

### **Check Logs**

```bash
# View sync logs
tail -f /root/suaranusa/detik-dynamic-scraper/logs/scheduled_sync_$(date +%Y%m%d).log

# View scheduler logs (if running as background)
tail -f /root/suaranusa/detik-dynamic-scraper/logs/scheduler.log

# View systemd logs
sudo journalctl -u detik-sync -n 100 -f
```

### **Check Database**

```bash
cd /root/suaranusa/detik-dynamic-scraper

# Total articles
sqlite3 data/comprehensive_full_test.db "SELECT COUNT(*) FROM articles;"

# Articles by source
sqlite3 data/comprehensive_full_test.db "
SELECT source, COUNT(*) as count 
FROM articles 
WHERE source LIKE '%.detik.com' 
GROUP BY source 
ORDER BY count DESC 
LIMIT 10;
"

# Check for NULL sources
sqlite3 data/comprehensive_full_test.db "
SELECT COUNT(*) 
FROM articles 
WHERE source IS NULL OR source = '';
"
# Should return: 0
```

### **Check Running Processes**

```bash
# Check if scheduler is running
ps aux | grep scheduler

# Check cron jobs
crontab -l | grep detik

# Check systemd service
sudo systemctl status detik-sync
```

---

## 🔧 Configuration

### **Adjust Sync Frequency**

Edit crontab:
```bash
crontab -e

# Examples:
# Every 2 hours
0 */2 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Every 12 hours
0 */12 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Once per day at 3 AM
0 3 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh
```

### **Adjust Articles Per Domain**

Edit `run_scheduled_sync_production.sh`:
```bash
nano /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Change this line:
ARTICLES_PER_DOMAIN=10  # Increase or decrease as needed
```

---

## 🐛 Troubleshooting

### **Issue: Virtual environment not found**

```bash
# Check if venv exists
ls -la /root/suaranusa/venv_detik/

# If missing, create new venv
cd /root/suaranusa
python3 -m venv venv_detik
source venv_detik/bin/activate
pip install -r detik-dynamic-scraper/requirements.txt
```

### **Issue: Permission denied**

```bash
# Make script executable
chmod +x /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Check file permissions
ls -la /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh
```

### **Issue: Database locked**

```bash
# Check for running processes
ps aux | grep python | grep scheduler

# Kill if needed
pkill -f scheduler.py

# Verify database
sqlite3 /root/suaranusa/detik-dynamic-scraper/data/comprehensive_full_test.db ".tables"
```

### **Issue: Import errors**

```bash
# Activate venv and install dependencies
source /root/suaranusa/venv_detik/bin/activate
pip install -r /root/suaranusa/detik-dynamic-scraper/requirements.txt
```

---

## ✅ Production Recommendations

### **For Production VPS:**

1. ✅ **Use Cron Job** - Most reliable for VPS
   ```bash
   0 2 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh
   ```

2. ✅ **Set Reasonable Interval** - Every 6-12 hours
   - Too frequent: May overload server
   - Too infrequent: Miss latest articles

3. ✅ **Monitor Disk Space**
   ```bash
   df -h /root/suaranusa/
   ```

4. ✅ **Enable Log Rotation**
   ```bash
   # Create logrotate config
   sudo nano /etc/logrotate.d/detik-sync
   ```
   
   Content:
   ```
   /root/suaranusa/detik-dynamic-scraper/logs/*.log {
       daily
       rotate 7
       compress
       missingok
       notifempty
   }
   ```

5. ✅ **Setup Alerts** (Optional)
   ```bash
   # Add to cron script for email alerts
   MAILTO=your-email@example.com
   ```

---

## 📁 VPS File Structure

```
/root/suaranusa/
├── venv_detik/                          # Virtual environment
├── detik-dynamic-scraper/
│   ├── src/
│   │   ├── scheduler.py                 # Scheduler
│   │   ├── api/main.py
│   │   └── ...
│   ├── data/
│   │   └── comprehensive_full_test.db   # Database
│   ├── logs/
│   │   ├── scheduler.log
│   │   └── scheduled_sync_YYYYMMDD.log
│   ├── run_scheduled_sync_production.sh # Production script ⭐
│   ├── requirements.txt
│   └── ...
└── ... (other projects)
```

---

## 🚀 Quick Commands Reference

```bash
# Test sync manually
cd /root/suaranusa/detik-dynamic-scraper
source /root/suaranusa/venv_detik/bin/activate
python3 src/scheduler.py --mode daily --run-now --articles-per-domain 2

# Run production script
bash /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Setup cron job
crontab -e
# Add: 0 2 * * * /root/suaranusa/detik-dynamic-scraper/run_scheduled_sync_production.sh

# Check logs
tail -f /root/suaranusa/detik-dynamic-scraper/logs/scheduled_sync_$(date +%Y%m%d).log

# Check database
sqlite3 /root/suaranusa/detik-dynamic-scraper/data/comprehensive_full_test.db "SELECT COUNT(*) FROM articles;"
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Virtual environment activated: `source /root/suaranusa/venv_detik/bin/activate`
- [ ] Dependencies installed: `pip list | grep APScheduler`
- [ ] Script executable: `ls -la run_scheduled_sync_production.sh`
- [ ] Test sync works: Manual run successful
- [ ] Cron job added: `crontab -l | grep detik`
- [ ] Logs directory exists: `ls logs/`
- [ ] Database accessible: `sqlite3 data/comprehensive_full_test.db ".tables"`

---

**Status:** ✅ Ready for Production VPS  
**Path:** `/root/suaranusa/detik-dynamic-scraper/`  
**Script:** `run_scheduled_sync_production.sh`

**Recommended:** Setup cron job for automated daily sync at 2 AM.
