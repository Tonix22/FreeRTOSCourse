// Copyleft (year) <Copyright Owner>
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyleft notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include <iostream>
#include <vector>


constexpr int dummyInt = 10;

// Class should use PascalCase
class TestClass {
 public:
    // Constructor name should match class name and use PascalCase
    TestClass() {
        std::cout << "Created TestClass object" << std::endl;
    }

    // Function should use CamelCase
    void PrintData() {
        std::cout << "Data: ";
        // Proper spacing and comment alignment
        for (int i = 0; i < data_.size(); ++i) {
            // Ensuring consistency in using std:: before cout
            std::cout << data_[i] << ' ';
        }
        std::cout << std::endl;
        int* value = new int(dummyInt);
        std::cout << *value << std::endl;  // Corrected spacing around <<
        delete value;  // Added to prevent memory leak
    }

    // Variable names should end with an underscore if private
    std::vector<int> data_;

    // Use emplace_back or push_back for adding elements
    void AddData(int val) {
        data_.push_back(val);  // Changed to push_back for standard compliance
    }
};

int main() {
    TestClass obj;  // Proper object naming using camelCase
    obj.AddData(1);
    obj.AddData(2);
    obj.AddData(3);
    obj.PrintData();

    return 0;
}
