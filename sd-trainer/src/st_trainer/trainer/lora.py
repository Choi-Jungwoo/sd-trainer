from st_trainer.trainer.process import TrainerProcess


class LoraTrainerProcess(TrainerProcess):
    def __init__(self):
        super(LoraTrainerProcess, self).__init__(
            'lora-trainer',
            'accelerate',
            args=['launch', '--num_cpu_threads_per_process=8', './sd-scripts/train_network.py'],
        )
