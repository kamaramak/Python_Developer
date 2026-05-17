from bot.core.callbacks.base import BaseCallbackFactory


class CalendarCallbackFactory(BaseCallbackFactory):
    """Фабрика callback для calendar."""

    def calendar_current_race(self):
        return f"{self.section_prefix}:race"
