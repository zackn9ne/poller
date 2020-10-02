import argparse

def get_args():
    '''cli args'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true", default=''
    )
    parser.add_argument(
        '-t', action='store', type=float, required=True
    )
    parser.add_argument(
        '-i', action='store_true', default=''
    )

    args = parser.parse_args()

    return args

def init():
    '''return command line args'''
    global DEVenvironment
    global target
    global interactive
    args = get_args()
    if args.dry_run:
        print (f'args are {args}')
        DEVenvironment = True
    else:
        DEVenvironment = False

    if args.i:
        print ('interactive mode')
        interactive = True
    else:
        interactive = False

    target = str(args.t)        