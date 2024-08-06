# Welcome to the FreeRTOS Course

This course is an open-source educational program under the MIT license, specifically designed for learning on the ESP32 platform. 
Our aim is to introduce and enforce good software practices essential for real-time operating systems, which are crucial in critical systems.

## Important Docs and Files

[Go to CourseContent](Documentation/CourseContent/CourseContent.pdf)

[Go to CoursePlanning](Documentation/CourseContent/Plannig.png)

[Go to Presentations](Documentation/Presentations)

[Go to Tools](Tools/Tools.md)

[Pytest example](Projects/dac_cosine_wave/pytest_dac_cosine_wave.py)

[Software Detailed Document Template](https://docs.google.com/document/d/1unF8FmWHeOJKlPy6cR2QpmrcaOKSOiiO/edit?usp=sharing&ouid=109808472061203912811&rtpof=true&sd=true)


## Course Tooling and Workflow

The FreeRTOS Course covers a comprehensive range of topics designed to equip you with the skills necessary for proficient and reliable coding in real-time systems:

- **RTOS Fundamentals**: Learn the basics of Real-Time Operating Systems and their importance in critical systems. [API](https://www.freertos.org/a00106.html)

- **Coding Standards**: Adhere to best practices based on the [Google Coding Standards](https://google.github.io/styleguide/cppguide.html).

- **Version Control**: Utilize Git to manage and document software changes effectively.Can learning Git basics [here](https://www.atlassian.com/git)

- **Code Linting**: Implement [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/) to ensure your code is clean, optimized, and free of common errors.

- **Software Planning**: Use [PlantUML](https://plantuml.com/) for effective planning and visualization of software designs.

- **Requirements Management**: Manage your project requirements efficiently with [Doorstop](https://doorstop.readthedocs.io/en/latest/).

- **Unit Testing**: Install Python Libraries. [Pytest Embedded](https://docs.espressif.com/projects/pytest-embedded/en/latest/)


First, ensure Python is installed on your system. Then, install `pytest` and `pytest-embedded`:
```bash
pip install pytest pytest-embedded
pytest test.py
```

## Learning Objectives

- **Build High-Quality Code**: By the end of this course, you should be able to write high-quality code that is maintainable and scalable.
- **Understand Good Practices**: Gain knowledge about coding standards, version control, and other practices that minimize bugs in production.
- **Operate Within Critical Systems**: Learn why RTOS is vital for critical systems and how good practices can significantly reduce errors in real-world applications.

## Why FreeRTOS?

FreeRTOS is widely used in critical systems where reliability and performance are paramount. By mastering FreeRTOS, you will be well-prepared to develop applications where failure can result in significant consequences. This course ensures you are equipped with both theoretical knowledge and practical skills to build robust and reliable software.

We are excited to guide you through this learning journey, where you will gain both the skills and best practices necessary for professional growth and excellence in the field of embedded systems.
