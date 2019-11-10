# jcl - Job scheduler/manager

Background service, "master", launches & manages jobs

Jobs specified with JSON files

Command line client interface

    jcl [<command>] [args] [options]

        // General
        help                            Show help
        tail                            Watch master log of process events
    
        // Configuration
        config                          Show config information
        config set <tag>=<value>        Set config tag
        config unset tag                Remove config tag
    
        // JCL Master management
        master status                   Show whether jcl master is running (& other info)
        master start                    Start jcl master running
        master stop                     Stop master
        master install                  Install master as Windows service
        master uninstall                Uninstall Windows service
        
        // All processes
        list                            Show status of all processes
        
        // Process creation/editing
        add <proc>                      Create a process by name
        edit <proc>                     Edit process by name
        remove <proc>                   Remove process by name
        
        // Run management
        run <proc>                      Kick off process
        redo <proc>                     Restart failed process
        cancel <proc>                   Cancel process (for today)
        kill <proc>                     Kill running process and mark as failed
        reset <proc>                    Reset process status for today
        
        // Options
        --date <yyyymmdd>|-<n>          Address process run for specific date (default: today)
        --tail                          Watch master log of process events
        
         

Web site interface

