import datetime

# set up to run every 30 seconds or so...

# Takes in a frame and returns a success/error message. Writes output to a file
def classifyFrame(frame: bytes) -> str:
    # classifier logic...

    # Write some output to file
    try:
        currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        f = open("classifications/" + currentDate + "_classification.txt", "x")

        f.write('some output...')
        f.close()
    except Exception as e:
        print('An error occured: ' + str(e))
        
    