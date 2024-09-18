class TrainerCallback:
    @staticmethod
    def on_init_start(trainer) -> None:
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

    @staticmethod
    def on_init_end(trainer) -> None:
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

    @staticmethod
    def on_epoch_start(trainer) -> None:
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

    @staticmethod
    def on_epoch_end(trainer) -> None:
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

    @staticmethod
    def on_train_step_start(trainer) -> None:
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

    @staticmethod
    def on_train_step_end(trainer) -> None:
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

    @staticmethod
    def on_keyboard_interrupt(trainer) -> None:
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
