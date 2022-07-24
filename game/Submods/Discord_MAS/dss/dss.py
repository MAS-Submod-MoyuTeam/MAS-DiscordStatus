import requests,argparse,time,sqlite3
import pypresence
import psutil
dss=None
status={}

def init():
    dss = pypresence.Client(client_id=status['id'])
    dss.start()
    dss.set_activity(
        state=status['State'],
        details=status['Detail'],
        start=int(status['Start']),
        large_image=status['large_image'],
        large_text=status['large_text'],
        small_image=status['small_image'],
        small_text=status['small_text'],
        buttons=status['Buttons']
    )

# required=True 
def main():
    parser = argparse.ArgumentParser(description='Discord Status Sync')
    parser.add_argument('-i', '--DiscordID',help="Discord APP ID")
    parser.add_argument('-s','--State', help="Discord State")
    parser.add_argument('-d','--Detail',help="Discord Status Detail")
    parser.add_argument('-stt','--Start',help="Start timescamp")
    parser.add_argument('-li','--large_image',help="name of the uploaded image for the large profile artwork")
    parser.add_argument('-lt','--large_text',help="tooltip for the large image")
    parser.add_argument('-si','--small_image',help="name of the uploaded image for the small profile artwork")
    parser.add_argument('-st','--small_text',help="tootltip for the small image")
    parser.add_argument('-b', '--Buttons', help="list of dicts for buttons on your profile in the format")
    args = parser.parse_args()

    status['id'] = args.DiscordID
    status['State'] = args.State
    status['Detail'] = args.Detail
    status['Start'] = args.Start
    status['large_image'] = args.large_image
    status['large_text'] = args.large_text
    status['small_image'] = args.small_image
    status['small_text'] = args.small_text
    status['Buttons'] = args.Buttons

    init()
    Timeout = 60
    while Timeout > 0:
        time.sleep(1)
        Timeout = Timeout -1

main()  