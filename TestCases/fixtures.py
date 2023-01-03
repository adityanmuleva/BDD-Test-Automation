from behave import fixture
import logging
from TestCases.features.steps.environment_steps import *


@fixture
def dummy_fixture(context):
    try:
        dummy_step()
        logging.info("fixture ran successfully")

    except:
        logging.info("Fixture did not work")
