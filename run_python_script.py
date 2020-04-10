import cProfile
import sys


script_names = ["pipeline", "acceptance"]

script_names_str = script_names.__repr__()


def run_python_script(script_name, *args, **kwargs):
    if 'profiler' in kwargs:
        use_profiler = True
    else:
        use_profiler = False

    if script_name == 'show':
        print("\nAvailable scripts\n----------------")
        for s in script_names:
            print(s)

        exit(0)

    if profiler:
        print("running with profiler")

    if script_name == "pipeline":
        from scripts import pipeline as script

    elif script_name == "acceptance":
        from scripts import acceptance as script

    else:
        message = "Error, script_name (%s) must be one of %s" % (script_name,
                                                                 script_names_str)
        raise ValueError(message)

    if profiler:
        command = "script.main(*args)"
        filename = "%s.prof" % script_name
        cProfile.runctx(command, None, locals(), filename=filename)
        print("To see profiler result, run:\nsnakeviz %s" % filename)
    else:
        script.main(*args)


if __name__ == "__main__":
    profiler = ' -p' in ' '.join(sys.argv)
    script = sys.argv[1]
    arguments = sys.argv[2:]
    # remove the profile flag now that profiler is on
    arguments = [i for i in arguments if i != '-p']
    run_python_script(script, arguments, profiler=profiler)
