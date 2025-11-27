
/*
JavaScript Demo for Multi-Language Debugger
Demonstrates functions, recursion, and error handling
*/

class Calculator {
    constructor(precision = 2) {
        this.precision = precision;
        this.history = [];
    }
    
    fibonacci(n) {
        if (n <= 1) {
            return n;
        } else {
            return this.fibonacci(n-1) + this.fibonacci(n-2);
        }
    }
    
    factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * this.factorial(n-1);
        }
    }
}

function main() {
    const calc = new Calculator();
    
    // Test fibonacci
    const fib_result = calc.fibonacci(10);
    console.log(`Fibonacci of 10: ${fib_result}`);
    
    // Test factorial
    const fact_result = calc.factorial(5);
    console.log(`Factorial of 5: ${fact_result}`);
    
    // This will cause an error for demonstration
    // undefinedVariable + 10;  // ReferenceError
}

main();
