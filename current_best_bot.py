from forecasting_tools import GeneralLlm
from bots import PerplexityRelatedMarketsScenarioBot


def get_best_bot(publish_reports_to_metaculus: bool = False):
    """
    Returns the current best bot with standardized settings.
    Set publish_reports_to_metaculus=True for tournament/main, False for API, etc.
    """
    llms = {
        "default": GeneralLlm(model="o3", temperature=0.2),
        "summarizer": GeneralLlm(model="o3", temperature=0.2)
    }
    return PerplexityRelatedMarketsScenarioBot(
        llms=llms,
        predictions_per_research_report=5,
        publish_reports_to_metaculus=publish_reports_to_metaculus
    )
