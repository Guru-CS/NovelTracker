try:
    with open("NovelTrackerFile",'r') as file:
        print("Opening Existing File")
except :
    with open ("NovelTrackerFile",'w') as file:
        print("New File Is Made")

def main():

