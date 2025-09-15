def linear_schedule(initial_value):
    """
    Linear learning rate schedule. From https://github.com/araffin/rl-baselines-zoo/blob/master/utils/utils.py#L225
    :param initial_value: (float or str)
    :return: (function)
    """
    if isinstance(initial_value, str):
        initial_value = float(initial_value)

    def func(progress):
        """
        Progress will decrease from 1 (beginning) to 0
        :param progress: (float)
        :return: (float)
        """
        return progress * initial_value

    return func