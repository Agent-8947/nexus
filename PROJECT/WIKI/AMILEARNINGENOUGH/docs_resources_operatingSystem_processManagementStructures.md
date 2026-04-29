# Process Management Structures

## Core Concepts

- **Process:**
    - [Wikipedia: Process (computing)](https://en.wikipedia.org/wiki/Process_(computing))
    - An instance of a program in execution.
- **Process Management:**
    - [GeeksforGeeks: Process Management in Operating System](https://www.geeksforgeeks.org/process-management-in-operating-system/)
    - The tasks performed by an operating system to manage processes.

## Key Data Structures

- **Process Control Block (PCB):**
    - [Wikipedia: Process control block](https://en.wikipedia.org/wiki/Process_control_block)
    - A data structure that stores information about a process, such as its process ID, state, program counter, register values, memory allocation details, and more.
- **Process Table:**
    - [Techopedia: Process Table](https://www.techopedia.com/definition/1066/process-table)
    - A table maintained by the operating system that contains entries (usually PCBs) for each active process.

## Process States

- **Process State:**
    - [Wikipedia: Process state](https://en.wikipedia.org/wiki/Process_state)
    - Represents the current activity of a process, such as running, ready, blocked (waiting), etc.
- **Process State Diagram:**
    - [GeeksforGeeks: Process States in Operating System](https://www.geeksforgeeks.org/process-states-in-operating-system/) 
    - Illustrates the possible states of a process and transitions between them.

## Process Scheduling

- **Process Scheduling:**
    - [Tutorialspoint: CPU Scheduling](https://www.tutorialspoint.com/operating_system/os_process_scheduling.htm)
    - The mechanism by which the operating system determines which process gets access to the CPU and for how long.
- **Scheduling Algorithms:**
    - [GeeksforGeeks: CPU Scheduling Algorithms](https://www.geeksforgeeks.org/cpu-scheduling-algorithms/)
    - Various algorithms like First-Come, First-Served (FCFS), Shortest Job First (SJF), Priority Scheduling, Round Robin, etc., used to determine the execution order of processes.

## Inter-process Communication (IPC)

- **Inter-process Communication:**
    - [Wikipedia: Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication)
    - Mechanisms that allow processes to communicate and synchronize with each other. Examples include:
        - **Pipes:** [Wikipedia: Pipeline (Unix)](https://en.wikipedia.org/wiki/Pipeline_(Unix))
        - **Message Queues:** [Wikipedia: Message queue](https://en.wikipedia.org/wiki/Message_queue)
        - **Shared Memory:** [Wikipedia: Shared memory](https://en.wikipedia.org/wiki/Shared_memory)
        - **Sockets:** [Wikipedia: Network socket](https://en.wikipedia.org/wiki/Network_socket)

## Threads and Concurrency

- **Thread (computing):**
    - [Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
    - A lightweight process that shares resources with other threads within the same process.
- **Concurrency (computer science):**
    - [Wikipedia: Concurrency (computer science)](https://en.wikipedia.org/wiki/Concurrency_(computer_science))
    - Dealing with multiple tasks seemingly at the same time.
- **Thread Synchronization:**
    - [Tutorialspoint: Thread Synchronization](https://www.tutorialspoint.com/operating-system/os_thread_synchronization.htm)
    - Mechanisms (like mutexes, semaphores, etc.) to prevent race conditions and ensure data consistency when multiple threads access shared resources.

## Additional Resources

- **Books:**
    - *Operating System Concepts* by Silberschatz, Galvin, and Gagne (**ISBN:** 978-1292400451)
    - *Modern Operating Systems* by Andrew S. Tanenbaum (**ISBN:** 978-0133591620)
