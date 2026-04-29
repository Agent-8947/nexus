# C Programming Language Cheatsheet

## Table of Contents
- [Basic Structure](#basic-structure)
- [Variables and Data Types](#variables-and-data-types)
- [Memory Management](#memory-management)
- [Binary Operators](#binary-operators)
- [Assignment Shortcuts](#assignment-shortcuts)
- [Standard Input/Output Functions](#standard-inputoutput-functions)
- [Standard Library Functions](#standard-library-functions)
- [Best Practices](#best-practices)
- [Advanced Topics](#advanced-topics)

## Basic Structure

### Program Template
```c
/* comment to describe the program */
#include <stdio.h>
/* definitions */

int main(int argc, char **argv) {
    /* variable declarations */
    /* program statements */
}
```

### Naming Conventions
Variable names must follow these rules:
- Can contain uppercase letters (A to Z)
- Can contain lowercase letters (a to z)
- Can contain numbers (0 to 9)
- Can contain underscores (_)
- Cannot start with a number
- Are case-sensitive

## Variables and Data Types

### Basic Data Types
| Data Type | Description | Example Usage |
|-----------|-------------|---------------|
| int | Integer values | `int count = -1;` |
| char | Character values | `char letter = 'A';` |
| float | Floating point numbers | `float pi = 3.141f;` |
| double | Double precision numbers | `double precise_pi = 3.14159265359;` |

### Variable Declaration Examples
```c
int age;
char initial;
float temperature;
double precise_measurement;
int *pointer_to_int;
char string_array[50];
```

## Memory Management

### Dynamic Memory Allocation
```c
// Allocating memory
int *array = (int *) malloc(sizeof(int) * 10);
if (array == NULL) {
    /* handle allocation failure */
}

// Resizing memory
int *newarray = (int *) realloc(array, sizeof(int) * 20);
if (newarray == NULL) {
    /* handle reallocation failure */
}
array = newarray;

// Freeing memory
free(array);
```

### Memory Management Best Practices
1. Always check for NULL after malloc/realloc
2. Always free allocated memory when no longer needed
3. Never free memory more than once
4. Update pointers after reallocation
5. Initialize pointers to NULL when declaring

## Binary Operators

### Bitwise Operations
| Operator | Description | Example |
|----------|-------------|----------|
| a & b | Bitwise AND | `result = 5 & 3;` |
| a \| b | Bitwise OR | `result = 5 \| 3;` |
| a ^ b | Bitwise XOR | `result = 5 ^ 3;` |
| a << n | Left shift | `result = 5 << 2;` |
| a >> n | Right shift | `result = 5 >> 2;` |

## Assignment Shortcuts

### Compound Assignment Operators
| Operator | Equivalent | Example |
|----------|------------|---------|
| += | a = a + b | `a += b;` |
| -= | a = a - b | `a -= b;` |
| *= | a = a * b | `a *= b;` |
| /= | a = a / b | `a /= b;` |
| %= | a = a % b | `a %= b;` |

## Standard Input/Output Functions

### Standard Streams
| Stream | Description | Usage |
|--------|-------------|-------|
| stdin | Standard input | Reading user input |
| stdout | Standard output | Normal program output |
| stderr | Standard error | Error messages |

### File Operations
```c
FILE *fopen(char *filename, char *mode);
size_t fread(void *ptr, size_t size, size_t nitems, FILE *stream);
int fclose(FILE *stream);
```

### Input/Output Functions
```c
// String output
int puts(char *string);
int printf(char *format, ...);
int fprintf(FILE *stream, char *format);
int sprintf(char *string, char *format);

// Character input/output
int getc(FILE *stream);
int putc(int ch, FILE *stream);
int getchar(void);
int putchar(int ch);
```

## Standard Library Functions

### Memory Management Functions
```c
void *malloc(size_t size);
void *realloc(void *ptr, size_t newsize);
void free(void *ptr);
```

### Sorting and Searching
```c
void qsort(void *array, size_t nitems, size_t size, 
           int (*compar)(void *a, void *b));
void *bsearch(void *key, void *array, size_t nitems, 
              size_t size, int (*compar)(void *a, void *b));
```

### Random Number Generation
```c
void srand(unsigned int seed);
int rand(void);
```

## Best Practices

### Memory Management Guidelines
1. Always initialize variables before use
2. Check return values from memory allocation functions
3. Free dynamically allocated memory
4. Avoid memory leaks
5. Use appropriate data types for variables

### Code Organization
1. Include necessary header files at the start
2. Define constants and macros after headers
3. Declare global variables (if needed) after definitions
4. Define functions before use or provide prototypes
5. Use meaningful variable and function names

### Error Handling
1. Always check return values of system calls
2. Use stderr for error messages
3. Implement proper error recovery mechanisms
4. Clean up resources in error conditions
5. Use appropriate error codes

## Advanced Topics

### Function Pointers
```c
// Declaration of a function pointer
int (*operation)(int, int);

// Example usage
int add(int a, int b) {
    return a + b;
}

operation = &add;
int result = (*operation)(5, 3);
```

### Structures and Unions
```c
struct Point {
    int x;
    int y;
};

union Data {
    int i;
    float f;
    char str[20];
};
```

### Preprocessor Directives
```c
#define MAX_SIZE 100
#define SQUARE(x) ((x) * (x))
#ifdef DEBUG
    // Debug code
#endif
#ifndef HEADER_H
#define HEADER_H
    // Header content
#endif
```

### Type Definitions
```c
typedef unsigned long ulong;
typedef struct Point Point;
typedef void (*CallbackFunc)(void *data);
```

### Bit Fields
```c
struct Flags {
    unsigned int is_active : 1;
    unsigned int is_urgent : 1;
    unsigned int priority : 3;
};
```

## Common Programming Patterns

### Buffer Management
```c
#define BUFFER_SIZE 1024

char buffer[BUFFER_SIZE];
size_t bytes_read;

// Safe reading
if ((bytes_read = fread(buffer, 1, BUFFER_SIZE - 1, file)) > 0) {
    buffer[bytes_read] = '\0';
}
```

### String Manipulation
```c
// String copy with bounds checking
char dest[50];
const char *src = "Hello, World!";
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### Command Line Arguments
```c
int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        printf("Argument %d: %s\n", i, argv[i]);
    }
    return 0;
}
```

## Debugging Tips

### Common Debugging Techniques
1. Use printf debugging
2. Check return values
3. Validate pointer operations
4. Monitor memory usage
5. Use assert statements

### Assert Usage
```c
#include <assert.h>

void process_data(int *data, size_t size) {
    assert(data != NULL);
    assert(size > 0);
    // Process data
}
```

## Performance Optimization

### Optimization Techniques
1. Use appropriate data structures
2. Minimize memory allocation
3. Optimize loops
4. Use bitwise operations when applicable
5. Consider cache efficiency

### Example Optimizations
```c
// Optimized loop
for (int i = 0; i < size; i++) {
    // Cache the value to avoid multiple array accesses
    int temp = array[i];
    if (temp > max) {
        max = temp;
    }
}
```
