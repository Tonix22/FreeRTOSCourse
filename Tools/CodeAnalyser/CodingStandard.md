# Markdown Guide for C++ Tooling and Style

This document provides links and commands relevant to C++ coding standards, tools for custom coding standards, and extensions for enhanced development practices.

## Resources and Installation Commands

### Google C++ Style Guide

For an extensive overview of the C++ style recommendations by Google, see the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).

### Installing Clang-Tidy

Clang-Tidy is a tool that can be used to adhere to custom coding standards. To install Clang-Tidy on your system, use the following command:

    sudo apt-get install clang-tidy

For more information about Clang-Tidy, visit [Clang-Tidy on LLVM.org](https://clang.llvm.org/extra/clang-tidy/).

### Using Clang-Tidy

To use Clang-Tidy with your C++ files:

    clang-tidy my_file.cpp -- -Iinclude_directory

### VS Code Extension for Clang-Tidy

For those using Visual Studio Code, enhance your C++ coding with the [CS128-clang-tidy extension](https://marketplace.visualstudio.com/items?itemName=CS128.cs128-clang-tidy).

## Running Code Linters

### Cpp Lint

For a more superficial check, `cpplint` can be used without needing Clang-Tidy:

    cpplint Test.cpp

### Running Clang-Tidy

To perform a detailed check with Clang-Tidy:

    clang-tidy Test.cpp

These tools and guidelines will help maintain high-quality C++ code in line with recognized standards and practices.
