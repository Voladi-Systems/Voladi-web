from subprocess import check_call

def main():
    command = [
        'cat',
        './cronjobs.txt',
        '|',
        'crontab',
        '-',
    ]
    check_call(' '.join(command), shell=True)


if __name__ == '__main__':
    main()
