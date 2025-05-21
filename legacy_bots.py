"""
This file contains legacy bot implementations that are no longer in active use.
These bots are kept for reference and historical purposes.
"""

from forecasting_tools import (
    ForecastBot, ReasonedPrediction, BinaryQuestion, MultipleChoiceQuestion, NumericQuestion, NumericDistribution, PredictedOptionList,
    GeneralLlm, PredictionExtractor, clean_indents
)
from tools import get_related_markets_from_adjacent_news, get_web_search_results_from_openrouter, fermi_estimate_with_llm, get_perplexity_research_from_openrouter, log_report_summary_returning_str
from datetime import datetime
import traceback

PROBABILITY_FINAL_ANSWER_LINE = (
    "Before giving your final answer, rewrite the question as a probability statement (e.g., "
    "\"What is the probability that [event] will happen?\"), making sure it matches the outcome you are forecasting. "
    "Then, the last thing you write is your final answer as: \"Probability: ZZ%\", 0-100 (no decimals, do not include a space between the number and the % sign)."
) 