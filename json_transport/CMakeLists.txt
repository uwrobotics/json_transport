cmake_minimum_required(VERSION 3.5)
project(json_transport)

# Set C++ standard (ROS 2 defaults to C++14, but we ensure it)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optionally add compile flags
add_compile_options(-Wall -Werror)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(json_msgs REQUIRED)
find_package(nlohmann_json REQUIRED)

# Create an INTERFACE library target for this header-only package.
add_library(${PROJECT_NAME} INTERFACE)
target_include_directories(${PROJECT_NAME} INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# Export dependencies so that downstream packages linking to json_transport get these includes.
ament_export_dependencies(rclcpp json_msgs nlohmann_json)
ament_export_include_directories(include)

# Install the INTERFACE target with an export name
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}Targets
  INCLUDES DESTINATION include
)

# Export the installed targets for downstream usage
ament_export_targets(${PROJECT_NAME}Targets)

# Install public header files (the header files should be placed in include/json_transport/)
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
)

# Install extra files (e.g. pip requirements)
install(FILES requirements.txt
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  # Linting (requires ament_lint_auto)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
