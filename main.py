"""
Project Name: Novel Tracker
Developer: Guru
Date: 2026-14-11
Purpose: This app manages your Novel data by persisting data to NovelTrackerFile.
"""
import tempfile as tf
import os
import time 

file_name="NovelTrackerFile.txt"
start_mes = "Here are your options, "
set_start = ["Log","List Novels","Show Tier List","Access a Novel's Data"]

log_mes="Alrighty, Lets Log!"
set_log=["Change Log For Previous Novel", "Log New Novel"]

data_format_novel = ["Name","Status","Current Chapter","Time Spent","Tier","Notes"]
tier_options = ["S Tier", "A Tier", "B Tier", "C Tier", "D Tier", "F Tier"]
status_options = ["Reading", "Stopped", "Novel in Hiatus"]
time_options = ["Start Stopwatch", "Manual"]

def get_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
        except:
            print("Invalid input. Enter a number.")
            continue

        if min_val is not None and value < min_val:
            print(f"Enter a number >= {min_val}")
            continue

        if max_val is not None and value > max_val:
            print(f"Enter a number <= {max_val}")
            continue

        return value

def get_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = float(input(prompt))
        except:
            print("Invalid input. Enter a number.")
            continue

        if min_val is not None and value < min_val:
            print(f"Enter a number >= {min_val}")
            continue

        if max_val is not None and value > max_val:
            print(f"Enter a number <= {max_val}")
            continue

        return value
    
def print_indexed_list(inp_list,indent="",sep=": ",endline="\n",ending="\n"):
    for num,choice in enumerate(inp_list, start=1):
        if "," in endline and num==len(inp_list):
            endline=""
        print(f'{indent}{num}{sep}{choice}',end=endline)
    print(f'{ending}',end="")

def field_insert(dict,key):
    if key == "Name":
        name = input(f"Enter '{key}': "  )
        dict[key]=name
        return dict
    if key == "Status":
        print_indexed_list(status_options,endline=", ")
        status_num=get_int(f"Enter '{key}': ",1,len(status_options))
        dict[key] = status_options[status_num-1]
        return dict 
    if key == "Current Chapter":
        chapter=get_float(f"Enter '{key}': ",min_val=0)
        dict[key] = f"{chapter:g}"
        return dict 
    if key == "Notes":
        with tf.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as f:
            f.write("Here Are Your Notes!\nEdit Them As You Like Ctrl S And Close When Done (Write Them Under the First Two Lines)\n\n")
            f.write(dict[key]or"")
            temp_path = f.name
        os.system(f'notepad "{temp_path}"')
        with open(temp_path, "r") as f:
            f.readline()  
            f.readline()  
            dict[key] = f.read().strip()
        os.remove(temp_path)
        return dict
    if key == "Time Spent":
        print("Alright do you want to, ")
        print_indexed_list(time_options,indent=" ")
        time_change = get_int("Enter Num: ",1,2)
        if time_options[time_change-1]=="Manual":
            while True:
                time_inp = input("Enter Time (Ex: 2:02:23): ")
                try:
                    h,m,s=map(int,time_inp.strip().split(":"))
                except:
                    print("Invalid Input")
                else:
                    if dict[key] == None:
                        old_seconds=0
                    else:
                        old_h, old_m, old_s = map(int, dict[key].split(":"))
                        old_seconds = old_h*3600 + old_m*60 + old_s
                    new_seconds = h*3600 + m*60 + s
                    total_seconds=old_seconds+new_seconds
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    dict[key] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    return dict               
        total = 0
        running = False
        start_time=0
        while True: 
            action=input("Enter start / stop / quit / time: ").lower().strip()
            if action == "start":
                if not running:
                    running =True
                    start_time = time.time()
                    print("Stopwatch running...")
                    elapsed =  time.time() - start_time
                else:
                    print("Already Running.")
            elif action == "stop":
                if running:
                    running = False
                    elapsed = time.time() - start_time
                    total += elapsed
                    print(f"\nPaused at {time_format}")
                else:
                    print("Stopwatch is not running.")
            elif action == "time":
                if running:
                    elapsed = time.time() - start_time + total
                else:
                    elapsed = total
                seconds = int(elapsed)
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                secs = seconds % 60
                time_format = f"{hours:02d}:{minutes:02d}:{secs:02d}"
                print(f"Time Elapsed: {time_format}")
            elif action == "quit":
                print(f"Final time: {time_format}")
                break
            else:
                print("Invalid Input")
        old_h, old_m, old_s = map(int, dict[key].split(":"))
        old_seconds = old_h*3600 + old_m*60 + old_s
        total_seconds = old_seconds + int(total)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        dict[key] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return dict

    if key=="Tier":
        print("Choose A Tier, ")
        print_indexed_list(tier_options,indent=" ")
        option = get_int("Enter Num: ",1,len(tier_options))
        tier=tier_options[option-1]
        dict[key]=tier[0]
        return dict

