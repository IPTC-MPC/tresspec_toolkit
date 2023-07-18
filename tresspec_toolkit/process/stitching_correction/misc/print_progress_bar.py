def print_progress_bar(iteration, total, current_run, total_number_of_runs, delay, prefix="Progress:",
                       suffix="Complete", digits=2, length=80, fill="█", end_char="\r"):

    # based on a sub on stackoverflow.com which can be found here:
    # https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """

    :param iteration:   index of current iteration (int)
    :param total:       total number of iterations (int)
    :param prefix:      prefix string (str)
    :param suffix:      suffix string (str)
    :param digits:      integer specifying number of digits in printed percentage of progress
    :param length:      character length of bar (integer)
    :param fill:        bar fill character (str)
    :param end_char:    end character (e.g. "\r", "\r\n") (str)
    :return:
    """

    percent = ("{0:." + str(digits) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} (run {current_run} of {total_number_of_runs}, delay = {delay} ps)',
          end=end_char)
    # Print New Line on Complete
    if iteration == total:
        print()
