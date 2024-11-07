1. **Core Guidelines (`cppcoreguidelines-`)**

    - `cppcoreguidelines-avoid-magic-numbers`: Avoid using magic numbers; use named constants instead.
    - `cppcoreguidelines-non-private-member-variables-in-classes`: Enforces that member variables should be private to maintain encapsulation.
    - `cppcoreguidelines-pro-bounds-array-to-pointer-decay`: Warns about array-to-pointer decay, which can lead to unexpected behavior.

2. **Modernize (`modernize-`)**

    - `modernize-use-nullptr`: Suggests replacing `NULL` or `0` with `nullptr` in C++11 and later.
    - `modernize-use-auto`: Recommends using `auto` for variable declarations where the type is obvious.
    - `modernize-use-override`: Ensures that functions overriding a virtual function are marked with `override`.

3. **Readability (`readability-`)**

    - `readability-identifier-naming`: Enforces consistent naming conventions for variables, functions, classes, etc.
    - `readability-braces-around-statements`: Enforces the use of braces for single-statement blocks.
    - `readability-function-cognitive-complexity`: Warns if a function is too complex, encouraging simplification.

4. **Google Style (`google-`)**

    - `google-readability-braces-around-statements`: Enforces Google style braces around statements.
    - `google-runtime-references`: Suggests using pointers instead of non-const references for out parameters.
    - `google-explicit-constructor`: Ensures constructors that can be called with a single argument are marked `explicit`.

5. **Performance (`performance-`)**

    - `performance-for-range-copy`: Warns if a loop copies the loop variable instead of using a reference.
    - `performance-unnecessary-copy-initialization`: Detects unnecessary copy initializations and suggests alternatives.
    - `performance-noexcept-move-constructor`: Suggests marking move constructors `noexcept` to allow better optimization.

6. **Bugprone (`bugprone-`)**

    - `bugprone-branch-clone`: Warns about identical code in different branches of conditional statements.
    - `bugprone-narrowing-conversions`: Detects potential data loss due to narrowing conversions.
    - `bugprone-macro-parentheses`: Ensures that macros with arguments are properly parenthesized.

7. **Miscellaneous (`misc-`)**

    - `misc-non-private-member-variables-in-classes`: Ensures that all member variables are private.
    - `misc-unused-parameters`: Warns about unused function parameters.
    - `misc-no-recursion`: Warns if recursion is detected in a function, which might lead to stack overflow.

8. **Portability (`portability-`)**

    - `portability-simd-intrinsics`: Warns about using SIMD intrinsics that may not be portable across different platforms.
    - `portability-restrict-system-includes`: Ensures that system includes are portable across different platforms.

9. **LLVM Style (`llvm-`)**

    - `llvm-header-guard`: Ensures consistent and correct use of header guards in LLVM-style.
    - `llvm-namespace-comment`: Requires namespace comments for nested namespaces to improve readability.
    - `llvm-else-after-return`: Ensures that `else` after `return` statements is removed for clarity.

10. **Clang Analyzer (`clang-analyzer-`)**

    - `clang-analyzer-core.CallAndMessage`: Detects bugs related to function calls, such as calling a function on a null pointer.
    - `clang-analyzer-deadcode.DeadStores`: Detects dead stores, where values are assigned but never read.
    - `clang-analyzer-optin.performance.Padding`: Warns about excessive padding in structs or classes, which can impact performance.

11. **Safety (`safety-`)**

    - `safety-no-assembler`: Ensures that no assembler code is used, which can be non-portable and error-prone.
    - `safety-delete-null-pointer`: Ensures that deleting a null pointer is handled safely.
