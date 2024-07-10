#include <iostream>
#include <vector>

// Use of incorrect naming convention for class (should be PascalCase)
class testClass {
public:
    // Constructor name should match class name and use PascalCase
    testClass() {
        std::cout << "Created testClass object" << std::endl;
    }

    // Use of incorrect naming convention for function (should be CamelCase)
    void printdata() {
        std::cout << "Data: ";
        for(int i = 0; i < data.size(); ++i) { // Missing spaces and improper use of prefix increment
            std::cout << data[i] << ' '; // Lack of consistency in using std:: before cout
        }
        std::cout << std::endl;
        int* value = new int(10);
        std::cout<<*value<<std::endl;
    }

    // Incorrect naming convention for variables (should be like data_member_)
    std::vector<int> data;

    // Incorrect method for adding data (should use emplace_back or push_back with proper type)
    void AddData(int val) {
        data.insert(data.end(), val); // Non-standard way of adding elements
    }
};

int main() {
    testClass obj; // Improper object naming (should be camelCase)
    obj.AddData(1);
    obj.AddData(2);
    obj.AddData(3);
    obj.printdata();

    return 0;
}
