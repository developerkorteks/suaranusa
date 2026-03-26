#!/usr/bin/env python3
"""
Scheduled Sync Service
Runs periodic syncs to keep the database updated
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import signal

from storage.database import Database
from repositories.article_repository import ArticleRepository
from services.scraper_service import ScraperService
from services.sync_service import SyncService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScheduledSyncService:
    """Service to run scheduled syncs"""
    
    def __init__(self, db_path: str = "data/comprehensive_full_test.db"):
        """Initialize scheduled sync service"""
        self.db_path = db_path
        self.scheduler = AsyncIOScheduler()
        self.db = None
        self.repo = None
        self.scraper_service = None
        self.sync_service = None
        
        # Sync configuration
        self.articles_per_domain = 10  # Default: 10 articles per domain
        self.running = False
        
    def _initialize_services(self):
        """Initialize database and services"""
        if not self.db:
            self.db = Database(self.db_path)
            self.repo = ArticleRepository(self.db)
            self.scraper_service = ScraperService(self.repo)
            self.sync_service = SyncService(self.repo, self.scraper_service)
            logger.info(f"✓ Services initialized with database: {self.db_path}")
    
    async def run_scheduled_sync(self):
        """Execute a scheduled sync"""
        try:
            logger.info("=" * 80)
            logger.info(f"🔄 Starting Scheduled Sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 80)
            
            # Initialize services if needed
            self._initialize_services()
            
            # Get initial count
            initial_count = self.repo.count()
            logger.info(f"📊 Initial article count: {initial_count}")
            
            # Run sync
            result = await self.sync_service.run_full_sync(
                articles_per_domain=self.articles_per_domain
            )
            
            # Get final count
            final_count = self.repo.count()
            
            # Log results
            logger.info("=" * 80)
            logger.info("✅ Scheduled Sync Complete!")
            logger.info(f"  - Domains processed: {result['domains_processed']}")
            logger.info(f"  - Articles hydrated: {result['total_hydrated']}")
            logger.info(f"  - Duration: {result['duration_seconds']:.2f}s")
            logger.info(f"  - Initial count: {initial_count}")
            logger.info(f"  - Final count: {final_count}")
            logger.info(f"  - Net change: +{final_count - initial_count}")
            logger.info(f"  - Next sync: {self.get_next_run_time()}")
            logger.info("=" * 80)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Scheduled sync failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def add_daily_sync(self, hour: int = 2, minute: int = 0):
        """
        Add daily sync at specific time
        
        Args:
            hour: Hour to run (0-23), default 2 AM
            minute: Minute to run (0-59), default 0
        """
        self.scheduler.add_job(
            self.run_scheduled_sync,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_sync',
            name=f'Daily Sync at {hour:02d}:{minute:02d}',
            replace_existing=True
        )
        logger.info(f"✓ Daily sync scheduled at {hour:02d}:{minute:02d}")
    
    def add_interval_sync(self, hours: int = 6):
        """
        Add sync at regular intervals
        
        Args:
            hours: Interval in hours, default 6 hours
        """
        self.scheduler.add_job(
            self.run_scheduled_sync,
            trigger=IntervalTrigger(hours=hours),
            id='interval_sync',
            name=f'Interval Sync every {hours} hours',
            replace_existing=True
        )
        logger.info(f"✓ Interval sync scheduled every {hours} hours")
    
    def add_custom_schedule(self, cron_expression: str, job_id: str = 'custom_sync'):
        """
        Add custom schedule using cron expression
        
        Args:
            cron_expression: Cron expression (e.g., "0 */6 * * *" for every 6 hours)
            job_id: Unique job ID
        """
        # Parse cron expression
        parts = cron_expression.split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have 5 parts: minute hour day month day_of_week")
        
        minute, hour, day, month, day_of_week = parts
        
        self.scheduler.add_job(
            self.run_scheduled_sync,
            trigger=CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week
            ),
            id=job_id,
            name=f'Custom Sync: {cron_expression}',
            replace_existing=True
        )
        logger.info(f"✓ Custom sync scheduled: {cron_expression}")
    
    def get_next_run_time(self):
        """Get next scheduled run time"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            try:
                # APScheduler 3.x uses next_run_time attribute
                next_runs = [job.next_run_time for job in jobs if hasattr(job, 'next_run_time') and job.next_run_time]
                if next_runs:
                    next_run = min(next_runs)
                    return next_run.strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                # Fallback for older versions
                return "Next run time unavailable"
        return "No jobs scheduled"
    
    def list_jobs(self):
        """List all scheduled jobs"""
        jobs = self.scheduler.get_jobs()
        if not jobs:
            logger.info("No scheduled jobs")
            return []
        
        job_list = []
        logger.info("📋 Scheduled Jobs:")
        for job in jobs:
            info = {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else 'N/A'
            }
            job_list.append(info)
            logger.info(f"  - {info['name']}")
            logger.info(f"    Next run: {info['next_run']}")
        
        return job_list
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        logger.info("=" * 80)
        logger.info("🚀 Starting Scheduled Sync Service")
        logger.info("=" * 80)
        
        # Initialize services
        self._initialize_services()
        
        # Start scheduler
        self.scheduler.start()
        self.running = True
        
        # List scheduled jobs
        self.list_jobs()
        
        logger.info("✓ Scheduler started successfully")
        logger.info(f"✓ Next sync: {self.get_next_run_time()}")
        logger.info("=" * 80)
    
    def stop(self):
        """Stop the scheduler"""
        if not self.running:
            logger.warning("Scheduler not running")
            return
        
        logger.info("Stopping scheduler...")
        self.scheduler.shutdown()
        self.running = False
        logger.info("✓ Scheduler stopped")
    
    async def run_forever(self):
        """Run scheduler forever (blocking)"""
        self.start()
        
        # Setup signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            logger.info(f"\n📛 Received signal {signum}, shutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("✓ Scheduler running. Press Ctrl+C to stop.")
        
        # Keep running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n📛 Keyboard interrupt received")
            self.stop()


