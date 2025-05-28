from forecasting_tools import GeneralLlm
from bots import PerplexityFilteredRelatedMarketsScenarioPerplexityBot


def get_best_bot(publish_reports_to_metaculus: bool = False):
    """
    Returns the current best bot with standardized settings.
    Set publish_reports_to_metaculus=True for tournament/main, False for API, etc.
    """
    llms = {
        "default": GeneralLlm(model="metaculus/o3", temperature=0.2),
        "summarizer": GeneralLlm(model="metaculus/o3", temperature=0.2)
    }
    return PerplexityFilteredRelatedMarketsScenarioPerplexityBot(
        llms=llms,
        predictions_per_research_report=5,
        publish_reports_to_metaculus=publish_reports_to_metaculus
    )


def log_report_summary(forecast_reports):
    """
    Returns a summary string for a list of forecast reports, using the current best bot's summary logic.
    """
    return PerplexityFilteredRelatedMarketsScenarioPerplexityBot.log_report_summary(forecast_reports)