def update_novel(novel_name,novel_data,filename):
        values = [novel_data[key] for key in data_format_novel]
        updated_line = ",".join(values)
        with open(filename,'r') as file:
            lines=file.readlines()
        with open(filename, "w") as file:
            novel_found = False
            for line in lines:             
                if novel_name.lower() in line.lower():
                    file.write(updated_line + "\n")
                    novel_found = True
                else:
                    file.write(line)  
            if not novel_found:
                file.write(updated_line + "\n")
            
def log_prev(filename):
    novel_found=False
    novel_name=""
    novel=input("Enter Novel Name: ").lower().strip()
    with open(filename,'r') as file:
        for line in file:
            if line.strip()!="":
                values = line.strip().split(",")
                novel_data = dict(zip(data_format_novel, values))
                novel_name=novel_data.get("Name")
                if novel_data.get("Name").lower().strip().replace(" ","")== novel.strip().lower().replace(" ",""):
                    novel_found=True
                    print(f"Here is the novel, \n {novel_data}")
                    print("What would you like to change?")
                    keys = list(novel_data.keys())
                    print_indexed_list(keys, endline=", ")
                    choice_num = get_int("Enter Num: ", 1, len(keys))
                    key = keys[choice_num - 1]
                    novel_data = field_insert(novel_data, key)
                    break
    if not novel_found:
        print("Novel not found")
    else:
        update_novel(novel_name,novel_data,filename)

def log_new(filename):
    print("Alrighty Fill In the Following")
    novel_data={key: None for key in data_format_novel}
    for key in data_format_novel:
        novel_data=field_insert(novel_data,key)
    print(f'Alright here is what you inputted,\n {novel_data}')
    update_novel(novel_data["Name"],novel_data,filename)

def choice(start_mes, choices):
    
    while True:
        print(start_mes)
        print_indexed_list(choices,indent=" ")
        value = get_int("Enter Num: ",1,len(choices))
        return choices[value-1] 

def access(filename):
    name = input("Alrighty Whats The Name of The Novel: ")
    with open(filename,'r') as file:
        for line in file:
            if line.strip()!="":
                values = line.strip().split(",")
                novel_data = dict(zip(data_format_novel, values))
                novel_name=novel_data.get("Name")
                if novel_data.get("Name").lower().strip().replace(" ","")== name.strip().lower().replace(" ",""):
                    novel_found=True
                    return print(f"Here is the novel, \n {novel_data}") 
    print("Novel not found")

def show(filename):
    print("Here's the List of novels, ")
    novel_names=[]
    with open(filename,'r') as file:
        for line in file:
            if line.strip() != "":
                values = line.strip().split(",")
                novel_data = dict(zip(data_format_novel, values))
                novel_names.append(novel_data.get("Name"))
    print_indexed_list(novel_names,indent=" ")

def showtiers(filename):
    print("Here's the Tiers of novels, ")
    tiered_novels = {tier: [] for tier in tier_options}
    with open(filename,'r') as file:
        for line in file:
            if line.strip() != "":
                values = line.strip().split(",")
                novel_data = dict(zip(data_format_novel, values))
                print(novel_data)
                tier_key = novel_data["Tier"] + " Tier"
                tiered_novels[tier_key].append(novel_data)
    for tier, novels in tiered_novels.items():
        print(f"  {tier}: ", end="")

        if novels:
            names = ", ".join(novel["Name"] for novel in novels)
            print(names)
        else:
            print("(none)")
   
actions = {

    1:log_prev,
    2:log_new,
    3:show,
    4:showtiers,
    5:access  
}

def main():
    global file_name
    try:
        with open("NovelTrackerFile.txt",'r') as file:
            print("Opening Existing File")
    except :
        with open ("NovelTrackerFile.txt",'w') as file:
            print("New File Is Made")
    print("Welcome to your Novel Tracker!")
    Running=True
    while Running:
        Loop = True
        Loop_2 = True
        next=choice(start_mes,set_start)
        if next == "Log":
            print(log_mes)
            print_indexed_list(set_log,indent=" ")
            value = get_int("Enter Num: ",1,len(set_log))
            actions[value](file_name)
        elif next == "List Novels":
            actions[3](file_name)
        elif next == "Show Tier List":
            actions[4](file_name)
        elif next == "Access a Novel's Data":
            actions[5](file_name)
        while Loop:
            loop_inp=input("Would You Like to Continue[Y/N]?: ")
            if loop_inp.strip().lower()=="y":
                while Loop_2:
                    clear_inp=input("\nWould You Like to Clear Console[Y/N]?: ")
                    if clear_inp.strip().lower()=="y":
                        os.system("cls")
                        Loop_2=False
                    elif clear_inp.strip().lower()=="n":
                        Loop_2=False
                    else:
                        print("Invalid Input Try Again.")
                break
            elif loop_inp.strip().lower()=="n":
                Loop=False
                print("See You Soon! Exiting...")
                Running=False
            else:
                print("Invalid Input Try Again")
if __name__ == "__main__":
    main()