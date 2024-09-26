from pydantic import BaseModel as PydanticBaseModel


class HyperParametersConfigModel(PydanticBaseModel):
    pass


class BaseFineTuneConfigModel(PydanticBaseModel):
    """
    Data Model for the configs
    """

    instruction: str = "text-summarization"
    # hyperparameters: HyperParametersConfigModel


class BaseFineTune:
    """
    Class which provides base structure for fine tuning models
    """

    config_class = BaseFineTuneConfigModel

    def __init__(self, **kwargs) -> None:
        self.config = self.config_class(**kwargs)

    def load_model(self):
        pass

    def load_dataset(self):
        pass

    def train(self):
        pass

    def tune(self):
        pass

    def evaluate(self):
        pass
