cmake_minimum_required(VERSION 3.16)

# Escanear componentes también en la raíz del proyecto (donde está HAL/)
list(APPEND EXTRA_COMPONENT_DIRS "${CMAKE_SOURCE_DIR}/drivers")

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(hello_world)
