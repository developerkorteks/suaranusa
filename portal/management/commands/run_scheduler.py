import logging
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from portal.tasks import sync_all_news

logger = logging.getLogger(__name__)

# The `close_old_connections` decorator ensures that database connections, 
# that may have become stale or timed out, are closed before and after your job is run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries from the database.
    It helps to keep the database small by only keeping execution logs for a week.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler for suaranusa news synchronization."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 1. Sync Job - Midnight (00:00)
        scheduler.add_job(
            sync_all_news,
            trigger=CronTrigger(hour=0, minute=0),
            id="sync_midnight",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'sync_midnight' for 00:00.")

        # 2. Sync Job - Midday (12:00)
        scheduler.add_job(
            sync_all_news,
            trigger=CronTrigger(hour=12, minute=0),
            id="sync_midday",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'sync_midday' for 12:00.")

        # 3. Cleanup Job - Every Monday at 03:00
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour=3, minute=0),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly cleanup job.")

        try:
            logger.info("Starting suaranusa news scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
