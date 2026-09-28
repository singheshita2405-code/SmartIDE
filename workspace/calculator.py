# SmartIDE — Math & Utilities Demo

class SmartCalculator:
    def add(self, a, b):
        return a + b
        
    def multiply(self, a, b):
        return a * b
        
    def power(self, base, exp):
        return base ** exp

if __name__ == "__main__":
    calc = SmartCalculator()
    print("Testing SmartCalculator:")
    print("12 + 25 =", calc.add(12, 25))
    print("7 * 8 =", calc.multiply(7, 8))
    print("2 ** 10 =", calc.power(2, 10))
    print("All tests passed cleanly!")
