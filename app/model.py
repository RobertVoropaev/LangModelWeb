from fastai.text.all import *
from fastdownload import FastDownload
import fastai.data
import fastai

import logging

logger = logging.getLogger(__name__)

class LanguageModel:
    def __init__(self):
        pass

    def predownload_data(self):
        logger.info("Predownload data")

        fast_download = FastDownload(
            fastai_cfg(),
            module=fastai.data,
            archive=None,
            data=None,
            base='./data'
        )

        data_path = fast_download.get(
            URLs.IMDB,
            force=False,
            extract_key="data"
        )

        data_loader = TextDataLoaders.from_folder(
            data_path,
            is_lm=True,
            valid_pct=0.1
        )

        self.data_path = data_path
        self.data_loader = data_loader

    def preload_model(self):
        logger.info("Preload data")

        learn = language_model_learner(
            self.data_loader,
            AWD_LSTM,
            metrics=[accuracy, Perplexity()],
            path=self.data_path,
            wd=0.1)

        self.learn = learn.to_fp16()

    def set_path_config_in_model(self):
        logger.info("Config model")
        self.learn.path = Path(".")
        self.learn.model_dir = Path("models")

    def predict(self, input_text, temp, size):
        logger.info("Predict data")
        preds = [self.learn.predict(input_text, 40, temperature=float(temp))
                 for _ in range(size)]
        return "\n".join(preds)
