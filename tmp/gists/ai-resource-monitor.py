import psutil
import GPUtil
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class AIResourceMonitor:
    """Monitor AI workload resource usage and detect anomalies."""

    def __init__(self, cpu_threshold: float = 80.0, mem_threshold: float = 90.0):
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold

    def get_gpu_stats(self) -> List[Dict]:
        """Get current GPU utilization."""
        gpus = GPUtil.getGPUs()
        return [{
            'id': gpu.id,
            'load': gpu.load * 100,
            'memory_used': gpu.memoryUsed,
            'memory_total': gpu.memoryTotal,
            'temperature': gpu.temperature
        } for gpu in gpus]

    def check_suspicious_activity(self) -> List[Dict]:
        """Detect potentially malicious processes."""
        suspicious_processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if proc.info['cpu_percent'] > self.cpu_threshold:
                    logger.warning(f"High CPU usage detected: {proc.info['name']} ({proc.info['cpu_percent']}%)")
                    suspicious_processes.append(proc.info)

                if proc.info['memory_percent'] > self.mem_threshold:
                    logger.warning(f"High memory usage detected: {proc.info['name']} ({proc.info['memory_percent']}%)")
                    suspicious_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return suspicious_processes
