
/*
C++ Demo for Multi-Language Debugger
Demonstrates classes, recursion, and error handling
*/

#include <iostream>
#include <vector>
using namespace std;

class Calculator {
private:
    int precision;
    vector<string> history;
    
public:
    Calculator(int prec = 2) : precision(prec) {}
    
    int fibonacci(int n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    
    int factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n-1);
        }
    }
};

int main() {
    Calculator calc(2);
    
    // Test fibonacci
    int fib_result = calc.fibonacci(10);
    cout << "Fibonacci of 10: " << fib_result << endl;
    
    // Test factorial
    int fact_result = calc.factorial(5);
    cout << "Factorial of 5: " << fact_result << endl;
    
    // This will cause an error for demonstration
    // int result = 10 / 0;  // Division by zero
    
    return 0;
}