async def main():
    """Main function to run scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Detik.com Scheduled Sync Service')
    parser.add_argument('--mode', choices=['daily', 'interval', 'custom'], default='daily',
                       help='Sync mode: daily, interval, or custom')
    parser.add_argument('--hour', type=int, default=2,
                       help='Hour for daily sync (0-23), default: 2')
    parser.add_argument('--minute', type=int, default=0,
                       help='Minute for daily sync (0-59), default: 0')
    parser.add_argument('--interval', type=int, default=6,
                       help='Interval in hours for interval mode, default: 6')
    parser.add_argument('--cron', type=str,
                       help='Cron expression for custom mode (e.g., "0 */6 * * *")')
    parser.add_argument('--articles-per-domain', type=int, default=10,
                       help='Number of articles to sync per domain, default: 10')
    parser.add_argument('--db-path', type=str, default='/root/suaranusa/data/comprehensive_full_test.db',
                       help='Database path')
    parser.add_argument('--run-now', action='store_true',
                       help='Run sync immediately on startup')
    
    args = parser.parse_args()
    
    # Create scheduler service
    service = ScheduledSyncService(db_path=args.db_path)
    service.articles_per_domain = args.articles_per_domain
    
    # Add scheduled job based on mode
    if args.mode == 'daily':
        service.add_daily_sync(hour=args.hour, minute=args.minute)
    elif args.mode == 'interval':
        service.add_interval_sync(hours=args.interval)
    elif args.mode == 'custom':
        if not args.cron:
            print("Error: --cron expression required for custom mode")
            sys.exit(1)
        service.add_custom_schedule(args.cron)
    
    # Run immediately if requested
    if args.run_now:
        logger.info("🚀 Running initial sync immediately...")
        await service.run_scheduled_sync()
    
    # Start scheduler and run forever
    await service.run_forever()


if __name__ == '__main__':
    asyncio.run(main())
