
/*
Java Demo for Multi-Language Debugger
Demonstrates classes, recursion, and error handling
*/

import java.util.ArrayList;

public class Calculator {
    private int precision;
    private ArrayList<String> history;
    
    public Calculator(int prec) {
        this.precision = prec;
        this.history = new ArrayList<String>();
    }
    
    public Calculator() {
        this(2);
    }
    
    public int fibonacci(int n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    
    public int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        // Test fibonacci
        int fib_result = calc.fibonacci(10);
        System.out.println("Fibonacci of 10: " + fib_result);
        
        // Test factorial
        int fact_result = calc.factorial(5);
        System.out.println("Factorial of 5: " + fact_result);
        
        // This will cause an error for demonstration
        // int result = 10 / 0;  // ArithmeticException
    }
}
