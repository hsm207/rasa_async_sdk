import asyncio
import logging
import time
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)
logger = logging.getLogger(__name__)


class ActionLongBackendCallSync(Action):
    def name(self) -> Text:
        return "action_long_backend_call_sync"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        logger.info(
            f"Received request to run action {self.name()} from {tracker.sender_id}"
        )
        time.sleep(5)
        logger.info(
            f"Finished request to run action {self.name()} from {tracker.sender_id}"
        )

        return []


class ActionLongBackendCallAsync(Action):
    def name(self) -> Text:
        return "action_long_backend_call_async"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        logger.info(
            f"Received request to run action {self.name()} from {tracker.sender_id}"
        )
        await asyncio.sleep(5)
        logger.info(
            f"Finished request to run action {self.name()} from {tracker.sender_id}"
        )

        return []
