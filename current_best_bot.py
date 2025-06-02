from forecasting_tools import GeneralLlm
from bots import PerplexityFilteredRelatedMarketsScenarioPerplexityBot


def get_best_bot(publish_reports_to_metaculus: bool = False, skip_previously_forecasted_questions: bool = False):
    """
    Returns the current best bot with standardized settings.
    Set publish_reports_to_metaculus=True for tournament/main, False for API, etc.
    Set skip_previously_forecasted_questions=True to skip questions already forecasted by the bot.
    """
    llms = {
        "default": GeneralLlm(model="metaculus/o3", temperature=0.2),
        "summarizer": GeneralLlm(model="metaculus/o3", temperature=0.2)
    }
    return PerplexityFilteredRelatedMarketsScenarioPerplexityBot(
        llms=llms,
        predictions_per_research_report=5,
        publish_reports_to_metaculus=publish_reports_to_metaculus,
        skip_previously_forecasted_questions=skip_previously_forecasted_questions
    )


def log_report_summary(forecast_reports, raise_errors=False):
    """
    Returns a summary string for a list of forecast reports, using the current best bot's summary logic.
    """
    return PerplexityFilteredRelatedMarketsScenarioPerplexityBot.log_report_summary(forecast_reports, raise_errors=raise_errors)
