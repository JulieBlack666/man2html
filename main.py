import argparse

from man_parser import ManParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts man file to html')
    parser.add_argument('man', type=str, help='Man file name')
    parser.add_argument('-f', '--html', type=str, help='Html file name')
    args = parser.parse_args()
    try:
        if args.html is None:
            man2html = ManParser(args.man)
        else:
            man2html = ManParser(args.man, args.html)
    except FileNotFoundError:
        print('No such file in directory')
    except TypeError:
        print('Not a man file')
    else:
        man2html.parse_file()
