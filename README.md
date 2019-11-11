# jcl - Job scheduler/manager

Background service, "master", launches & manages jobs

Jobs specified with JSON files

Command line client interface

    jcl [<command>] [args] [options]

        // General
        help                            Show help
        tail                            Watch master log of job events
    
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
        list                            Show status of all jobs
        
        // Process creation/editing
        add <proc>                      Create a job by name
        edit <proc>                     Edit job by name
        remove <proc>                   Remove job by name
        show <proc>                     Show job settings
        
        // Run management
        run <proc>                      Kick off job
        redo <proc>                     Restart failed job
        cancel <proc>                   Cancel job (for today)
        kill <proc>                     Kill running job and mark as failed
        reset <proc>                    Reset job status for today
        
        // Options
        --date <yyyymmdd>|-<n>          Address master for specific date (default: today)
        --tail                          Watch master log of job events
        
         

Web site interface

