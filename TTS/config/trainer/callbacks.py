from typing import Callable, Dict


class TrainerCallback:
    def __init__(self) -> None:
        self.callbacks_on_init_start = []
        self.callbacks_on_init_end = []
        self.callbacks_on_epoch_start = []
        self.callbacks_on_epoch_end = []
        self.callbacks_on_train_epoch_start = []
        self.callbacks_on_train_epoch_end = []
        self.callbacks_on_train_step_start = []
        self.callbacks_on_train_step_end = []
        self.callbacks_on_keyboard_interrupt = []

    def parse_callbacks_dict(self, callbacks_dict: Dict[str, Callable]) -> None:
        for key, value in callbacks_dict.items():
            if key == "on_init_start":
                self.callbacks_on_init_start.append(value)
            elif key == "on_init_end":
                self.callbacks_on_init_end.append(value)
            elif key == "on_epoch_start":
                self.callbacks_on_epoch_start.append(value)
            elif key == "on_epoch_end":
                self.callbacks_on_epoch_end.append(value)
            elif key == "on_train_epoch_start":
                self.callbacks_on_train_epoch_start.append(value)
            elif key == "on_train_epoch_end":
                self.callbacks_on_train_epoch_end.append(value)
            elif key == "on_train_step_start":
                self.callbacks_on_train_step_start.append(value)
            elif key == "on_train_step_end":
                self.callbacks_on_train_step_end.append(value)
            elif key == "on_keyboard_interrupt":
                self.callbacks_on_keyboard_interrupt.append(value)
            else:
                raise ValueError(f"Invalid callback key: {key}")

    def on_init_start(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_init_start"):
                TTS.Trainer.trainer.model.module.on_init_start(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_init_start"):
                TTS.Trainer.trainer.model.on_init_start(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_init_start"):
            TTS.Trainer.trainer.criterion.on_init_start(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_init_start"):
            TTS.Trainer.trainer.optimizer.on_init_start(trainer)

        if self.callbacks_on_init_start:
            for callback in self.callbacks_on_init_start:
                callback(trainer)

    def on_init_end(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_init_end"):
                TTS.Trainer.trainer.model.module.on_init_end(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_init_end"):
                TTS.Trainer.trainer.model.on_init_end(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_init_end"):
            TTS.Trainer.trainer.criterion.on_init_end(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_init_end"):
            TTS.Trainer.trainer.optimizer.on_init_end(trainer)

        if len(self.callbacks_on_init_end) > 0:
            for callback in self.callbacks_on_init_end:
                callback(trainer)

    def on_epoch_start(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_epoch_start"):
                TTS.Trainer.trainer.model.module.on_epoch_start(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_epoch_start"):
                TTS.Trainer.trainer.model.on_epoch_start(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_epoch_start"):
            TTS.Trainer.trainer.criterion.on_epoch_start(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_epoch_start"):
            TTS.Trainer.trainer.optimizer.on_epoch_start(trainer)

        if self.callbacks_on_epoch_start:
            for callback in self.callbacks_on_epoch_start:
                callback(trainer)

    def on_epoch_end(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_epoch_end"):
                TTS.Trainer.trainer.model.module.on_epoch_end(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_epoch_end"):
                TTS.Trainer.trainer.model.on_epoch_end(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_epoch_end"):
            TTS.Trainer.trainer.criterion.on_epoch_end(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_epoch_end"):
            TTS.Trainer.trainer.optimizer.on_epoch_end(trainer)

        if self.callbacks_on_epoch_end:
            for callback in self.callbacks_on_epoch_end:
                callback(trainer)

    def on_train_epoch_start(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_train_epoch_start"):
                TTS.Trainer.trainer.model.module.on_train_epoch_start(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_train_epoch_start"):
                TTS.Trainer.trainer.model.on_train_epoch_start(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_train_epoch_start"):
            TTS.Trainer.trainer.criterion.on_train_epoch_start(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_train_epoch_start"):
            TTS.Trainer.trainer.optimizer.on_train_epoch_start(trainer)

        if self.callbacks_on_train_epoch_start:
            for callback in self.callbacks_on_train_epoch_start:
                callback(trainer)

    def on_train_epoch_end(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_train_epoch_end"):
                TTS.Trainer.trainer.model.module.on_train_epoch_end(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_train_epoch_end"):
                TTS.Trainer.trainer.model.on_train_epoch_end(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_train_epoch_end"):
            TTS.Trainer.trainer.criterion.on_train_epoch_end(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_train_epoch_end"):
            TTS.Trainer.trainer.optimizer.on_train_epoch_end(trainer)

        if self.callbacks_on_train_epoch_end:
            for callback in self.callbacks_on_train_epoch_end:
                callback(trainer)

    @staticmethod
    def before_backward_pass(trainer, loss_dict) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "before_backward_pass"):
                TTS.Trainer.trainer.model.module.before_backward_pass(loss_dict, TTS.Trainer.trainer.optimizer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "before_backward_pass"):
                TTS.Trainer.trainer.model.before_backward_pass(loss_dict, TTS.Trainer.trainer.optimizer)

    @staticmethod
    def before_gradient_clipping(trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "before_gradient_clipping"):
                TTS.Trainer.trainer.model.module.before_gradient_clipping()
        else:
            if hasattr(TTS.Trainer.trainer.model, "before_gradient_clipping"):
                TTS.Trainer.trainer.model.before_gradient_clipping()

    def on_train_step_start(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_train_step_start"):
                TTS.Trainer.trainer.model.module.on_train_step_start(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_train_step_start"):
                TTS.Trainer.trainer.model.on_train_step_start(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_train_step_start"):
            TTS.Trainer.trainer.criterion.on_train_step_start(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_train_step_start"):
            TTS.Trainer.trainer.optimizer.on_train_step_start(trainer)

        if self.callbacks_on_train_step_start:
            for callback in self.callbacks_on_train_step_start:
                callback(trainer)

    def on_train_step_end(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_train_step_end"):
                TTS.Trainer.trainer.model.module.on_train_step_end(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_train_step_end"):
                TTS.Trainer.trainer.model.on_train_step_end(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_train_step_end"):
            TTS.Trainer.trainer.criterion.on_train_step_end(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_train_step_end"):
            TTS.Trainer.trainer.optimizer.on_train_step_end(trainer)

        if self.callbacks_on_train_step_end:
            for callback in self.callbacks_on_train_step_end:
                callback(trainer)

    def on_keyboard_interrupt(self, trainer) -> None:
        if hasattr(TTS.Trainer.trainer.model, "module"):
            if hasattr(TTS.Trainer.trainer.model.module, "on_keyboard_interrupt"):
                TTS.Trainer.trainer.model.module.on_keyboard_interrupt(trainer)
        else:
            if hasattr(TTS.Trainer.trainer.model, "on_keyboard_interrupt"):
                TTS.Trainer.trainer.model.on_keyboard_interrupt(trainer)

        if hasattr(TTS.Trainer.trainer.criterion, "on_keyboard_interrupt"):
            TTS.Trainer.trainer.criterion.on_keyboard_interrupt(trainer)

        if hasattr(TTS.Trainer.trainer.optimizer, "on_keyboard_interrupt"):
            TTS.Trainer.trainer.optimizer.on_keyboard_interrupt(trainer)

        if self.callbacks_on_keyboard_interrupt:
            for callback in self.callbacks_on_keyboard_interrupt:
                callback(trainer)
