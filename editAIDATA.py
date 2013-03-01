import tictac

if __name__ == '__main__':
    aidata = tictac.load()
    keys = aidata.keys()
    input = ''
    while input != 'Q':
        print "(L)ist, (R)ead, (W)rite"
        input = raw_input("? ")[0].upper()
        if input == 'L':
            for a in range(0, len(keys))[::5][1:]:
                print "%s %s %s %s %s" % ([(keys.index(item), item) for item in keys[a-5:a]])
        elif input == 'R':
            key = int(raw_input("Key? "))
            print aidata[key]
        elif input == 'W':
            pass
        elif input == 'Q':
            pass
        else:
            raise ValueError(input)
    tictac.dump(aidata)