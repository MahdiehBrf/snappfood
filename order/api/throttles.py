from rest_framework.throttling import AnonRateThrottle


class DelayReportThrottle(AnonRateThrottle):
    scope = "delay_report"
    rate = "1/min"
