# Installing Clang-Tidy

Clang-Tidy is a linter tool for C and C++ languages, part of the Clang project. It helps in identifying typical programming errors, improving style and performance. Here's how to install Clang-Tidy on different operating systems.

## Clang rules explained

[Clang Explained](clangtydyExplained.md)

## Coding Standard

[Clang Explained](CodingStandard.md)

## Prerequisites

Before installing Clang-Tidy, ensure you have Clang installed as Clang-Tidy is part of the Clang tools. You can download Clang from the [LLVM downloads page](http://releases.llvm.org/download.html).

## Installation Instructions

### Windows

1. **Install LLVM**:
   - Download the LLVM installer from the [LLVM Download Page](https://releases.llvm.org/download.html).
   - Run the installer and make sure to select the 'Add LLVM to the system PATH for all users' option.

2. **Verify Installation**:
   - Open a command prompt and type:
     ```bash
     clang-tidy --version
     ```
   - This should display the version of Clang-Tidy installed.

### macOS

1. **Install LLVM using Homebrew**:
   - First, install Homebrew by running the following command in the Terminal:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Then, install LLVM:
     ```bash
     brew install llvm
     ```

2. **Add LLVM to your PATH**:
   - Add the following line to your `.bash_profile` or `.zshrc` file:
     ```bash
     export PATH="/usr/local/opt/llvm/bin:$PATH"
     ```

3. **Verify Installation**:
   - Open a new terminal session and type:
     ```bash
     clang-tidy --version
     ```
   - This should display the Clang-Tidy version.

### Linux

1. **Install LLVM and Clang-Tidy**:
   - You can install LLVM and Clang-Tidy using your package manager. For example, on Ubuntu:
     ```bash
     sudo apt-get install clang-tidy
     ```

2. **Verify Installation**:
   - Check the installation by running:
     ```bash
     clang-tidy --version
     ```
   - This command should print the installed version of Clang-Tidy.

## Usage

To use Clang-Tidy, you can run it from the command line by specifying the source files you want to analyze. For example:

```bash
clang-tidy your_file.cpp -- -I/path/to/headers
