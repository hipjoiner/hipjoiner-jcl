# jcl - Job runner & manager

Background service, "master", launches & manages jobs

Jobs specified with JSON files

Command line client interface

    jcl
        // Configuration
        config                  Show config information
        set <tag>=<value>       Set config tag
        unset tag               Remove config tag
    
        // Master management
        master status
        master start
        master stop
        
        // All processes
        list                    Show status of all processes
        
        // Process creation/editing
        add <proc>              Create a process by name
        edit <proc>             Edit process by name
        remove <proc>           Remove process by name
        
        // Process running
        run <proc>              Kick off process
        redo <proc>             Restart failed process
        cancel <proc>
        kill <proc>
        
         

Web site interface

