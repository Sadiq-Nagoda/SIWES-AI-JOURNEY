
tasks = []

while True:

    #Menu
    print("""
          
          
          
          
          
          
          
          
          
          
          """)
    print("========================================")
    print("            TASK MANAGER by S.U.N       ")
    print("========================================")
    print("1. Add Task")
    print("2. View Task")
    print("3. Delete Task")
    print("4. Exit")

    #User Choice
    choice = (input("Choose an option 1-4: "))
#Handling User Input
    #Adding Task 
    if choice == "1":
        task = input("Enter Task: ")
        tasks.append(task)
        print("Task added succesfully! ")
    #Viewing Task
    elif choice == "2":
        for i, tasks in enumerate(tasks, start=1):
           print(tasks)
        print("These are ur tasks!!")
        
    #Deleting Task
    elif choice == "3":
       
        for i, task in enumerate(tasks, start=1):
             num = int(input("Enter the task number you want to delete: "))
             index = num - 1
             tasks.pop(index)
        print("Deleted succesfully!")
    #Exit
    elif choice == "4":
        print("GOOD BYE!")
        break
    #handling Invalid Inputs
    else:
        print("Please Enter Valid Input!!")
    
