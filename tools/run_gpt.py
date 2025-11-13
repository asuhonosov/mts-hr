from __future__ import annotations

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._models.completions.config import ReasoningMode
from yandex_cloud_ml_sdk._models.completions.result import GPTModelResult

from settings import YCSettings


class ModelRunner:
    def __init__(self, yc_settings: YCSettings | None = None):
        self._yc_settings = yc_settings or YCSettings()
        self._sdk = YCloudML(folder_id=self._yc_settings.folder_id, auth=self._yc_settings.token)

    def run_text(
        self,
        model_uri: str,
        text: str,
        system_prompt: str | None = None,
        reasoning_mode: ReasoningMode = ReasoningMode.DISABLED,
        model_version: str = 'latest',
    ) -> GPTModelResult:
        model = self._sdk.models.completions(model_name=model_uri, model_version=model_version)

        context = []
        if system_prompt is not None:
            context.append({'role': 'system', 'text': system_prompt})

        context.append({"role": "user", "text": text})

        model = model.configure(reasoning_mode=reasoning_mode)
        return model.run(context)
