# tasknet
Job runner &amp; manager

Tasknet manages jobs that are intended to be run on a standalone basis
(without user interaction).  It launches jobs as scheduled, redirects their standard output,
and notifies by email of any unexpected behavior.

Tasknet can be run by a single user on a single standalone machine, or on multiple machines.
Coordination of tasks across machines is possible if the machines have read/write privileges
to a common fileshare.

Tasknet uses only the file system, and apart from python (in which it is written) requires
no outside software (like databases).  [Note: requires an email mechanism to send email 
notifications.]

